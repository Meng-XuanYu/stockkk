import re
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy

from main import widgets


class ChangePasswordPage(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.setObjectName('change_password_page')
        self.setStyleSheet('background-color: rgb(40, 44, 52);')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        self.app_icon = QLabel(self)
        self.app_icon.setAlignment(Qt.AlignCenter)
        self.app_icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.app_icon.setPixmap(QPixmap("./images/images/stockkk_vertical.jpg"))
        self.app_icon.adjustSize()
        layout.addWidget(self.app_icon)

        layout.addSpacing(10)

        self.current_password_input = QLineEdit(self)
        self.current_password_input.setPlaceholderText('当前密码')
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.current_password_input)

        layout.addSpacing(10)

        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText('新密码')
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.new_password_input)

        layout.addSpacing(3)

        password_requirements = QLabel(
            '密码要求：8-20个字符，必须包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符', self)
        password_requirements.setStyleSheet('color: rgb(150, 150, 150);')  # 将文字颜色调成灰色
        layout.addWidget(password_requirements)

        self.confirm_new_password_input = QLineEdit(self)
        self.confirm_new_password_input.setPlaceholderText('确认新密码')
        self.confirm_new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_new_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.confirm_new_password_input)

        layout.addSpacing(10)

        self.change_password_button = QPushButton('修改密码', self)
        self.change_password_button.setStyleSheet(
            'background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px; font-size: 18px;')
        self.change_password_button.clicked.connect(self.change_password)
        layout.addWidget(self.change_password_button)

    def resizeEvent(self, event):
        pixmap = QPixmap("./images/images/stockkk_vertical.jpg")
        scaled_pixmap = pixmap.scaled(self.app_icon.width(), self.app_icon.height(), Qt.KeepAspectRatio)
        self.app_icon.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def change_password(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setIconPixmap(QPixmap('images/images/stockkk.jpg'))
        msg_box.setText("确定要修改密码吗？")
        msg_box.setWindowTitle("确认修改")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            current_password = self.current_password_input.text()
            new_password = self.new_password_input.text()
            confirm_new_password = self.confirm_new_password_input.text()
            if not current_password or not new_password or not confirm_new_password:
                QMessageBox.warning(self, "修改密码失败", "所有字段均不能为空")
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', new_password):
                QMessageBox.warning(self, "修改密码失败", "新密码不符合要求")
                return
            elif not self.interface.get_current_user().check_password(current_password):
                QMessageBox.warning(self, "修改密码失败", "当前密码错误")
            else:
                if new_password == confirm_new_password:
                    self.interface.change_user_password(self.interface.get_current_user(), new_password)
                    QMessageBox.information(self, '成功', '密码修改成功')
                    self.interface.get_window().back_home_page()
                else:
                    QMessageBox.warning(self, '错误', '新密码不匹配')
