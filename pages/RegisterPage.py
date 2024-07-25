import re
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy

import main
from exceptions.WrongUsernameException import WrongUsernameException


class RegisterPage(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.setObjectName('register_page')
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

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('用户名')
        self.username_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.username_input)

        layout.addSpacing(3)

        username_requirements = QLabel(
            '用户名要求：6-20个字符，只能包含字母、数字和下划线，不区分大小写', self)
        username_requirements.setStyleSheet('color: rgb(150, 150, 150);')
        layout.addWidget(username_requirements)

        layout.addSpacing(10)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.password_input)

        layout.addSpacing(3)

        password_requirements = QLabel(
            '密码要求：8-20个字符，必须包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符', self)
        password_requirements.setStyleSheet('color: rgb(150, 150, 150);')  # 将文字颜色调成灰色
        layout.addWidget(password_requirements)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText('确认密码')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.confirm_password_input)

        layout.addSpacing(10)

        self.register_button = QPushButton('注册', self)
        self.register_button.setStyleSheet(
            'background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px; font-size: 18px;')
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

    def resizeEvent(self, event):
        pixmap = QPixmap("./images/images/stockkk_vertical.jpg")
        scaled_pixmap = pixmap.scaled(self.app_icon.width(), self.app_icon.height(), Qt.KeepAspectRatio)
        self.app_icon.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def register(self):
        username = self.username_input.text().lower()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if not username or not password or not confirm_password:
            information_box = QMessageBox()
            information_box.setIcon(QMessageBox.Warning)
            icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
            information_box.setIconPixmap(icon_pixmap)
            information_box.setText("用户名或密码不能为空")
            information_box.setWindowTitle("注册失败")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()
            return
        elif not re.match(r'^[a-zA-Z0-9_]{6,20}$', username) or not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', password):
            QMessageBox.warning(self, "注册失败", "用户名或密码不符合要求")
            return
        if password == confirm_password:
            try:
                self.interface.create_user(username, password)
            except WrongUsernameException:
                information_box = QMessageBox()
                information_box.setIcon(QMessageBox.Warning)
                icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
                information_box.setIconPixmap(icon_pixmap)
                information_box.setText("用户名已存在，请重试。")
                information_box.setWindowTitle("注册失败")
                information_box.setStandardButtons(QMessageBox.Ok)
                information_box.exec_()
                return
            information_box = QMessageBox()
            information_box.setIcon(QMessageBox.Warning)
            icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
            information_box.setIconPixmap(icon_pixmap)
            information_box.setText("注册成功，已自动登录")
            information_box.setWindowTitle("注册成功")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()
            self.interface.user_login(self.username_input.text(), self.password_input.text())
            self.new_main_window = main.MainWindow(self.interface)
            self.interface.change_window(self.new_main_window)
            self.new_main_window.show()
            self.close()
        else:
            information_box = QMessageBox()
            information_box.setIcon(QMessageBox.Warning)
            icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
            information_box.setIconPixmap(icon_pixmap)
            information_box.setText("两次密码不匹配")
            information_box.setWindowTitle("注册失败")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()
            return
