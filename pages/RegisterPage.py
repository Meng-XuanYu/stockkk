from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import re

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
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        app_icon = QLabel(self)
        app_icon.setAlignment(Qt.AlignCenter)
        app_icon.setPixmap(QIcon("./images/images/stockkk_vertical.jpg").pixmap(235, 246))  # 替换为你的图标路径和大小
        layout.addWidget(app_icon)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('用户名')
        self.username_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText('确认密码')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(
            'background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton('注册', self)
        self.register_button.setStyleSheet(
            'background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;')
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "注册失败", "用户名和密码不能为空")
            return
        elif not re.match(r'^[a-zA-Z0-9_]{6,20}$', username) or not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', password):
            QMessageBox.warning(self, "注册失败", "用户名或密码不符合要求")
            return
        if password == confirm_password:
            try:
                self.interface.create_user(username, password)
            except WrongUsernameException:
                QMessageBox.warning(self, "注册失败", "用户名已存在，请重试。")
                return
            QMessageBox.information(self, '成功', '注册成功')
            self.close()
        else:
            QMessageBox.warning(self, '错误', '密码不匹配')
