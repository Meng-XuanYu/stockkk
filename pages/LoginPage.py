from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("login_page")
        self.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("登录", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: rgb(221, 221, 221);")
        layout.addWidget(title)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setStyleSheet("background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("登录", self)
        self.login_button.setStyleSheet("background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # 这里添加登录逻辑
        if username == "admin" and password == "admin":
            QMessageBox.information(self, "成功", "登录成功")
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误")
