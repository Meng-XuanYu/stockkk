import atexit
import sys
from interface.Interface import Interface
from modules import *
widgets = None


class MainWindow(QMainWindow):
    def __init__(self, interface=None, first_time=False):
        from modules import UIMainWindow, Settings, UIFunctions, AppFunctions
        QMainWindow.__init__(self)

        if interface is None:
            self.interface = Interface()
            self.ui = UIMainWindow()
        else:
            self.interface = interface
            self.ui = UIMainWindow(interface)
        self.ui.setup_ui(self)
        global widgets
        widgets = self.ui
        if first_time:
            app.setWindowIcon(QIcon('images/images/stockkk.jpg'))

        # mac用false, windows用true，windows效果好一点
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        # Settings.ENABLE_CUSTOM_TITLE_BAR = False

        title = 'Stockkk'
        description = 'Stockkk APP - Stock market data visualizer and analysis tool.'
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # 边栏动画
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggle_menu(self, True))

        UIFunctions.ui_definitions(self)

        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 链接左边栏和点击事件
        widgets.btn_home.clicked.connect(self.button_click)
        widgets.btn_read_data.clicked.connect(self.button_click)
        widgets.btn_history.clicked.connect(self.button_click)
        widgets.btn_picture.clicked.connect(self.button_click)
        widgets.btn_login.clicked.connect(self.button_click)
        widgets.btn_logout.clicked.connect(self.button_click)
        widgets.btn_register.clicked.connect(self.button_click)
        widgets.btn_change_password.clicked.connect(self.button_click)
        widgets.btn_change_username.clicked.connect(self.button_click)

        # 左边栏动画是否开启
        def open_close_left_box():
            UIFunctions.toggle_left_box(self, True)

        widgets.toggle_left_box.clicked.connect(open_close_left_box)
        widgets.extraCloseColumnBtn.clicked.connect(open_close_left_box)

        # 右边栏动画是否开启
        def open_close_right_box():
            UIFunctions.toggle_right_box(self, True)

        widgets.userBtn.clicked.connect(open_close_right_box)

        self.show()

        AppFunctions.set_theme_hack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.select_menu(widgets.btn_home.styleSheet()))

    # 点击事件
    def button_click(self):
        from modules import UIFunctions
        btn = self.sender()
        btn_name = btn.objectName()

        if btn_name == 'btn_home':
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_read_data':
            widgets.stackedWidget.setCurrentWidget(widgets.read_data_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_history':
            widgets.stackedWidget.setCurrentWidget(widgets.user_log_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_picture':
            widgets.stackedWidget.setCurrentWidget(widgets.picture_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_login':
            widgets.stackedWidget.setCurrentWidget(widgets.login_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_logout':
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
            msg_box.setIconPixmap(icon_pixmap)
            msg_box.setText("确定要退出登录吗？")
            msg_box.setWindowTitle("确认退出")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg_box.exec_()
            if result == QMessageBox.Yes:
                self.interface.user_logout()
                new_window = MainWindow(self.interface)
                self.interface.change_window(new_window)
                new_window.show()

        if btn_name == 'btn_register':
            widgets.stackedWidget.setCurrentWidget(widgets.register_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_change_password':
            widgets.stackedWidget.setCurrentWidget(widgets.change_password_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

        if btn_name == 'btn_change_username':
            widgets.stackedWidget.setCurrentWidget(widgets.change_username_page)
            UIFunctions.reset_style(self, btn_name)
            btn.setStyleSheet(UIFunctions.select_menu(btn.styleSheet()))

    # 实时变化
    def resizeEvent(self, event):
        from modules import UIFunctions
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def back_home_page(self):
        from modules import UIFunctions
        global widgets
        widgets = self.ui
        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        UIFunctions.reset_style(self, 'btn_home')


def on_exit(interface):
    if interface.get_current_user() is not None:
        interface.user_logout()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    interface = Interface()
    window = MainWindow(interface, first_time=True)
    interface.set_window(window)
    window.show()
    atexit.register(on_exit, interface)
    sys.exit(app.exec())
