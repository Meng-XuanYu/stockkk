import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 加载样式
    with open('ui/style.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
