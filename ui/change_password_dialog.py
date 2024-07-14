from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import re


class ChangePasswordDialog(QDialog):
    def __init__(self, interface, user):
        super().__init__()
        self.interface = interface
        self.user = user

        self.setWindowTitle("修改密码")
        self.setGeometry(400, 400, 300, 250)

        layout = QVBoxLayout()

        self.old_password_label = QLabel("旧密码:", self)
        layout.addWidget(self.old_password_label)
        self.old_password_entry = QLineEdit(self)
        self.old_password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_password_entry)

        self.new_password_label = QLabel("新密码:", self)
        layout.addWidget(self.new_password_label)
        self.new_password_entry = QLineEdit(self)
        self.new_password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_entry)

        self.confirm_new_password_label = QLabel("确认新密码:", self)
        layout.addWidget(self.confirm_new_password_label)
        self.confirm_new_password_entry = QLineEdit(self)
        self.confirm_new_password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_new_password_entry)

        self.change_password_button = QPushButton("修改密码", self)
        self.change_password_button.clicked.connect(self.handle_change_password)
        layout.addWidget(self.change_password_button)

        self.setLayout(layout)

    def handle_change_password(self):
        old_password = self.old_password_entry.text()
        new_password = self.new_password_entry.text()
        confirm_new_password = self.confirm_new_password_entry.text()
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', new_password):
            QMessageBox.warning(self, "修改失败", "新密码不符合要求，请重试。")
            return
        if self.user.check_password(old_password) and new_password == confirm_new_password:
            self.interface.change_user_password(self.user, new_password)
            QMessageBox.information(self, "修改成功", "密码修改成功！")
            self.close()
        else:
            QMessageBox.warning(self, "修改失败", "旧密码错误或新密码不匹配，请重试。")
