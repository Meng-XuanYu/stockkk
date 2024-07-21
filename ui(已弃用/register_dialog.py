import re

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from exceptions.WrongUsernameException import WrongUsernameException


class RegisterDialog(QDialog):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        self.setWindowTitle("用户注册")
        self.setGeometry(400, 400, 300, 300)  # 稍微增加高度以容纳提示信息

        layout = QVBoxLayout()

        self.username_label = QLabel("用户名:", self)
        layout.addWidget(self.username_label)
        self.username_entry = QLineEdit(self)
        layout.addWidget(self.username_entry)
        self.username_hint = QLabel("用户名必须由字母、数字、下划线组成，长度在6到20之间。", self)
        self.username_hint.setStyleSheet("font-size: 10px; color: gray;")  # 设置提示信息的样式
        layout.addWidget(self.username_hint)

        self.password_label = QLabel("密码:", self)
        layout.addWidget(self.password_label)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)
        self.password_hint = QLabel("密码必须包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符，长度在8到20之间。", self)
        self.password_hint.setStyleSheet("font-size: 10px; color: gray;")  # 设置提示信息的样式
        layout.addWidget(self.password_hint)

        self.confirm_password_label = QLabel("确认密码:", self)
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_entry = QLineEdit(self)
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_entry)

        self.register_button = QPushButton("注册", self)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "注册失败", "用户名和密码不能为空，请重试。")
            return
        elif not re.match(r'^[a-zA-Z0-9_]{6,20}$', username) or not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', password):
            QMessageBox.warning(self, "注册失败", "用户名或密码不符合要求，请重试。")
            return
        if password == confirm_password:
            try:
                self.interface.create_user(username, password)
            except WrongUsernameException:
                QMessageBox.warning(self, "注册失败", "用户名已存在，请重试。")
                return
            QMessageBox.information(self, "注册成功", "注册成功，" + username + "！")
            self.close()
        else:
            QMessageBox.warning(self, "注册失败", "两次输入的密码不一致，请重试。")
