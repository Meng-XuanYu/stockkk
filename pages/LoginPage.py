from PySide6.QtGui import Qt, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy
from exceptions.WrongUsernameException import WrongUsernameException
from exceptions.WrongPassWordException import WrongPassWordException


class LoginPage(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.setObjectName("login_page")
        self.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # 添加应用程序图标
        self.app_icon = QLabel(self)
        self.app_icon.setAlignment(Qt.AlignCenter)
        self.app_icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.app_icon.setPixmap(QPixmap("./images/images/stockkk_vertical.jpg"))
        self.app_icon.adjustSize()
        layout.addWidget(self.app_icon)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setStyleSheet(
            "background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "background-color: rgb(33, 37, 43); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px;")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("登录", self)
        self.login_button.setStyleSheet(
            "background-color: rgb(52, 59, 72); color: rgb(221, 221, 221); border-radius: 5px; padding: 10px; font-size: 18px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

    def resizeEvent(self, event):
        pixmap = QPixmap("./images/images/stockkk_vertical.jpg")
        scaled_pixmap = pixmap.scaled(self.app_icon.width(), self.app_icon.height(), Qt.KeepAspectRatio)
        self.app_icon.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def login(self):
        try:
            import main
            self.interface.user_login(self.username_input.text(), self.password_input.text())
            QMessageBox.information(self, "成功", "登录成功")

            self.new_main_window = main.MainWindow(self.interface)
            self.interface.change_window(self.new_main_window)
            self.new_main_window.show()
        except (WrongUsernameException, WrongPassWordException):
            QMessageBox.warning(self, "错误", "用户名或密码错误")
