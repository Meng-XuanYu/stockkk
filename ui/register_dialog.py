from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("用户注册")
        self.setGeometry(400, 400, 300, 250)

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
        if password == confirm_password:
            QMessageBox.information(self, "注册成功", "欢迎，" + username + "！")
            self.accept()
        else:
            QMessageBox.warning(self, "注册失败", "两次输入的密码不一致，请重试。")
