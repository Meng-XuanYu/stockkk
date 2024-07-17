import sys
from PyQt5.QtWidgets import QApplication
from ui.login_dialog import LoginDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 加载样式
    with open('ui/style.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    login_window = LoginDialog()
    login_window.show()
    sys.exit(app.exec_())
