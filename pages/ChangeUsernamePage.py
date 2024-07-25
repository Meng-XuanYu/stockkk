import re
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy


class ChangeUsernamePage(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.setObjectName('change_username_page')
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
        self.current_password_input.setPlaceholderText('密码')
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.current_password_input)

        layout.addSpacing(10)

        self.new_username_input = QLineEdit(self)
        self.new_username_input.setPlaceholderText('新用户名')
        self.new_username_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.new_username_input)

        layout.addSpacing(3)

        username_requirements = QLabel(
            '用户名要求：6-20个字符，只能包含字母、数字和下划线，不区分大小写', self)
        username_requirements.setStyleSheet('color: rgb(150, 150, 150);')
        layout.addWidget(username_requirements)

        layout.addSpacing(10)

        self.change_username_button = QPushButton('修改用户名', self)
        self.change_username_button.setStyleSheet(
            'background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px; font-size: 18px;')
        self.change_username_button.clicked.connect(self.change_username)
        layout.addWidget(self.change_username_button)

    def resizeEvent(self, event):
        pixmap = QPixmap("./images/images/stockkk_vertical.jpg")
        scaled_pixmap = pixmap.scaled(self.app_icon.width(), self.app_icon.height(), Qt.KeepAspectRatio)
        self.app_icon.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def change_username(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.setText("确定要修改用户名吗？")
        msg_box.setWindowTitle("确认修改")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            current_password = self.current_password_input.text()
            new_username = self.new_username_input.text().lower()
            if not current_password or not new_username:
                QMessageBox.warning(self, "修改用户名失败", "所有字段不能为空")
                return
            elif not re.match(r'^[a-zA-Z0-9_]{6,20}$', new_username):
                QMessageBox.warning(self, "修改用户名失败", "新用户名不符合要求")
                return
            elif not self.interface.get_current_user().check_password(current_password):
                QMessageBox.warning(self, "修改用户名失败", "当前密码错误")
            else:
                self.interface.user_rename(self.interface.get_current_user(), new_username)
                QMessageBox.information(self, '成功', '用户名修改成功')
                self.interface.get_window().back_home_page()
