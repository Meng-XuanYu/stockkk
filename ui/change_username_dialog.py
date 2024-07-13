from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class ChangeUsernameDialog(QDialog):
    def __init__(self):
        super().__init__()

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
        old_username = self.old_username_entry.text()
        new_username = self.new_username_entry.text()

        if old_username == new_username:
            QMessageBox.information(self, "修改成功", "用户名修改成功！")
            # TODO: 修改数据库中的用户名
            self.close()
        else:
            QMessageBox.warning(self, "修改失败", "前后用户名不一致，请重新输入。")
