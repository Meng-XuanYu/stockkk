from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *

from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from interface.Interface import Interface
from pages.LoginPage import LoginPage
from pages.RegisterPage import RegisterPage
from .resources_rc import *
from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Scatter, Line, Grid
from pyecharts.globals import CurrentConfig, ThemeType


class Ui_MainWindow(object):
    def __init__(self):
        self.stock_data = None
        self.interface = Interface(self)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"\n"
                                      "\n"
                                      "QWidget{\n"
                                      "	color: rgb(221, 221, 221);\n"
                                      "	font: 10pt \"Arial\";\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Tooltip */\n"
                                      "QToolTip {\n"
                                      "	color: #ffffff;\n"
                                      "	background-color: rgba(33, 37, 43, 180);\n"
                                      "	border: 1px solid rgb(44, 49, 58);\n"
                                      "	background-image: none;\n"
                                      "	background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 2px solid rgb(255, 121, 198);\n"
                                      "	text-align: left;\n"
                                      "	padding-left: 8px;\n"
                                      "	margin: 0px;\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Bg App */\n"
                                      "#bgApp {	\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "	border: 1px solid rgb(44, 49, 58);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Left Menu */\n"
                                      "#leftMenuBg {	\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "}\n"
                                      "#topLogo {\n"
                                      "	background-"
                                      "color: rgb(33, 37, 43);\n"
                                      "	background-image: url(./images/images/stockkk_top.jpg);\n"
                                      "	background-position: centered;\n"
                                      "	background-repeat: no-repeat;\n"
                                      " height: 10px;\n"
                                      " width: 10px;\n"
                                      "}\n"
                                      "#titleLeftApp { font: 63 12pt \"Arial\"; }\n"
                                      "#titleLeftDescription { font: 8pt \"Arial\"; color: rgb(189, 147, 249); }\n"
                                      "\n"
                                      "/* MENUS */\n"
                                      "#topMenu .QPushButton {	\n"
                                      "	background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 22px solid transparent;\n"
                                      "	background-color: transparent;\n"
                                      "	text-align: left;\n"
                                      "	padding-left: 44px;\n"
                                      "}\n"
                                      "#topMenu .QPushButton:hover {\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "}\n"
                                      "#topMenu .QPushButton:pressed {	\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "	color: rgb(255, 255, 255);\n"
                                      "}\n"
                                      "#bottomMenu .QPushButton {	\n"
                                      "	background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 20px solid transparent;\n"
                                      "	background-color:transparent;\n"
                                      "	text-align: left;\n"
                                      "	padding-l"
                                      "eft: 44px;\n"
                                      "}\n"
                                      "#bottomMenu .QPushButton:hover {\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "}\n"
                                      "#bottomMenu .QPushButton:pressed {	\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "	color: rgb(255, 255, 255);\n"
                                      "}\n"
                                      "#leftMenuFrame{\n"
                                      "	border-top: 3px solid rgb(44, 49, 58);\n"
                                      "}\n"
                                      "\n"
                                      "/* Toggle Button */\n"
                                      "#toggleButton {\n"
                                      "	background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 20px solid transparent;\n"
                                      "	background-color: rgb(37, 41, 48);\n"
                                      "	text-align: left;\n"
                                      "	padding-left: 44px;\n"
                                      "	color: rgb(113, 126, 149);\n"
                                      "}\n"
                                      "#toggleButton:hover {\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "}\n"
                                      "#toggleButton:pressed {\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "}\n"
                                      "\n"
                                      "/* Title Menu */\n"
                                      "#titleRightInfo { padding-left: 10px; }\n"
                                      "\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Extra Tab */\n"
                                      "#extraLeftBox {	\n"
                                      "	background-color: rgb(44, 49, 58);\n"
                                      "}\n"
                                      ""
                                      "#extraTopBg{	\n"
                                      "	background-color: rgb(189, 147, 249)\n"
                                      "}\n"
                                      "\n"
                                      "/* Icon */\n"
                                      "#extraIcon {\n"
                                      "	background-position: center;\n"
                                      "	background-repeat: no-repeat;\n"
                                      "	background-image: url(:/icons/images/icons/cil-heart.png);\n"
                                      "}\n"
                                      "\n"
                                      "/* Label */\n"
                                      "#extraLabel { color: rgb(255, 255, 255); }\n"
                                      "\n"
                                      "/* Btn Close */\n"
                                      "#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
                                      "#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
                                      "#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
                                      "\n"
                                      "/* Extra Content */\n"
                                      "#extraContent{\n"
                                      "	border-top: 3px solid rgb(40, 44, 52);\n"
                                      "}\n"
                                      "\n"
                                      "/* Extra Top Menus */\n"
                                      "#extraTopMenu .QPushButton {\n"
                                      "background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 22px solid transparent;\n"
                                      "	background-color:transparent;\n"
                                      "	text-align: lef"
                                      "t;\n"
                                      "	padding-left: 44px;\n"
                                      "}\n"
                                      "#extraTopMenu .QPushButton:hover {\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "}\n"
                                      "#extraTopMenu .QPushButton:pressed {	\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "	color: rgb(255, 255, 255);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Content App */\n"
                                      "#contentTopBg{	\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "}\n"
                                      "#contentBottom{\n"
                                      "	border-top: 3px solid rgb(44, 49, 58);\n"
                                      "}\n"
                                      "\n"
                                      "/* Top Buttons */\n"
                                      "#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
                                      "#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
                                      "#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
                                      "\n"
                                      "/* Theme Settings */\n"
                                      "#extraRightBox { background-color: rgb(44, 49, 58); }\n"
                                      "#themeSettingsTopDetail { background-color: rgb(189"
                                      ", 147, 249); }\n"
                                      "\n"
                                      "/* Bottom Bar */\n"
                                      "#bottomBar { background-color: rgb(44, 49, 58); }\n"
                                      "#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
                                      "\n"
                                      "/* CONTENT SETTINGS */\n"
                                      "/* MENUS */\n"
                                      "#contentSettings .QPushButton {	\n"
                                      "	background-position: left center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "	border: none;\n"
                                      "	border-left: 22px solid transparent;\n"
                                      "	background-color:transparent;\n"
                                      "	text-align: left;\n"
                                      "	padding-left: 44px;\n"
                                      "}\n"
                                      "#contentSettings .QPushButton:hover {\n"
                                      "	background-color: rgb(40, 44, 52);\n"
                                      "}\n"
                                      "#contentSettings .QPushButton:pressed {	\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "	color: rgb(255, 255, 255);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "QTableWidget */\n"
                                      "QTableWidget {	\n"
                                      "	background-color: transparent;\n"
                                      "	padding: 10px;\n"
                                      "	border-radius: 5px;\n"
                                      "	gridline-color: rgb(44, 49, 58);\n"
                                      ""
                                      "	border-bottom: 1px solid rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QTableWidget::item{\n"
                                      "	border-color: rgb(44, 49, 60);\n"
                                      "	padding-left: 5px;\n"
                                      "	padding-right: 5px;\n"
                                      "	gridline-color: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QTableWidget::item:selected{\n"
                                      "	background-color: rgb(189, 147, 249);\n"
                                      "}\n"
                                      "QHeaderView::section{\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "	max-width: 30px;\n"
                                      "	border: 1px solid rgb(44, 49, 58);\n"
                                      "	border-style: none;\n"
                                      "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                                      "    border-right: 1px solid rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QTableWidget::horizontalHeader {	\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "}\n"
                                      "QHeaderView::section:horizontal\n"
                                      "{\n"
                                      "    border: 1px solid rgb(33, 37, 43);\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "	padding: 3px;\n"
                                      "	border-top-left-radius: 7px;\n"
                                      "    border-top-right-radius: 7px;\n"
                                      "}\n"
                                      "QHeaderView::section:vertical\n"
                                      "{\n"
                                      "    border: 1px solid rgb(44, 49, 60);\n"
                                      "}\n"
                                      "\n"
                                      "/* ////////////////////////////////////////////////////////////////////////////"
                                      "/////////////////////\n"
                                      "LineEdit */\n"
                                      "QLineEdit {\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "	border-radius: 5px;\n"
                                      "	border: 2px solid rgb(33, 37, 43);\n"
                                      "	padding-left: 10px;\n"
                                      "	selection-color: rgb(255, 255, 255);\n"
                                      "	selection-background-color: rgb(255, 121, 198);\n"
                                      "}\n"
                                      "QLineEdit:hover {\n"
                                      "	border: 2px solid rgb(64, 71, 88);\n"
                                      "}\n"
                                      "QLineEdit:focus {\n"
                                      "	border: 2px solid rgb(91, 101, 124);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "PlainTextEdit */\n"
                                      "QPlainTextEdit {\n"
                                      "	background-color: rgb(27, 29, 35);\n"
                                      "	border-radius: 5px;\n"
                                      "	padding: 10px;\n"
                                      "	selection-color: rgb(255, 255, 255);\n"
                                      "	selection-background-color: rgb(255, 121, 198);\n"
                                      "}\n"
                                      "QPlainTextEdit  QScrollBar:vertical {\n"
                                      "    width: 8px;\n"
                                      " }\n"
                                      "QPlainTextEdit  QScrollBar:horizontal {\n"
                                      "    height: 8px;\n"
                                      " }\n"
                                      "QPlainTextEdit:hover {\n"
                                      "	border: 2px solid rgb(64, 71, 88);\n"
                                      "}\n"
                                      "QPlainTextEdit:focus {\n"
                                      "	border: 2px solid "
                                      "rgb(91, 101, 124);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "ScrollBars */\n"
                                      "QScrollBar:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    height: 8px;\n"
                                      "    margin: 0px 21px 0 21px;\n"
                                      "	border-radius: 0px;\n"
                                      "}\n"
                                      "QScrollBar::handle:horizontal {\n"
                                      "    background: rgb(189, 147, 249);\n"
                                      "    min-width: 25px;\n"
                                      "	border-radius: 4px\n"
                                      "}\n"
                                      "QScrollBar::add-line:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "    width: 20px;\n"
                                      "	border-top-right-radius: 4px;\n"
                                      "    border-bottom-right-radius: 4px;\n"
                                      "    subcontrol-position: right;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::sub-line:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "    width: 20px;\n"
                                      "	border-top-left-radius: 4px;\n"
                                      "    border-bottom-left-radius: 4px;\n"
                                      "    subcontrol-position: left;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::up-arrow:horiz"
                                      "ontal, QScrollBar::down-arrow:horizontal\n"
                                      "{\n"
                                      "     background: none;\n"
                                      "}\n"
                                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
                                      "{\n"
                                      "     background: none;\n"
                                      "}\n"
                                      " QScrollBar:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    width: 8px;\n"
                                      "    margin: 21px 0 21px 0;\n"
                                      "	border-radius: 0px;\n"
                                      " }\n"
                                      " QScrollBar::handle:vertical {	\n"
                                      "	background: rgb(189, 147, 249);\n"
                                      "    min-height: 25px;\n"
                                      "	border-radius: 4px\n"
                                      " }\n"
                                      " QScrollBar::add-line:vertical {\n"
                                      "     border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "     height: 20px;\n"
                                      "	border-bottom-left-radius: 4px;\n"
                                      "    border-bottom-right-radius: 4px;\n"
                                      "     subcontrol-position: bottom;\n"
                                      "     subcontrol-origin: margin;\n"
                                      " }\n"
                                      " QScrollBar::sub-line:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "     height: 20px;\n"
                                      "	border-top-left-radius: 4px;\n"
                                      "    border-top-right-radius: 4px;\n"
                                      "     subcontrol-position: top;\n"
                                      "     subcontrol-origin: margin;\n"
                                      ""
                                      " }\n"
                                      " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                      "     background: none;\n"
                                      " }\n"
                                      "\n"
                                      " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                      "     background: none;\n"
                                      " }\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "CheckBox */\n"
                                      "QCheckBox::indicator {\n"
                                      "    border: 3px solid rgb(52, 59, 72);\n"
                                      "	width: 15px;\n"
                                      "	height: 15px;\n"
                                      "	border-radius: 10px;\n"
                                      "    background: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QCheckBox::indicator:hover {\n"
                                      "    border: 3px solid rgb(58, 66, 81);\n"
                                      "}\n"
                                      "QCheckBox::indicator:checked {\n"
                                      "    background: 3px solid rgb(52, 59, 72);\n"
                                      "	border: 3px solid rgb(52, 59, 72);	\n"
                                      "	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "RadioButton */\n"
                                      "QRadioButton::indicator {\n"
                                      "    border: 3px solid rgb(52, 59, 72);\n"
                                      "	width: 15px;\n"
                                      "	heigh"
                                      "t: 15px;\n"
                                      "	border-radius: 10px;\n"
                                      "    background: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QRadioButton::indicator:hover {\n"
                                      "    border: 3px solid rgb(58, 66, 81);\n"
                                      "}\n"
                                      "QRadioButton::indicator:checked {\n"
                                      "    background: 3px solid rgb(94, 106, 130);\n"
                                      "	border: 3px solid rgb(52, 59, 72);	\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "ComboBox */\n"
                                      "QComboBox{\n"
                                      "	background-color: rgb(27, 29, 35);\n"
                                      "	border-radius: 5px;\n"
                                      "	border: 2px solid rgb(33, 37, 43);\n"
                                      "	padding: 5px;\n"
                                      "	padding-left: 10px;\n"
                                      "}\n"
                                      "QComboBox:hover{\n"
                                      "	border: 2px solid rgb(64, 71, 88);\n"
                                      "}\n"
                                      "QComboBox::drop-down {\n"
                                      "	subcontrol-origin: padding;\n"
                                      "	subcontrol-position: top right;\n"
                                      "	width: 25px; \n"
                                      "	border-left-width: 3px;\n"
                                      "	border-left-color: rgba(39, 44, 54, 150);\n"
                                      "	border-left-style: solid;\n"
                                      "	border-top-right-radius: 3px;\n"
                                      "	border-bottom-right-radius: 3px;	\n"
                                      "	background-image: url(:/icons/images/icons/cil-arrow-bottom.png"
                                      ");\n"
                                      "	background-position: center;\n"
                                      "	background-repeat: no-reperat;\n"
                                      " }\n"
                                      "QComboBox QAbstractItemView {\n"
                                      "	color: rgb(255, 121, 198);	\n"
                                      "	background-color: rgb(33, 37, 43);\n"
                                      "	padding: 10px;\n"
                                      "	selection-background-color: rgb(39, 44, 54);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Sliders */\n"
                                      "QSlider::groove:horizontal {\n"
                                      "    border-radius: 5px;\n"
                                      "    height: 10px;\n"
                                      "	margin: 0px;\n"
                                      "	background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "QSlider::groove:horizontal:hover {\n"
                                      "	background-color: rgb(55, 62, 76);\n"
                                      "}\n"
                                      "QSlider::handle:horizontal {\n"
                                      "    background-color: rgb(189, 147, 249);\n"
                                      "    border: none;\n"
                                      "    height: 10px;\n"
                                      "    width: 10px;\n"
                                      "    margin: 0px;\n"
                                      "	border-radius: 5px;\n"
                                      "}\n"
                                      "QSlider::handle:horizontal:hover {\n"
                                      "    background-color: rgb(195, 155, 255);\n"
                                      "}\n"
                                      "QSlider::handle:horizontal:pressed {\n"
                                      "    background-color: rgb(255, 121, 198);\n"
                                      "}\n"
                                      "\n"
                                      "QSlider::groove:"
                                      "vertical {\n"
                                      "    border-radius: 5px;\n"
                                      "    width: 10px;\n"
                                      "    margin: 0px;\n"
                                      "	background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "QSlider::groove:vertical:hover {\n"
                                      "	background-color: rgb(55, 62, 76);\n"
                                      "}\n"
                                      "QSlider::handle:vertical {\n"
                                      "    background-color: rgb(189, 147, 249);\n"
                                      "	border: none;\n"
                                      "    height: 10px;\n"
                                      "    width: 10px;\n"
                                      "    margin: 0px;\n"
                                      "	border-radius: 5px;\n"
                                      "}\n"
                                      "QSlider::handle:vertical:hover {\n"
                                      "    background-color: rgb(195, 155, 255);\n"
                                      "}\n"
                                      "QSlider::handle:vertical:pressed {\n"
                                      "    background-color: rgb(255, 121, 198);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "CommandLinkButton */\n"
                                      "QCommandLinkButton {	\n"
                                      "	color: rgb(255, 121, 198);\n"
                                      "	border-radius: 5px;\n"
                                      "	padding: 5px;\n"
                                      "	color: rgb(255, 170, 255);\n"
                                      "}\n"
                                      "QCommandLinkButton:hover {	\n"
                                      "	color: rgb(255, 170, 255);\n"
                                      "	background-color: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QCommandLinkButton:pressed {	\n"
                                      "	color: rgb(189, 147,"
                                      " 249);\n"
                                      "	background-color: rgb(52, 58, 71);\n"
                                      "}\n"
                                      "\n"
                                      "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
                                      "Button */\n"
                                      "#pagesContainer QPushButton {\n"
                                      "	border: 2px solid rgb(52, 59, 72);\n"
                                      "	border-radius: 5px;	\n"
                                      "	background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "#pagesContainer QPushButton:hover {\n"
                                      "	background-color: rgb(57, 65, 80);\n"
                                      "	border: 2px solid rgb(61, 70, 86);\n"
                                      "}\n"
                                      "#pagesContainer QPushButton:pressed {	\n"
                                      "	background-color: rgb(35, 40, 49);\n"
                                      "	border: 2px solid rgb(43, 50, 61);\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)

        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_read_data = QPushButton(self.topMenu)
        self.btn_read_data.setObjectName(u"btn_read_data")
        sizePolicy.setHeightForWidth(self.btn_read_data.sizePolicy().hasHeightForWidth())
        self.btn_read_data.setSizePolicy(sizePolicy)
        self.btn_read_data.setMinimumSize(QSize(0, 45))
        self.btn_read_data.setFont(font)
        self.btn_read_data.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_read_data.setLayoutDirection(Qt.LeftToRight)
        self.btn_read_data.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-input.png);")

        self.verticalLayout_8.addWidget(self.btn_read_data)

        self.btn_picture = QPushButton(self.topMenu)
        self.btn_picture.setObjectName(u"btn_picture")
        sizePolicy.setHeightForWidth(self.btn_picture.sizePolicy().hasHeightForWidth())
        self.btn_picture.setSizePolicy(sizePolicy)
        self.btn_picture.setMinimumSize(QSize(0, 45))
        self.btn_picture.setFont(font)
        self.btn_picture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_picture.setLayoutDirection(Qt.LeftToRight)
        self.btn_picture.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-chart.png);")

        self.verticalLayout_8.addWidget(self.btn_picture)

        self.btn_history = QPushButton(self.topMenu)
        self.btn_history.setObjectName(u"btn_history")
        sizePolicy.setHeightForWidth(self.btn_history.sizePolicy().hasHeightForWidth())
        self.btn_history.setSizePolicy(sizePolicy)
        self.btn_history.setMinimumSize(QSize(0, 45))
        self.btn_history.setFont(font)
        self.btn_history.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_history.setLayoutDirection(Qt.LeftToRight)
        self.btn_history.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-save.png)")

        self.verticalLayout_8.addWidget(self.btn_history)

        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-heart.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)

        self.verticalLayout_3.addWidget(self.leftMenuFrame)

        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)

        self.verticalLayout_5.addLayout(self.extraTopLayout)

        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)

        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)

        self.extraColumLayout.addWidget(self.extraContent)

        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.userBtn = QPushButton(self.rightButtons)
        self.userBtn.setObjectName(u"userBtn")
        self.userBtn.setMinimumSize(QSize(28, 28))
        self.userBtn.setMaximumSize(QSize(28, 28))
        self.userBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.userBtn.setIcon(icon1)
        self.userBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.userBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)

        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")



        # 主页页面
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home")
        self.home_page.setStyleSheet(u"background-image: url(./images/images/stockkk_horizontal.jpg);\n"
                                "background-position: center;\n"
                                "background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home_page)
        # 读取数据页面
        self.read_data_page = QWidget()
        self.read_data_page.setObjectName(u"read_data_page")
        self.read_data_page.setStyleSheet(u"b")
        self.verticalLayout = QVBoxLayout(self.read_data_page)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.read_data_page)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.row_1)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.row_1)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setFont(font)
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setGeometry(QRect(10, 0, 1130, 24))
        self.labelBoxBlenderInstalation.setFont(font)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")
        self.labelBoxBlenderInstalation.setTextFormat(Qt.AutoText)
        self.labelBoxBlenderInstalation.setWordWrap(False)
        self.labelBoxBlenderInstalation.setMargin(-1)
        self.labelBoxBlenderInstalation.setIndent(0)

        self.verticalLayout_17.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.lineEdit = QLineEdit(self.frame_content_wid_1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_content_wid_1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 30))
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon4)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        self.labelVersion_3.setObjectName(u"labelVersion_3")
        self.labelVersion_3.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_3.setLineWidth(1)
        self.labelVersion_3.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)

        self.horizontalLayout_9.addLayout(self.gridLayout)

        self.verticalLayout_17.addWidget(self.frame_content_wid_1)

        self.verticalLayout_16.addWidget(self.frame_div_content_1)

        self.verticalLayout.addWidget(self.row_1)

        self.row_3 = QFrame(self.read_data_page)
        self.row_3.setObjectName(u"row_3")
        self.row_3.setMinimumSize(QSize(0, 0))
        self.row_3.setFrameShape(QFrame.StyledPanel)
        self.row_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.row_3)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.row_4 = QFrame(self.read_data_page)
        self.row_4.setObjectName(u"row_4")
        self.row_4.setMinimumSize(QSize(0, 0))
        self.row_4.setFrameShape(QFrame.StyledPanel)
        self.row_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.row_4)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.row_2 = QFrame(self.read_data_page)
        self.row_2.setObjectName(u"row_2")
        self.row_2.setMinimumSize(QSize(0, 150))
        self.row_2.setFrameShape(QFrame.StyledPanel)
        self.row_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.row_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.row_2)
        if (self.tableWidget.columnCount() < 10):
            self.tableWidget.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if self.tableWidget.rowCount() < 16:
            self.tableWidget.setRowCount(16)
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font4);
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget.setItem(0, 4, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget.setItem(0, 5, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget.setItem(0, 6, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget.setItem(0, 7, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget.setItem(0, 8, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget.setItem(0, 9, __qtablewidgetitem35)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy3)
        palette = QPalette()
        brush = QBrush(QColor(221, 221, 221, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
        self.tableWidget.setPalette(palette)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_12.addWidget(self.tableWidget)

        self.verticalLayout.addWidget(self.row_4)
        self.verticalLayout.addWidget(self.row_3)
        self.verticalLayout.addWidget(self.row_2)

        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLineEdit.setPlaceholderText("输入股票代码搜索")
        self.searchLineEdit.setFixedSize(200, 30)  # 调整宽度和高度

        self.searchButton = QPushButton()
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("显示数据")
        self.searchButton.setFixedSize(60, 30)  # 调整宽度和高度

        # 添加 errorLabel
        self.errorLabel = QLabel(self.read_data_page)
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setText("")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.errorLabel)

        QMetaObject.connectSlotsByName(MainWindow)

        searchLayout = QHBoxLayout()
        searchLayout.setSpacing(10)

        errorLayout = QHBoxLayout()
        errorLayout.setSpacing(0)
        errorLayout.addWidget(self.errorLabel)
        self.stackedWidget.addWidget(self.read_data_page)



        self.verticalLayout_15.addWidget(self.stackedWidget)

        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.btn_login = QPushButton(self.topMenus)
        self.btn_login.setObjectName(u"btn_login")
        sizePolicy.setHeightForWidth(self.btn_login.sizePolicy().hasHeightForWidth())
        self.btn_login.setSizePolicy(sizePolicy)
        self.btn_login.setMinimumSize(QSize(0, 45))
        self.btn_login.setFont(font)
        self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_login.setLayoutDirection(Qt.LeftToRight)
        self.btn_login.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-user.png);")

        self.verticalLayout_14.addWidget(self.btn_login)

        self.btn_register = QPushButton(self.topMenus)
        self.btn_register.setObjectName(u"btn_register")
        sizePolicy.setHeightForWidth(self.btn_register.sizePolicy().hasHeightForWidth())
        self.btn_register.setSizePolicy(sizePolicy)
        self.btn_register.setMinimumSize(QSize(0, 45))
        self.btn_register.setFont(font)
        self.btn_register.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_register.setLayoutDirection(Qt.LeftToRight)
        self.btn_register.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-user-follow.png);")

        self.verticalLayout_14.addWidget(self.btn_register)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)

        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)

        self.verticalLayout_7.addWidget(self.contentSettings)

        self.horizontalLayout_4.addWidget(self.extraRightBox)

        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)

        self.verticalLayout_6.addWidget(self.bottomBar)

        self.verticalLayout_2.addWidget(self.contentBottom)

        self.appLayout.addWidget(self.contentBox)

        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        QMetaObject.connectSlotsByName(MainWindow)



        # picture_page 区域
        self.picture_page = QWidget()
        self.picture_page.setObjectName(u"picture_page")
        self.verticalLayout_21 = QVBoxLayout(self.picture_page)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(10, 10, 10, 10)
        # 添加 row_3 布局
        self.row_3_picture = QFrame(self.picture_page)
        self.row_3_picture.setObjectName(u"row_3_picture")
        self.row_3_picture.setFrameShape(QFrame.StyledPanel)
        self.row_3_picture.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.row_3_picture)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        # 添加搜索栏和按钮
        self.searchLineEdit_picture = QLineEdit()
        self.searchLineEdit_picture.setObjectName(u"searchLineEdit_picture")
        self.searchLineEdit_picture.setPlaceholderText("输入股票代码搜索")
        self.searchLineEdit_picture.setFixedSize(200, 30)
        self.searchButton_picture = QPushButton()
        self.searchButton_picture.setObjectName(u"searchButton_picture")
        self.searchButton_picture.setText("生成图片")
        self.searchButton_picture.setFixedSize(60, 30)
        # 添加图表类型选择栏
        self.chartTypeButton = QToolButton()
        self.chartTypeButton.setObjectName(u"chartTypeButton")
        self.chartTypeButton.setText("选择图表类型")
        self.chartTypeButton.setFixedSize(200, 30)
        self.chartTypeButton.setPopupMode(QToolButton.InstantPopup)
        # 创建图表类型菜单
        self.chartTypeMenu = QMenu(self.chartTypeButton)
        chart_types = ['开盘和收盘价格平均条形图', '总交易量条形图', '最高价格条形图',
                       '最低价格条形图', '复合增长条形图', '振幅散点图', '换手率条形图', 'K线图']
        for chart_type in chart_types:
            action = self.chartTypeMenu.addAction(chart_type)
            action.triggered.connect(lambda checked, t=chart_type: self.chartTypeButton.setText(t))
        self.chartTypeButton.setMenu(self.chartTypeMenu)
        # 添加错误提示框
        self.errorLabel_picpage = QLabel()
        self.errorLabel_picpage.setObjectName("errorLabel")
        self.errorLabel_picpage.setText("")
        self.errorLabel_picpage.setFixedSize(200, 30)
        self.errorLabel_picpage.setAlignment(Qt.AlignCenter)
        searchLayout_picpage = QHBoxLayout()
        searchLayout_picpage.setSpacing(10)
        searchLayout_picpage.addWidget(self.searchLineEdit_picture)
        searchLayout_picpage.addWidget(self.chartTypeButton)
        searchLayout_picpage.addWidget(self.searchButton_picture)
        searchLayout_picpage.addWidget(self.errorLabel_picpage)

        self.horizontalLayout_15.addStretch()
        self.horizontalLayout_15.addLayout(searchLayout_picpage)
        self.horizontalLayout_15.addStretch()

        # 添加 row_2 布局
        self.row_2_picture = QFrame(self.picture_page)
        self.row_2_picture.setObjectName(u"row_2_picture")
        self.row_2_picture.setFrameShape(QFrame.StyledPanel)
        self.row_2_picture.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)

        # 添加图像显示框
        self.webEngineView = QWebEngineView()
        self.webEngineView.setObjectName(u"webEngineView")
        self.horizontalLayout_16.addWidget(self.webEngineView)

        self.webEngineView.setMinimumSize(QSize(800, 600))

        self.chartTypeButton.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                padding: 5px;
                color: rgb(221, 221, 221);
                font: 10pt "Arial";
            }
            QToolButton:hover {
                background-color: rgb(61, 70, 86);
                border: 2px solid rgb(61, 70, 86);
            }
            QToolButton:pressed {
                background-color: rgb(43, 50, 61);
                border: 2px solid rgb(43, 50, 61);
            }
            QToolButton::menu-indicator {
                image: none;
            }
            QMenu {
                background-color: rgb(52, 59, 72);
                border: 1px solid rgb(44, 49, 58);
                color: rgb(221, 221, 221);
            }
            QMenu::item:selected {
                background-color: rgb(61, 70, 86);
            }
        """)
        self.verticalLayout_21.addWidget(self.row_3_picture)
        self.verticalLayout_21.addWidget(self.row_2_picture)
        self.stackedWidget.addWidget(self.picture_page)

        # 前端功能区
        # 设置文件选择按钮和表格
        self.pushButton.clicked.connect(self.select_file)
        self.searchButton.clicked.connect(self.search_stock)
        self.searchButton_picture.clicked.connect(self.generate_chart)

        # 登录注册页面
        self.register_page = RegisterPage()
        self.login_page = LoginPage()
        self.stackedWidget.addWidget(self.login_page)
        self.stackedWidget.addWidget(self.register_page)

        # 最后的处理
        self.retranslateUi(MainWindow)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "选择文件", "",
                                                   "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_name:
            self.lineEdit.setText(file_name)
            self.load_data(file_name)

    def select_chart_type(self, chart_type):
        self.chartTypeButton.setText(chart_type)

    def load_data(self, file_name):
        import pandas as pd

        if file_name.endswith('.xlsx'):
            self.stock_data = pd.read_excel(file_name)
        elif file_name.endswith('.csv'):
            self.stock_data = pd.read_csv(file_name)
        else:
            return

        self.stock_data['日期'] = pd.to_datetime(self.stock_data['日期']).dt.strftime('%Y-%m-%d')
        self.interface.import_data_frame(self.stock_data)

    def search_stock(self):
        stock_code = self.searchLineEdit.text()
        if stock_code:
            try:
                filtered_data = self.interface.search_stock_by_code(stock_code)
                self.display_data(filtered_data.get_data_frame())
                self.errorLabel.setText(f'搜索成功：{stock_code}, 请在数据表格中查看数据')
                self.errorLabel.setStyleSheet("color: #58b368;")
            except StockDataNotFoundException:
                self.errorLabel.setText('未导入股票数据，请先导入数据')
                self.errorLabel.setStyleSheet("color: #fb7756;")
            except StockCodeNotFoundException:
                self.errorLabel.setText(f'未找到股票代码：{stock_code}')
                self.errorLabel.setStyleSheet("color: #fb7756;")
        else:
            self.errorLabel.setStyleSheet("color: #dad873;")
            self.errorLabel.setText('请输入股票代码')

    def display_data(self, data):
        self.tableWidget.setRowCount(len(data) + 1)
        self.tableWidget.setColumnCount(len(data.columns))
        self.tableWidget.setHorizontalHeaderLabels(data.columns)

        # 填充数据
        for row in range(len(data)):
            for col in range(len(data.columns)):
                self.tableWidget.setItem(row + 1, col, QTableWidgetItem(str(data.iat[row, col])))

    # setupUi

    def generate_chart(self):
        stock_code = self.searchLineEdit_picture.text()
        if stock_code:
            try:
                filtered_data = self.interface.search_stock_by_code(stock_code)
                chart_type = self.chartTypeButton.text()

                # 根据选择的图表类型生成相应的图表
                if chart_type == '选择图表类型':
                    self.errorLabel_picpage.setText('未选择图表类型')
                    self.errorLabel_picpage.setStyleSheet("color: #fb7756;")
                else:
                    if chart_type == '开盘和收盘价格平均条形图':
                        chart_html = self.create_open_close_chart(filtered_data.get_data_frame())
                    elif chart_type == '总交易量条形图':
                        chart_html = self.create_total_volume_chart(filtered_data.get_data_frame())
                    elif chart_type == '最高价格条形图':
                        chart_html = self.create_high_price_chart(filtered_data.get_data_frame())
                    elif chart_type == '最低价格条形图':
                        chart_html = self.create_low_price_chart(filtered_data.get_data_frame())
                    elif chart_type == '复合增长条形图':
                        chart_html = self.create_compound_growth_chart(filtered_data.get_data_frame())
                    elif chart_type == '振幅散点图':
                        chart_html = self.create_amplitude_scatter_chart(filtered_data.get_data_frame())
                    elif chart_type == '换手率条形图':
                        chart_html = self.create_turnover_rate_chart(filtered_data.get_data_frame())
                    elif chart_type == 'K线图':
                        chart_html = self.create_Kline_chart(filtered_data.get_data_frame())
                    self.errorLabel_picpage.setText('图片生成成功')
                    self.errorLabel_picpage.setStyleSheet("color: #58b368;")
                    self.webEngineView.setHtml(chart_html)
            except StockDataNotFoundException:
                self.errorLabel_picpage.setText('未导入股票数据，请先导入数据')
                self.errorLabel_picpage.setStyleSheet("color: #fb7756;")
            except StockCodeNotFoundException:
                self.errorLabel_picpage.setText('未找到' f'未找到股票代码：{stock_code}')
                self.errorLabel_picpage.setStyleSheet("color: #fb7756;")
        else:
            self.errorLabel_picpage.setStyleSheet("color: #dad873;")
            self.errorLabel_picpage.setText('请先输入股票代码')

    def create_open_close_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        open_prices = stock_data['开盘价'].tolist()
        close_prices = stock_data['收盘价'].tolist()

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))  # 设置响应式布局
        bar.add_xaxis(dates)
        bar.add_yaxis("开盘价", open_prices, label_opts=opts.LabelOpts(is_show=False))  # 不显示数值
        bar.add_yaxis("收盘价", close_prices, label_opts=opts.LabelOpts(is_show=False))  # 不显示数值
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="开盘和收盘价格平均条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return bar.render_embed()

    def create_total_volume_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        volumes = stock_data['交易量'].tolist()

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        bar.add_xaxis(dates)
        bar.add_yaxis("交易量", volumes, label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="总交易量条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return bar.render_embed()

    def create_high_price_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        high_prices = stock_data['最高价'].tolist()

        line = Line(
            init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        line.add_xaxis(dates)
        line.add_yaxis("最高价", high_prices, label_opts=opts.LabelOpts(is_show=False))
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="最高价格条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),

            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return line.render_embed()

    def create_low_price_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        low_prices = stock_data['最低价'].tolist()

        line = Line(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        line.add_xaxis(dates)
        line.add_yaxis("最低价", low_prices, label_opts=opts.LabelOpts(is_show=False))
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="最低价格条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return line.render_embed()

    def create_compound_growth_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        growths = stock_data['涨跌幅'].tolist()

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        bar.add_xaxis(dates)
        bar.add_yaxis("涨跌幅", growths, label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="复合增长条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return bar.render_embed()

    def create_amplitude_scatter_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        amplitudes = stock_data['振幅'].tolist()

        scatter = Scatter(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        scatter.add_xaxis(dates)
        scatter.add_yaxis("振幅", amplitudes, label_opts=opts.LabelOpts(is_show=False))
        scatter.set_global_opts(
            title_opts=opts.TitleOpts(title="振幅散点图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return scatter.render_embed()

    def create_turnover_rate_chart(self, stock_data):
        dates = stock_data['日期'].tolist()
        turnover_rates = stock_data['换手率'].tolist()

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        bar.add_xaxis(dates)
        bar.add_yaxis("换手率", turnover_rates, label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="换手率条形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),

            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        return bar.render_embed()

    def create_Kline_chart(self, stock_data):
        dates = stock_data['日期'].tolist()

        kline = Kline(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        kline.add_xaxis(dates)
        kline.add_yaxis(
            "K线图",
            stock_data[['开盘价', '收盘价', '最高价', '最低价']].values.tolist(),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值")]
            ),
        )

        ma10 = stock_data['收盘价'].rolling(window=10).mean().dropna()
        start_date = ma10.index[0]

        line_ma10 = Line()
        line_ma10.add_xaxis(dates[start_date:])
        line_ma10.add_yaxis(
            "MA10",
            ma10.tolist(),
            is_smooth=True,
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )
        line_ma10.set_global_opts(legend_opts=opts.LegendOpts(pos_left="right"))

        ma20 = stock_data['收盘价'].rolling(window=20, min_periods=1).mean().dropna()
        line_ma20 = Line()
        line_ma20.add_xaxis(dates[start_date:])
        line_ma20.add_yaxis(
            "MA20",
            ma20.tolist(),
            is_smooth=True,
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )

        kline.set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title="K线图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={"dataZoom": {"yAxisIndex": "none"}})
        )

        kline.overlap(line_ma10)
        kline.overlap(line_ma20)

        grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500%"))
        grid.add(
            kline,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", height="60%"),
        )

        return kline.render_embed()

    # 已经精简很多了

    def retranslateUi(self, MainWindow):
        self.btn_picture.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u53ef\u89c6\u5316", None))

        # 小组件名称
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"股市📈小助手", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"股市数据可视化 / 分析评估", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"隐藏", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"主页", None))
        self.btn_read_data.setText(QCoreApplication.translate("MainWindow", u"读取数据", None))
        self.btn_history.setText(QCoreApplication.translate("MainWindow", u"历史记录", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"使用帮助", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"使用帮助", None))
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"收起使用帮助", None))
        self.extraCloseColumnBtn.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow",
                                                         u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                         "p, li { white-space: pre-wrap; }\n"
                                                         "hr { height: 1px; border-width: 0; }\n"
                                                         "li.unchecked::marker { content: \"\\2610\"; }\n"
                                                         "li.checked::marker { content: \"\\2612\"; }\n"
                                                         "</style></head><body style=\" font-family:'Arial'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Stockkk</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">可以让yxs别叫</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-le"
                                                         "ft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: XuanYu_Master</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert UI</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-uic main.ui(已弃用 &gt; ui_main.py</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert QRC</span></p>\n"
                                                         "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\""
                                                         ">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>",
                                                         None))
        self.titleRightInfo.setText(
            QCoreApplication.translate("MainWindow", u"Stock APP - Stock market data visualizer and analysis tool.",
                                       None))
        self.userBtn.setToolTip(QCoreApplication.translate("MainWindow", u"用户系统", None))
        self.userBtn.setText("")
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"最小化", None))
        self.minimizeAppBtn.setText("")
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"最大化", None))
        self.maximizeRestoreAppBtn.setText("")
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"关闭", None))
        self.closeAppBtn.setText("")
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"选取文件", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"点击右侧按钮选择文件", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"选取", None))
        self.labelVersion_3.setText(
            QCoreApplication.translate("MainWindow", u"请选取股市信息文件，各类表格文件均可", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"4", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"6", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"7", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"8", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"9", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem20 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem21 = self.tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem22 = self.tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem23 = self.tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem24 = self.tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem25 = self.tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem26 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"\u80a1\u7968\u4ee3\u7801", None));
        ___qtablewidgetitem27 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u671f", None));
        ___qtablewidgetitem28 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u76d8\u4ef7", None));
        ___qtablewidgetitem29 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"\u6536\u76d8\u4ef7", None));
        ___qtablewidgetitem30 = self.tableWidget.item(0, 4)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u4ef7", None));
        ___qtablewidgetitem31 = self.tableWidget.item(0, 5)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"\u6700\u4f4e\u4ef7", None));
        ___qtablewidgetitem32 = self.tableWidget.item(0, 6)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"\u4ea4\u6613\u91cf", None));
        ___qtablewidgetitem33 = self.tableWidget.item(0, 7)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"\u6da8\u8dcc\u5e45", None));
        ___qtablewidgetitem34 = self.tableWidget.item(0, 8)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"\u632f\u5e45", None));
        ___qtablewidgetitem35 = self.tableWidget.item(0, 9)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"\u6362\u624b\u7387", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.btn_login.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u767b\u5f55", None))
        self.btn_register.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u6ce8\u518c", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa\u767b\u5f55", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: XuanYu_Master", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v0.8.1", None))
