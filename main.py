import sys
import os
import platform
from modules import *
from widgets import *

widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # mac用false, windows用true，windows效果好一点
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        # Settings.ENABLE_CUSTOM_TITLE_BAR = False

        title = "Stockkk"
        description = "Stockkk APP - Stock market data visualizer and analysis tool."
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # 边栏动画
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)

        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 链接左边栏和点击事件
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_read_data.clicked.connect(self.buttonClick)
        widgets.btn_history.clicked.connect(self.buttonClick)
        widgets.btn_picture.clicked.connect(self.buttonClick)
        widgets.btn_login.clicked.connect(self.buttonClick)
        widgets.btn_logout.clicked.connect(self.buttonClick)
        widgets.btn_register.clicked.connect(self.buttonClick)

        # 左边栏动画是否开启
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # 右边栏动画是否开启
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.userBtn.clicked.connect(openCloseRightBox)

        self.show()

        AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # 点击事件
    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_read_data":
            widgets.stackedWidget.setCurrentWidget(widgets.read_data_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_history":
            pass

        if btnName == "btn_picture":
            widgets.stackedWidget.setCurrentWidget(widgets.picture_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_login":
            widgets.stackedWidget.setCurrentWidget(widgets.login_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_logout":
            pass

        if btnName == "btn_register":
            widgets.stackedWidget.setCurrentWidget(widgets.register_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # 实时变化
    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
