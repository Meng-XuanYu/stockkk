from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from .register_dialog import RegisterDialog
from exceptions.WrongPassWordException import WrongPassWordException
from exceptions.WrongUsernameException import WrongUsernameException


class LoginDialog(QDialog):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        self.setWindowTitle("用户登录")
        self.setGeometry(400, 400, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("用户名:", self)
        layout.addWidget(self.username_label)
        self.username_entry = QLineEdit(self)
        layout.addWidget(self.username_entry)

        self.password_label = QLabel("密码:", self)
        layout.addWidget(self.password_label)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # 添加注册按钮
        register_layout = QHBoxLayout()
        register_label = QLabel("还没有账号？", self)
        register_layout.addWidget(register_label)

        self.register_button = QPushButton("注册", self)
        self.register_button.clicked.connect(self.show_register_dialog)
        register_layout.addWidget(self.register_button)

        layout.addLayout(register_layout)

        self.setLayout(layout)

    def handle_login(self):
        try:
            user = self.interface.get_user(self.username_entry.text(), self.password_entry.text())
            self.accept()
            QMessageBox.information(self, "登录成功", f"欢迎，{user}！")
        except (WrongUsernameException, WrongPassWordException):
            QMessageBox.warning(self, "登录失败", "用户名或密码错误，请重试。")

    def show_register_dialog(self):
        self.close()
        register_dialog = RegisterDialog()
        register_dialog.exec_()
