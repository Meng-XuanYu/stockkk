from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import re

from exceptions.WrongUsernameException import WrongUsernameException


class ChangeUsernameDialog(QDialog):
    def __init__(self, interface, user):
        super().__init__()
        self.interface = interface
        self.user = user

        self.setWindowTitle("修改用户名")
        self.setGeometry(400, 400, 300, 200)

        layout = QVBoxLayout()

        self.old_username_label = QLabel("新用户名:", self)
        layout.addWidget(self.old_username_label)
        self.old_username_entry = QLineEdit(self)
        layout.addWidget(self.old_username_entry)

        self.new_username_label = QLabel("确定新用户名:", self)
        layout.addWidget(self.new_username_label)
        self.new_username_entry = QLineEdit(self)
        layout.addWidget(self.new_username_entry)

        self.change_username_button = QPushButton("修改用户名", self)
        self.change_username_button.clicked.connect(self.handle_change_username)
        layout.addWidget(self.change_username_button)

        self.setLayout(layout)

    def handle_change_username(self):
        new_username = self.old_username_entry.text()
        confirmed_new_username = self.new_username_entry.text()
        if not re.match(r'^[a-zA-Z0-9_]{6,20}$', new_username):
            QMessageBox.warning(self, "修改失败", "新用户名不符合要求，请重新输入。")
            return
        elif self.user.get_name() == new_username:
            QMessageBox.warning(self, "修改失败", "新用户名不能与原用户名相同，请重新输入。")
            return
        if new_username == confirmed_new_username:
            try:
                self.interface.user_rename(self.user, confirmed_new_username)
            except WrongUsernameException:
                QMessageBox.warning(self, "修改失败", "该用户名已存在，请重新输入。")
                return
            QMessageBox.information(self, "修改成功", "用户名修改成功！")
            self.close()
        else:
            QMessageBox.warning(self, "修改失败", "前后用户名不一致，请重新输入。")
