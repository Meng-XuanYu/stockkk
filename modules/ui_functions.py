# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class UIFunctions(MainWindow):
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if not status:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip('Restore')
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u':/icons/images/icons/icon_restore.png'))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip('Maximize')
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u':/icons/images/icons/icon_maximize.png'))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def return_status(self):
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def set_status(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggle_menu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            max_extend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                width_extended = max_extend
            else:
                width_extended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b'minimumWidth')
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(width_extended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    # noinspection DuplicatedCode
    def toggle_left_box(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            width_right_box = self.ui.extraRightBox.width()
            max_extend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.toggle_left_box.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                width_extended = max_extend
                # SELECT BTN
                self.ui.toggle_left_box.setStyleSheet(style + color)
                if width_right_box != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                width_extended = standard
                # RESET BTN
                self.ui.toggle_left_box.setStyleSheet(style.replace(color, ''))

        UIFunctions.start_box_animation(self, width, width_right_box, 'left')

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    # noinspection DuplicatedCode
    def toggle_right_box(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraRightBox.width()
            width_left_box = self.ui.extraLeftBox.width()
            max_extend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.userBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                width_extended = max_extend
                self.ui.userBtn.setStyleSheet(style + color)
                if width_left_box != 0:
                    style = self.ui.toggle_left_box.styleSheet()
                    self.ui.toggle_left_box.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                width_extended = standard
                # RESET BTN
                self.ui.userBtn.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(self, width_left_box, width, 'right')

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0

        # Check values
        if left_box_width == 0 and direction == 'left':
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == 'right':
            right_width = 240
        else:
            right_width = 0

            # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b'minimumWidth')
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b'minimumWidth')
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def select_menu(get_style):
        select = get_style + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselect_menu(get_style):
        deselect = get_style.replace(Settings.MENU_SELECTED_STYLESHEET, '')
        return deselect

    # START SELECTION
    def select_standard_menu(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.select_menu(w.styleSheet()))

    # RESET SELECTION
    def reset_style(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselect_menu(w.styleSheet()))

        for w in self.ui.topMenus.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselect_menu(w.styleSheet()))

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def ui_definitions(self):
        def double_click_maximize_restore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        self.ui.titleRightInfo.mouseDoubleClickEvent = double_click_maximize_restore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def move_window(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.return_status(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

            self.ui.titleRightInfo.mouseMoveEvent = move_window

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet('width: 20px; height: 20px; margin 0px; padding: 0px;')

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)
