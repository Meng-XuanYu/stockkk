import os
from io import StringIO
import pandas as pd
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import main
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from interface.Interface import Interface
from interface.ChartType import ChartType
from pages.ChangePasswordPage import ChangePasswordPage
from pages.ChangeUsernamePage import ChangeUsernamePage
from pages.LoginPage import LoginPage
from pages.RegisterPage import RegisterPage
from pages.user_log_page import UserLogPage
from . import picture_generator
from .market_analysis_window import MarketAnalysisWindow
from .picture_window import ChartDisplayWindow
from .resources_rc import *
from data.Stock import Stock


class UIMainWindow(object):
    def __init__(self, interface=None):
        self.stock_data = None
        if interface is None:
            self.interface = Interface()
        else:
            self.interface = interface
        self.chart_display_windows = []  # 存储所有ChartDisplayWindow实例的列表

    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u'MainWindow')
        main_window.resize(1280, 720)
        main_window.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(main_window)
        self.styleSheet.setObjectName(u'styleSheet')
        font = QFont()
        font.setFamilies([u'Arial'])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)

        style_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'themes', 'styles.qss')
        with open(style_file_path, 'r') as f:
            self.styleSheet.setStyleSheet(f.read())

        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u'appMargins')
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u'bgApp')
        self.bgApp.setStyleSheet(u'')
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u'appLayout')
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u'leftMenuBg')
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u'topLogoInfo')
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u'topLogo')
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u'titleLeftApp')
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u'Arial'])
        font1.setPointSize(12)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u'titleLeftDescription')
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u'Arial'])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u'leftMenuFrame')
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u'verticalMenuLayout')
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u'toggleBox')
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u'toggleButton')
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(size_policy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u'background-image: url(:/icons/images/icons/icon_menu.png);')

        self.verticalLayout_4.addWidget(self.toggleButton)

        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u'topMenu')
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u'verticalLayout_8')
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u'btn_home')
        size_policy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(size_policy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-home.png);')

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_read_data = QPushButton(self.topMenu)
        self.btn_read_data.setObjectName(u'btn_read_data')
        size_policy.setHeightForWidth(self.btn_read_data.sizePolicy().hasHeightForWidth())
        self.btn_read_data.setSizePolicy(size_policy)
        self.btn_read_data.setMinimumSize(QSize(0, 45))
        self.btn_read_data.setFont(font)
        self.btn_read_data.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_read_data.setLayoutDirection(Qt.LeftToRight)
        self.btn_read_data.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-input.png);')

        self.verticalLayout_8.addWidget(self.btn_read_data)

        self.btn_picture = QPushButton(self.topMenu)
        self.btn_picture.setObjectName(u'btn_picture')
        size_policy.setHeightForWidth(self.btn_picture.sizePolicy().hasHeightForWidth())
        self.btn_picture.setSizePolicy(size_policy)
        self.btn_picture.setMinimumSize(QSize(0, 45))
        self.btn_picture.setFont(font)
        self.btn_picture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_picture.setLayoutDirection(Qt.LeftToRight)
        self.btn_picture.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-chart.png);')

        self.verticalLayout_8.addWidget(self.btn_picture)

        self.btn_history = QPushButton(self.topMenu)

        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u'bottomMenu')
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u'verticalLayout_9')
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggle_left_box = QPushButton(self.bottomMenu)
        self.toggle_left_box.setObjectName(u'toggleLeftBox')
        size_policy.setHeightForWidth(self.toggle_left_box.sizePolicy().hasHeightForWidth())
        self.toggle_left_box.setSizePolicy(size_policy)
        self.toggle_left_box.setMinimumSize(QSize(0, 45))
        self.toggle_left_box.setFont(font)
        self.toggle_left_box.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_left_box.setLayoutDirection(Qt.LeftToRight)
        self.toggle_left_box.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-heart.png);')

        self.verticalLayout_9.addWidget(self.toggle_left_box)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)

        self.verticalLayout_3.addWidget(self.leftMenuFrame)

        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u'extraLeftBox')
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u'extraColumLayout')
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u'extraTopBg')
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u'verticalLayout_5')
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u'extraTopLayout')
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u'extraIcon')
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u'extraLabel')
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u'extraCloseColumnBtn')
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u':/icons/images/icons/icon_close.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)

        self.verticalLayout_5.addLayout(self.extraTopLayout)

        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u'extraContent')
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u'verticalLayout_12')
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u'extraCenter')
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u'verticalLayout_10')
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u'textEdit')
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u'background: transparent;')
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)

        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u'extraBottom')
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)

        self.extraColumLayout.addWidget(self.extraContent)

        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u'contentBox')
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u'contentTopBg')
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u'leftBox')
        size_policy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        size_policy1.setHorizontalStretch(0)
        size_policy1.setVerticalStretch(0)
        size_policy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(size_policy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u'horizontalLayout_3')
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u'titleRightInfo')
        size_policy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        size_policy2.setHorizontalStretch(0)
        size_policy2.setVerticalStretch(0)
        size_policy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(size_policy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u'rightButtons')
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.userInfoLabel = QLabel(self.rightButtons)
        self.userInfoLabel.setObjectName(u'userInfoLabel')
        if self.interface.get_current_user() is not None:
            self.userInfoLabel.setText(f'当前用户: {self.interface.get_current_user().get_name()}')
        else:
            self.userInfoLabel.setText('当前未登录')
        self.userBtn = QPushButton(self.rightButtons)
        self.userBtn.setObjectName(u'userBtn')
        self.userBtn.setMinimumSize(QSize(28, 28))
        self.userBtn.setMaximumSize(QSize(28, 28))
        self.userBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u':/icons/images/icons/cil-user.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.userBtn.setIcon(icon1)
        self.userBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.userInfoLabel)
        self.horizontalLayout_2.addWidget(self.userBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u'minimizeAppBtn')
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u':/icons/images/icons/icon_minimize.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u'maximizeRestoreAppBtn')
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u'Arial'])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u':/icons/images/icons/icon_maximize.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u'closeAppBtn')
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)

        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u'contentBottom')
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u'verticalLayout_6')
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u'content')
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u'horizontalLayout_4')
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u'pagesContainer')
        self.pagesContainer.setStyleSheet(u'')
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u'verticalLayout_15')
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u'stackedWidget')
        self.stackedWidget.setStyleSheet(u'background: transparent;')

        # 主页页面
        self.home_page = QWidget()
        self.home_page.setObjectName(u'home')
        self.home_page.setStyleSheet(u'background-image: url(./images/images/stockkk_horizontal.jpg);\n'
                                     'background-position: center;\n'
                                     'background-repeat: no-repeat;')
        self.stackedWidget.addWidget(self.home_page)
        # --------------------------------------------------------------------------------
        # 读取数据页面
        self.read_data_page = QWidget()
        self.read_data_page.setObjectName(u'read_data_page')
        self.read_data_page.setStyleSheet(u'b')
        self.verticalLayout = QVBoxLayout(self.read_data_page)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.read_data_page)
        self.row_1.setObjectName(u'row_1')
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.row_1.setStyleSheet("border: none;")
        self.verticalLayout_16 = QVBoxLayout(self.row_1)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u'verticalLayout_16')
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.row_1)
        self.frame_div_content_1.setObjectName(u'frame_div_content_1')
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u'verticalLayout_17')
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u'frame_title_wid_1')
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setFont(font)
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u'labelBoxBlenderInstalation')
        self.labelBoxBlenderInstalation.setGeometry(QRect(10, 0, 1130, 24))
        self.labelBoxBlenderInstalation.setStyleSheet("color: #77E4C8;"
                                                      "font-size: 14px;")
        self.labelBoxBlenderInstalation.setTextFormat(Qt.AutoText)
        self.labelBoxBlenderInstalation.setWordWrap(False)
        self.labelBoxBlenderInstalation.setMargin(-1)
        self.labelBoxBlenderInstalation.setIndent(0)

        self.verticalLayout_17.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u'frame_content_wid_1')
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_9.setObjectName(u'horizontalLayout_9')
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u'gridLayout')
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.lineEdit = QLineEdit(self.frame_content_wid_1)
        self.lineEdit.setObjectName(u'lineEdit')
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u'background-color: rgb(33, 37, 43);')

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_content_wid_1)
        self.pushButton.setObjectName(u'pushButton')
        self.pushButton.setMinimumSize(QSize(150, 30))
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton.setStyleSheet(u'background-color: rgb(52, 59, 72);')
        icon4 = QIcon()
        icon4.addFile(u':/icons/images/icons/cil-folder-open.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon4)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.pushButton_all = QPushButton(self.frame_content_wid_1)
        self.pushButton_all.setObjectName(u'pushButton_all')
        self.pushButton_all.setMinimumSize(QSize(150, 30))
        self.pushButton_all.setFont(font)
        self.pushButton_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_all.setStyleSheet(u'background-color: rgb(52, 59, 72);')
        icon4 = QIcon()
        icon4.addFile(u':/icons/images/icons/cil-magnifying-glass.png', QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_all.setIcon(icon4)

        self.gridLayout.addWidget(self.pushButton_all, 0, 2, 1, 1)

        self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        self.labelVersion_3.setObjectName(u'labelVersion_3')
        self.labelVersion_3.setStyleSheet(u'color: rgb(113, 126, 149);')
        self.labelVersion_3.setLineWidth(1)
        self.labelVersion_3.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)

        self.horizontalLayout_9.addLayout(self.gridLayout)

        self.verticalLayout_17.addWidget(self.frame_content_wid_1)

        self.verticalLayout_16.addWidget(self.frame_div_content_1)

        self.verticalLayout.addWidget(self.row_1)

        self.row_3 = QFrame(self.read_data_page)
        self.row_3.setObjectName(u'row_3')
        self.row_3.setMinimumSize(QSize(0, 0))
        self.row_3.setFrameShape(QFrame.StyledPanel)
        self.row_3.setFrameShadow(QFrame.Raised)
        self.row_3.setStyleSheet("border: none;")
        self.horizontalLayout_13 = QHBoxLayout(self.row_3)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u'horizontalLayout_13')
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.row_4 = QFrame(self.read_data_page)
        self.row_4.setObjectName(u'row_4')
        self.row_4.setMinimumSize(QSize(0, 0))
        self.row_4.setFrameShape(QFrame.StyledPanel)
        self.row_4.setFrameShadow(QFrame.Raised)
        self.row_4.setStyleSheet("""
            QFrame {
                border: none;  /* 移除边框 */
            }
        """)
        self.horizontalLayout_14 = QHBoxLayout(self.row_4)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u'horizontalLayout_14')
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.row_2 = QFrame(self.read_data_page)
        self.row_2.setObjectName(u'row_2')
        self.row_2.setMinimumSize(QSize(0, 150))
        self.row_2.setFrameShape(QFrame.StyledPanel)
        self.row_2.setFrameShadow(QFrame.Raised)
        self.row_2.setStyleSheet("""
            QFrame {
                border: none;  /* 移除边框 */
            }
        """)
        self.horizontalLayout_12 = QHBoxLayout(self.row_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u'horizontalLayout_12')
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.row_2)
        if self.tableWidget.columnCount() < 10:
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
        font4.setFamilies([u'Arial'])
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font4)
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
        self.tableWidget.setObjectName(u'tableWidget')
        size_policy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(size_policy3)
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
        self.searchLineEdit.setObjectName('searchLineEdit')
        self.searchLineEdit.setPlaceholderText('输入股票代码搜索')
        self.searchLineEdit.setFixedSize(200, 30)  # 调整宽度和高度

        self.searchButton = QPushButton()
        self.searchButton.setObjectName('searchButton')
        self.searchButton.setText('显示数据')
        self.searchButton.setFixedSize(60, 30)  # 调整宽度和高度

        # 添加 errorLabel
        self.errorLabel = QLabel(self.read_data_page)
        self.errorLabel.setObjectName('errorLabel')
        self.errorLabel.setText('')
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setStyleSheet("color:#FFDE4D;"
                                      "font-size: 12px;")
        self.verticalLayout.addWidget(self.errorLabel)

        QMetaObject.connectSlotsByName(main_window)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        error_layout = QHBoxLayout()
        error_layout.setSpacing(0)
        error_layout.addWidget(self.errorLabel)

        # 将 searchLineEdit 和 searchButton 添加到这个水平布局中
        search_layout.addWidget(self.searchLineEdit)
        search_layout.addWidget(self.searchButton)
        # 添加弹簧以实现居中效果
        self.horizontalLayout_13.addStretch()
        self.horizontalLayout_13.addLayout(search_layout)
        self.horizontalLayout_13.addStretch()

        # 将这个水平布局添加到 row_3 中
        self.horizontalLayout_13.addLayout(search_layout)
        self.horizontalLayout_14.addLayout(error_layout)
        self.stackedWidget.addWidget(self.read_data_page)

        self.verticalLayout_15.addWidget(self.stackedWidget)

        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u'extraRightBox')
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u'verticalLayout_7')
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u'themeSettingsTopDetail')
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u'contentSettings')
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u'verticalLayout_13')
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u'topMenus')
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u'verticalLayout_14')
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)

        # 边栏按钮是否显示
        self.btn_login = QPushButton(self.topMenus)
        self.btn_register = QPushButton(self.topMenus)
        self.btn_logout = QPushButton(self.topMenus)
        self.btn_change_password = QPushButton(self.topMenus)
        self.btn_change_username = QPushButton(self.topMenus)
        self.btn_delete_user = QPushButton(self.topMenus)
        self.btn_delete_chart_history = QPushButton(self.topMenus)
        self.btn_delete_log_history = QPushButton(self.topMenus)

        if self.interface.get_current_user() is None:
            self.btn_login.setObjectName(u'btn_login')
            size_policy.setHeightForWidth(self.btn_login.sizePolicy().hasHeightForWidth())
            self.btn_login.setSizePolicy(size_policy)
            self.btn_login.setMinimumSize(QSize(0, 45))
            self.btn_login.setFont(font)
            self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_login.setLayoutDirection(Qt.LeftToRight)
            self.btn_login.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-user.png);')
            self.verticalLayout_14.addWidget(self.btn_login)

            self.btn_register.setObjectName(u'btn_register')
            size_policy.setHeightForWidth(self.btn_register.sizePolicy().hasHeightForWidth())
            self.btn_register.setSizePolicy(size_policy)
            self.btn_register.setMinimumSize(QSize(0, 45))
            self.btn_register.setFont(font)
            self.btn_register.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_register.setLayoutDirection(Qt.LeftToRight)
            self.btn_register.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-user-follow.png);')
            self.verticalLayout_14.addWidget(self.btn_register)

            self.btn_logout.hide()
            self.btn_change_password.hide()
            self.btn_change_username.hide()
            self.btn_delete_user.hide()
            self.btn_delete_chart_history.hide()
            self.btn_delete_log_history.hide()
            self.btn_history.hide()
        else:
            self.btn_change_password.setObjectName(u'btn_change_password')
            size_policy.setHeightForWidth(self.btn_change_password.sizePolicy().hasHeightForWidth())
            self.btn_change_password.setSizePolicy(size_policy)
            self.btn_change_password.setMinimumSize(QSize(0, 45))
            self.btn_change_password.setFont(font)
            self.btn_change_password.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_change_password.setLayoutDirection(Qt.LeftToRight)
            self.btn_change_password.setStyleSheet(
                u'background-image: url(:/icons/images/icons/cil-lock-unlocked.png);')
            self.verticalLayout_14.addWidget(self.btn_change_password)

            self.btn_change_username.setObjectName(u'btn_change_username')
            size_policy.setHeightForWidth(self.btn_change_username.sizePolicy().hasHeightForWidth())
            self.btn_change_username.setSizePolicy(size_policy)
            self.btn_change_username.setMinimumSize(QSize(0, 45))
            self.btn_change_username.setFont(font)
            self.btn_change_username.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_change_username.setLayoutDirection(Qt.LeftToRight)
            self.btn_change_username.setStyleSheet(
                u'background-image: url(:/icons/images/icons/cil-featured-playlist.png);')
            self.verticalLayout_14.addWidget(self.btn_change_username)

            self.btn_delete_chart_history.setObjectName(u'btn_delete_chart_history')
            size_policy.setHeightForWidth(self.btn_delete_chart_history.sizePolicy().hasHeightForWidth())
            self.btn_delete_chart_history.setSizePolicy(size_policy)
            self.btn_delete_chart_history.setMinimumSize(QSize(0, 45))
            self.btn_delete_chart_history.setFont(font)
            self.btn_delete_chart_history.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_delete_chart_history.setLayoutDirection(Qt.LeftToRight)
            self.btn_delete_chart_history.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-chart.png);')
            self.verticalLayout_14.addWidget(self.btn_delete_chart_history)

            self.btn_delete_log_history.setObjectName(u'btn_delete_log_history')
            size_policy.setHeightForWidth(self.btn_delete_log_history.sizePolicy().hasHeightForWidth())
            self.btn_delete_log_history.setSizePolicy(size_policy)
            self.btn_delete_log_history.setMinimumSize(QSize(0, 45))
            self.btn_delete_log_history.setFont(font)
            self.btn_delete_log_history.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_delete_log_history.setLayoutDirection(Qt.LeftToRight)
            self.btn_delete_log_history.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-notes.png);')
            self.verticalLayout_14.addWidget(self.btn_delete_log_history)

            self.btn_delete_user.setObjectName(u'btn_delete_user')
            size_policy.setHeightForWidth(self.btn_delete_user.sizePolicy().hasHeightForWidth())
            self.btn_delete_user.setSizePolicy(size_policy)
            self.btn_delete_user.setMinimumSize(QSize(0, 45))
            self.btn_delete_user.setFont(font)
            self.btn_delete_user.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_delete_user.setLayoutDirection(Qt.LeftToRight)
            self.btn_delete_user.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-user-unfollow.png);')
            self.verticalLayout_14.addWidget(self.btn_delete_user)

            self.btn_logout.setObjectName(u'btn_logout')
            size_policy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
            self.btn_logout.setSizePolicy(size_policy)
            self.btn_logout.setMinimumSize(QSize(0, 45))
            self.btn_logout.setFont(font)
            self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_logout.setLayoutDirection(Qt.LeftToRight)
            self.btn_logout.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-account-logout.png);')
            self.verticalLayout_14.addWidget(self.btn_logout)

            self.btn_history.setObjectName(u'btn_history')
            size_policy.setHeightForWidth(self.btn_history.sizePolicy().hasHeightForWidth())
            self.btn_history.setSizePolicy(size_policy)
            self.btn_history.setMinimumSize(QSize(0, 45))
            self.btn_history.setFont(font)
            self.btn_history.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_history.setLayoutDirection(Qt.LeftToRight)
            self.btn_history.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-save.png);')
            self.verticalLayout_8.addWidget(self.btn_history)

            self.btn_register.hide()
            self.btn_login.hide()

        self.btn_delete_cache = QPushButton(self.topMenu)
        self.btn_delete_cache.setObjectName(u'btn_delete_cache')
        size_policy.setHeightForWidth(self.btn_delete_cache.sizePolicy().hasHeightForWidth())
        self.btn_delete_cache.setSizePolicy(size_policy)
        self.btn_delete_cache.setMinimumSize(QSize(0, 45))
        self.btn_delete_cache.setFont(font)
        self.btn_delete_cache.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete_cache.setLayoutDirection(Qt.LeftToRight)
        self.btn_delete_cache.setStyleSheet(u'background-image: url(:/icons/images/icons/cil-x-circle.png);')

        self.verticalLayout_8.addWidget(self.btn_delete_cache)

        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)

        self.verticalLayout_7.addWidget(self.contentSettings)

        self.horizontalLayout_4.addWidget(self.extraRightBox)

        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u'bottomBar')
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u'horizontalLayout_5')
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u'creditsLabel')
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font5 = QFont()
        font5.setFamilies([u'Arial'])
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u'version')
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u'frame_size_grip')
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)

        self.verticalLayout_6.addWidget(self.bottomBar)

        self.verticalLayout_2.addWidget(self.contentBottom)

        self.appLayout.addWidget(self.contentBox)

        self.appMargins.addWidget(self.bgApp)

        main_window.setCentralWidget(self.styleSheet)

        QMetaObject.connectSlotsByName(main_window)

        # picture_page 区域
        self.picture_page = QWidget()
        self.picture_page.setObjectName(u'picture_page')
        self.verticalLayout_21 = QVBoxLayout(self.picture_page)
        self.verticalLayout_21.setObjectName(u'verticalLayout_21')
        self.verticalLayout_21.setContentsMargins(10, 10, 10, 10)
        # 添加 row_3 布局
        self.row_3_picture = QFrame(self.picture_page)
        self.row_3_picture.setObjectName(u'row_3_picture')
        self.row_3_picture.setFrameShape(QFrame.StyledPanel)
        self.row_3_picture.setFrameShadow(QFrame.Raised)
        self.row_3_picture.setStyleSheet("""
            QFrame {
                border: none;  /* 移除边框 */
            }
        """)
        self.horizontalLayout_15 = QHBoxLayout(self.row_3_picture)
        self.horizontalLayout_15.setObjectName(u'horizontalLayout_15')
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        # 添加搜索栏和按钮
        self.searchLineEdit_picture = QLineEdit()
        self.searchLineEdit_picture.setObjectName(u'searchLineEdit_picture')
        self.searchLineEdit_picture.setPlaceholderText('输入股票代码搜索')
        self.searchLineEdit_picture.setFixedSize(200, 30)
        self.searchButton_picture = QPushButton()
        self.searchButton_picture.setObjectName(u'searchButton_picture')
        self.searchButton_picture.setText('生成图片')
        self.searchButton_picture.setFixedSize(60, 30)
        # 添加图表类型选择栏
        self.chartTypeButton = QToolButton()
        self.chartTypeButton.setObjectName(u'chartTypeButton')
        self.chartTypeButton.setText('选择图表类型')
        self.chartTypeButton.setFixedSize(200, 30)
        self.chartTypeButton.setPopupMode(QToolButton.InstantPopup)
        # 创建图表类型菜单
        self.chartTypeMenu = QMenu(self.chartTypeButton)
        chart_types = ['开盘和收盘价格平均条形图', '总交易量条形图', '最高价格条形图',
                       '最低价格条形图', '复合增长条形图', '振幅散点图', '换手率条形图', 'K线图', '价格折线图', 'RSI图', 'MACD图']
        for chart_type in chart_types:
            action = self.chartTypeMenu.addAction(chart_type)
            action.triggered.connect(lambda checked, t=chart_type: self.chartTypeButton.setText(t))
        self.chartTypeButton.setMenu(self.chartTypeMenu)
        # 添加错误提示框
        search_layout_pic_page = QHBoxLayout()
        search_layout_pic_page.setSpacing(10)
        search_layout_pic_page.addWidget(self.searchLineEdit_picture)
        search_layout_pic_page.addWidget(self.chartTypeButton)
        search_layout_pic_page.addWidget(self.searchButton_picture)

        self.horizontalLayout_15.addStretch()
        self.horizontalLayout_15.addLayout(search_layout_pic_page)
        self.horizontalLayout_15.addStretch()

        # 添加 row_2 布局
        self.row_2_picture = QFrame(self.picture_page)
        self.row_2_picture.setObjectName(u'row_2_picture')
        self.row_2_picture.setFrameShape(QFrame.StyledPanel)
        self.row_2_picture.setFrameShadow(QFrame.Raised)
        self.row_2_picture.setStyleSheet("""
            QFrame {
                border: none;  /* 移除边框 */
            }
        """)
        self.horizontalLayout_16 = QHBoxLayout(self.row_2_picture)
        self.horizontalLayout_16.setObjectName(u'horizontalLayout_16')
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)

        # 添加滚动区域
        self.scrollArea = QScrollArea(self.row_2_picture)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(u'scrollArea')
        self.scrollArea.setStyleSheet('''
            QScrollArea {
                background-color: transparent;
                border-radius: 5px;
            }
        ''')

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u'scrollAreaWidgetContents')
        self.scrollAreaWidgetContents.setGeometry(0, 0, 600, 400)

        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName(u'scrollAreaLayout')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.title_layout = QHBoxLayout()
        if self.interface.get_current_user() is None:
            self.title_label = QLabel("可视化历史记录，登录后可使用该功能")
        else:
            self.title_label = QLabel("可视化历史记录")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedWidth(300)
        self.title_label.setFixedHeight(50)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #9AB1D6; 
                padding: 0px; 
                border-radius: 5px; 
                border: transparent;
            }
        """)
        self.title_layout.addStretch()  # 添加弹簧以居中标签
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()  # 添加弹簧以居中标签
        self.scrollAreaLayout.addLayout(self.title_layout)

        self.horizontalLayout_16.addWidget(self.scrollArea)

        self.load_chart_record()

        self.chartTypeButton.setStyleSheet('''
            QToolButton {
                background-color: transparent;
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                padding: 5px;
                color: rgb(221, 221, 221);
                font: 10pt 'Arial';
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
        ''')
        self.verticalLayout_21.addWidget(self.row_3_picture)
        self.verticalLayout_21.addWidget(self.row_2_picture)
        self.stackedWidget.addWidget(self.picture_page)

        # 前端功能区
        # 设置文件选择按钮和表格
        self.pushButton.clicked.connect(self.select_file)
        self.searchButton.clicked.connect(self.search_stock)
        self.searchButton_picture.clicked.connect(self.generate_chart)
        self.btn_delete_log_history.clicked.connect(self.delete_user_log_history)
        self.btn_delete_user.clicked.connect(self.delete_user)
        self.btn_delete_chart_history.clicked.connect(self.delete_user_chart_history)
        self.btn_delete_cache.clicked.connect(self.delete_cache)
        self.pushButton_all.clicked.connect(self.market_analysis)

        # 页面
        self.register_page = RegisterPage(self.interface)
        self.login_page = LoginPage(self.interface)
        self.stackedWidget.addWidget(self.login_page)
        self.stackedWidget.addWidget(self.register_page)

        self.change_password_page = ChangePasswordPage(self.interface)
        self.stackedWidget.addWidget(self.change_password_page)

        self.change_username_page = ChangeUsernamePage(self.interface)
        self.stackedWidget.addWidget(self.change_username_page)

        self.user_log_page = UserLogPage(self.interface)
        self.stackedWidget.addWidget(self.user_log_page)

        # 最后的处理
        self.retranslate_ui(main_window)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, '选择文件', '',
                                                   'Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)',
                                                   options=options)
        if file_path:
            self.load_data(file_path)  # 这里仍然传递文件路径，因为load_data需要完整路径

    def load_data(self, file_path):
        import pandas as pd

        if file_path.endswith('.xlsx'):
            self.stock_data = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            self.stock_data = pd.read_csv(file_path)
        else:
            information_box = QMessageBox()
            information_box.setIcon(QMessageBox.Warning)
            icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
            information_box.setIconPixmap(icon_pixmap)
            information_box.setText("导入数据类型错误，请选择正确的类型")
            information_box.setWindowTitle("导入失败")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()
            return
        information_box = QMessageBox()
        information_box.setIcon(QMessageBox.Warning)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        information_box.setIconPixmap(icon_pixmap)
        information_box.setText("导入股市数据成功！")
        information_box.setWindowTitle("导入成功")
        information_box.setStandardButtons(QMessageBox.Ok)
        information_box.exec_()

        self.errorLabel.setText('可以在下面表格中查看导入数据的特定代码股票数据')
        file_name = os.path.basename(file_path)
        self.interface.set_file_name(file_name)
        self.lineEdit.setText(file_path)

        self.stock_data['日期'] = pd.to_datetime(self.stock_data['日期']).dt.strftime('%Y-%m-%d')
        self.interface.import_data_frame(self.stock_data)

    def search_stock(self):
        stock_code = self.searchLineEdit.text()
        if stock_code:
            try:
                filtered_data = self.interface.search_stock_by_code(stock_code)
                self.display_data(filtered_data.get_data_frame())
                self.errorLabel.setText(f'搜索成功：{stock_code}, 请在数据表格中查看数据')
                self.errorLabel.setStyleSheet('color: #58b368;'
                                              'font-size: 12px;')
            except StockDataNotFoundException:
                self.errorLabel.setText('未导入股票数据，请先导入数据')
                self.errorLabel.setStyleSheet('color: #fb7756;'
                                              'font-size: 12px;')
            except StockCodeNotFoundException:
                self.errorLabel.setText(f'未找到股票代码：{stock_code}')
                self.errorLabel.setStyleSheet('color: #fb7756;'
                                              'font-size: 12px;')
        else:
            self.errorLabel.setStyleSheet('color: #dad873;'
                                          'font-size: 12px;')
            self.errorLabel.setText('请输入股票代码')

    def display_data(self, data):
        self.tableWidget.setRowCount(len(data) + 1)
        self.tableWidget.setColumnCount(len(data.columns))
        self.tableWidget.setHorizontalHeaderLabels(data.columns)

        # 填充数据
        for row in range(len(data)):
            for col in range(len(data.columns)):
                self.tableWidget.setItem(row + 1, col, QTableWidgetItem(str(data.iat[row, col])))

    def retranslate_ui(self, main_window):
        self.btn_picture.setText(QCoreApplication.translate('MainWindow', u'单股聚焦', None))

        # 小组件名称
        main_window.setWindowTitle(QCoreApplication.translate('MainWindow', u'MainWindow', None))
        self.titleLeftApp.setText(QCoreApplication.translate('MainWindow', u'股市📈小助手', None))
        self.titleLeftDescription.setText(QCoreApplication.translate('MainWindow', u'股市数据可视化 / 分析评估', None))
        self.toggleButton.setText(QCoreApplication.translate('MainWindow', u'隐藏', None))
        self.btn_home.setText(QCoreApplication.translate('MainWindow', u'主页', None))
        self.btn_read_data.setText(QCoreApplication.translate('MainWindow', u'读取数据', None))
        self.btn_delete_cache.setText(QCoreApplication.translate('MainWindow', u'清除缓存', None))
        self.btn_history.setText(QCoreApplication.translate('MainWindow', u'用户登录历史记录', None))
        self.toggle_left_box.setText(QCoreApplication.translate('MainWindow', u'爱心提示', None))
        self.extraLabel.setText(QCoreApplication.translate('MainWindow', u'爱心提示', None))
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate('MainWindow', u'收起爱心提示', None))
        self.extraCloseColumnBtn.setText('')
        self.textEdit.setHtml(QCoreApplication.translate('MainWindow',
                                                         u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                                                         '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                                                         'p, li { white-space: pre-wrap; }\n'
                                                         'hr { height: 1px; border-width: 0; }\n'
                                                         'li.unchecked::marker { content: "\\2610"; }\n'
                                                         'li.checked::marker { content: "\\2612"; }\n'
                                                         '</style></head><body style=" font-family:\'Arial\'; font-size:10pt; font-weight:400; font-style:normal;">\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600; color:#ff79c6;">功能简介</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;">1.股票数据的导入、分析和相关指标的计算</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;">2.股票数据与相关指标通过各类图表进行可视化</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;">3.各类图表实现鼠标交互，支持查看数值、拖动图表、放大缩小等多种交互功能</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;">4.基于本地数据库的多用户注册、登录与管理</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;">5.基于本地数据库的用户登录记录与图表生成历史存储</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#bd93f9;">项目地址：https://github.com/Meng-XuanYu/stockkk</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600; color:#ff79c6;">使用小tips</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; color:#ffffff;">1.记得先导入数据</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; color:#ffffff;">2.保留缓存，可以加载图片更快</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; color:#ffffff;">3.注册账号后可以使用历史记录功能哦，查看更方便快捷</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size9pt; color:#ffffff;">4.可以点击左工具栏上面第一个展开左侧工具栏，查看每个按钮对应名称</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin左:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; font-weight:600; color:#ff79c6;">注意事项</span></p>\n'
                                                         '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin右:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; color:red;">请确保导入的数据中包含了所需图像的信息</span></p></body></html>',
                                                         None))
        self.titleRightInfo.setText(
            QCoreApplication.translate('MainWindow', u'Stock APP - Stock market data visualizer and analysis tool.',
                                       None))
        self.userBtn.setToolTip(QCoreApplication.translate('MainWindow', u'用户系统', None))
        self.userBtn.setText('')
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate('MainWindow', u'最小化', None))
        self.minimizeAppBtn.setText('')
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate('MainWindow', u'最大化', None))
        self.maximizeRestoreAppBtn.setText('')
        self.closeAppBtn.setToolTip(QCoreApplication.translate('MainWindow', u'关闭', None))
        self.closeAppBtn.setText('')
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate('MainWindow', u'选取文件', None))
        self.lineEdit.setText('')
        self.lineEdit.setPlaceholderText(
            QCoreApplication.translate('MainWindow', u'点击右侧按钮选择文件', None))
        self.pushButton.setText(QCoreApplication.translate('MainWindow', u'选取', None))
        self.pushButton_all.setText(QCoreApplication.translate('MainWindow', u'大盘分析', None))
        self.labelVersion_3.setText(
            QCoreApplication.translate('MainWindow', u'请选取股市信息文件，各类表格文件均可', None))
        ___qtablewidgetitem26 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate('MainWindow', u'\u80a1\u7968\u4ee3\u7801', None))
        ___qtablewidgetitem27 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate('MainWindow', u'\u65e5\u671f', None))
        ___qtablewidgetitem28 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem28.setText(QCoreApplication.translate('MainWindow', u'\u5f00\u76d8\u4ef7', None))
        ___qtablewidgetitem29 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem29.setText(QCoreApplication.translate('MainWindow', u'\u6536\u76d8\u4ef7', None))
        ___qtablewidgetitem30 = self.tableWidget.item(0, 4)
        ___qtablewidgetitem30.setText(QCoreApplication.translate('MainWindow', u'\u6700\u9ad8\u4ef7', None))
        ___qtablewidgetitem31 = self.tableWidget.item(0, 5)
        ___qtablewidgetitem31.setText(QCoreApplication.translate('MainWindow', u'\u6700\u4f4e\u4ef7', None))
        ___qtablewidgetitem32 = self.tableWidget.item(0, 6)
        ___qtablewidgetitem32.setText(QCoreApplication.translate('MainWindow', u'\u4ea4\u6613\u91cf', None))
        ___qtablewidgetitem33 = self.tableWidget.item(0, 7)
        ___qtablewidgetitem33.setText(QCoreApplication.translate('MainWindow', u'\u6da8\u8dcc\u5e45', None))
        ___qtablewidgetitem34 = self.tableWidget.item(0, 8)
        ___qtablewidgetitem34.setText(QCoreApplication.translate('MainWindow', u'\u632f\u5e45', None))
        ___qtablewidgetitem35 = self.tableWidget.item(0, 9)
        ___qtablewidgetitem35.setText(QCoreApplication.translate('MainWindow', u'\u6362\u624b\u7387', None))
        if self.interface.get_current_user() is None:
            self.btn_login.setText(QCoreApplication.translate('MainWindow', u'\u7528\u6237\u767b\u5f55', None))
            self.btn_register.setText(QCoreApplication.translate('MainWindow', u'\u7528\u6237\u6ce8\u518c', None))
        else:
            self.btn_logout.setText(QCoreApplication.translate('MainWindow', u'\u9000\u51fa\u767b\u5f55', None))
            self.btn_change_password.setText(QCoreApplication.translate('MainWindow', u'修改密码', None))
            self.btn_change_username.setText(QCoreApplication.translate('MainWindow', u'修改用户名', None))
            self.btn_delete_user.setText(QCoreApplication.translate('MainWindow', u'注销账号', None))
            self.btn_delete_chart_history.setText(QCoreApplication.translate('MainWindow', u'清除图片记录', None))
            self.btn_delete_log_history.setText(QCoreApplication.translate('MainWindow', u'清除登录记录', None))
        self.creditsLabel.setText(QCoreApplication.translate('MainWindow', u'By: XuanYu_Master', None))
        self.version.setText(QCoreApplication.translate('MainWindow', u'v2.0.0', None))

    def delete_user_log_history(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.setText("确定要删除登录历史记录吗？")
        msg_box.setWindowTitle("确认删除")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            self.interface.get_current_user().clear_log_records()

    def delete_user_chart_history(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.setText("确定要删除图表记录吗？")
        msg_box.setWindowTitle("确认清除")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            self.interface.get_current_user().clear_chart_records()
            self.clear_all_history_records()

    def delete_user(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.setText("确定要注销账号吗？")
        msg_box.setWindowTitle("确认注销")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            self.interface.user_delete()
            self.new_main_window = main.MainWindow(self.interface)
            self.interface.change_window(self.new_main_window)
            self.new_main_window.show()

    def delete_cache(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.setText("确定要清除缓存吗？")
        msg_box.setWindowTitle("确认清除")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            self.interface.delete_log_history()
            self.interface.delete_chart_history()

    def market_analysis(self):
        information_box = QMessageBox()
        information_box.setIcon(QMessageBox.Warning)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        information_box.setIconPixmap(icon_pixmap)
        try:
            market_analysis_window = MarketAnalysisWindow(self.interface)
            market_analysis_window.show()
            information_box.setText("如果是首次生成图片，请耐心等待")
            information_box.setWindowTitle("大盘分析成功")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()
        except StockDataNotFoundException:
            information_box.setText("未导入股票数据，请先导入数据")
            information_box.setWindowTitle("大盘分析失败")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()

    def generate_chart(self):
        stock_code = self.searchLineEdit_picture.text()
        information_box = QMessageBox()
        information_box.setIcon(QMessageBox.Warning)
        icon_pixmap = QPixmap('images/images/stockkk.jpg').scaled(64, 64)
        information_box.setIconPixmap(icon_pixmap)

        if stock_code:
            try:
                stock = self.interface.search_stock_by_code(stock_code)
                chart_type_text = self.chartTypeButton.text()

                # 根据选择的图表类型生成相应的图表
                if chart_type_text == '选择图表类型':
                    information_box.setText("请先选择图表类型")
                    information_box.setWindowTitle("生成失败")
                    information_box.setStandardButtons(QMessageBox.Ok)
                    information_box.exec_()
                else:
                    chart_html = picture_generator.create_chart(stock,
                                                                ChartType.get_chart_type_from_text(chart_type_text))
                    new_chart_window = ChartDisplayWindow(chart_html, stock)
                    new_chart_window.show()
                    self.chart_display_windows.append(new_chart_window)
                    information_box.setText("如果是首次生成图片，请耐心等待")
                    information_box.setWindowTitle("生成成功")
                    information_box.setStandardButtons(QMessageBox.Ok)
                    information_box.exec_()
                    user = self.interface.get_current_user()
                    if user is not None:
                        chart_record = user.get_lastest_chart()
                        self.add_history_record(chart_record['store_time'], chart_record['file_name'],
                                                chart_record['stock_code'],
                                                ChartType.get_back_chart_type_name(chart_record['chart_type']))
            except StockDataNotFoundException:
                information_box.setText("请先导入股票数据")
                information_box.setWindowTitle("生成失败")
                information_box.setStandardButtons(QMessageBox.Ok)
                information_box.exec_()
            except StockCodeNotFoundException:
                information_box.setText("请输入正确的股票代码")
                information_box.setWindowTitle("生成失败")
                information_box.setStandardButtons(QMessageBox.Ok)
                information_box.exec_()
        else:
            information_box.setText("请先输入股票代码")
            information_box.setWindowTitle("生成失败")
            information_box.setStandardButtons(QMessageBox.Ok)
            information_box.exec_()

    def load_chart_record(self):
        user = self.interface.get_current_user()
        if user:
            chart_records = user.get_chart_records()
            for chart_record in chart_records:
                self.add_history_record(chart_record['store_time'], chart_record['file_name'],
                                        chart_record['stock_code'],
                                        ChartType.get_back_chart_type_name(chart_record['chart_type']))

    def add_history_record(self, date, file_name, stock_code, chart_type):
        record_layout = QHBoxLayout()

        date_label = QLabel(date.strftime('%Y-%m-%d %H:%M:%S'))
        date_label.setFixedWidth(200)
        date_label.setFixedHeight(30)

        file_label = QLabel(file_name)
        file_label.setFixedWidth(200)
        file_label.setFixedHeight(30)

        stock_label = QLabel(stock_code)
        stock_label.setFixedWidth(100)
        stock_label.setFixedHeight(30)

        chart_label = QLabel(chart_type)
        chart_label.setFixedWidth(200)
        chart_label.setFixedHeight(30)

        view_button = QPushButton("查询")
        view_button.setFixedWidth(60)
        view_button.setFixedHeight(30)
        view_button.clicked.connect(lambda: self.on_view_button_clicked(date, stock_code))

        record_layout.addWidget(date_label)
        record_layout.addWidget(file_label)
        record_layout.addWidget(stock_label)
        record_layout.addWidget(chart_label)
        record_layout.addWidget(view_button)

        # 创建记录项的容器并设置边框
        record_layout_widget = QWidget()
        record_layout_widget.setLayout(record_layout)
        record_layout_widget.setStyleSheet("border: 2px solid #959493; "
                                           "border-radius: 5px;")
        record_layout_widget.setFixedHeight(60)
        date_label.setStyleSheet("QLabel { border: white; }")
        file_label.setStyleSheet("QLabel { border: white; }")
        stock_label.setStyleSheet("QLabel { border: white; }")
        chart_label.setStyleSheet("QLabel { border: white; }")
        view_button.setStyleSheet('''
            QPushButton {
                background-color: rgb(52, 59, 72);
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                padding: 5px;
                color: rgb(221, 221, 221);
            }
            QPushButton:hover {
                background-color: rgb(61, 70, 86);
                border: 2px solid rgb(61, 70, 86);
            }
            QPushButton:pressed {
                background-color: rgb(43, 50, 61);
                border: 2px solid rgb(43, 50, 61);
            }''')
        self.scrollAreaLayout.insertWidget(1, record_layout_widget, alignment=Qt.AlignTop)

    def on_view_button_clicked(self, date_time, stock_code):
        chart_and_data = self.interface.get_current_user().get_chart_and_data_in_records(date_time)
        chart_html = chart_and_data['chart']
        stock_data = pd.read_json(StringIO(chart_and_data['stock_data']))
        new_chart_window = ChartDisplayWindow(chart_html, Stock(self.interface, stock_code, stock_data))
        new_chart_window.show()
        self.chart_display_windows.append(new_chart_window)

    def clear_all_history_records(self):
        while self.scrollAreaLayout.count():
            item = self.scrollAreaLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.title_layout.count():
            item = self.title_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("可视化历史记录")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedWidth(300)
        self.title_label.setFixedHeight(50)
        self.title_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #9AB1D6; 
                        padding: 0px; 
                        border-radius: 5px; 
                        border: transparent;
                    }
                """)
        self.title_layout.addStretch()  # 添加弹簧以居中标签
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()  # 添加弹簧以居中标签
        self.scrollAreaLayout.addLayout(self.title_layout)
