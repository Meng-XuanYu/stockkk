from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout


class UserLogPage(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.setObjectName('user_log_page')
        self.setStyleSheet('background-color: rgb(40, 44, 52);')
        self.init_ui()

    def init_ui(self):
        # 设置主窗口的布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # 移除主布局的边距

        # 添加滚动区域
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollArea.setStyleSheet('''
                            QScrollArea {
                                background-color: transparent;
                                border-radius: 5px;
                            }
                        ''')
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')

        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName('scrollAreaLayout')
        self.scrollAreaLayout.setContentsMargins(10, 10, 10, 10)  # 设置滚动区域内部内容的边距
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        title_layout = QHBoxLayout()
        title_label = QLabel("账号登录历史记录")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
                            QLabel {
                                font-size: 16px;
                                font-weight: bold;
                                color: #9AB1D6; 
                                padding: 0px; 
                                border-radius: 5px; 
                                border: transparent;
                            }
                        """)
        title_layout.addStretch()  # 添加弹簧以居中标签
        title_layout.addWidget(title_label)
        title_layout.addStretch()  # 添加弹簧以居中标签
        self.scrollAreaLayout.addLayout(title_layout)

        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")
        self.add_history_record("2022-01-01 12:00:00", "登录成功")

        # 将滚动区域添加到主布局中
        main_layout.addWidget(self.scrollArea)
        self.setLayout(main_layout)

    def add_history_record(self, time, type):
        record_layout = QHBoxLayout()

        time_label = QLabel(time)
        time_label.setFixedWidth(200)
        time_label.setFixedHeight(30)

        type_label = QLabel(type)
        type_label.setFixedWidth(100)
        type_label.setFixedHeight(30)

        record_layout.addWidget(time_label)
        record_layout.addWidget(type_label)

        # 创建记录项的容器并设置边框
        record_layout_widget = QWidget()
        record_layout_widget.setLayout(record_layout)
        record_layout_widget.setStyleSheet("border: 2px solid #959493; "
                                           "border-radius: 5px;")
        type_label.setStyleSheet("QLabel { border: white; }")
        time_label.setStyleSheet("QLabel { border: white; }")
        self.scrollAreaLayout.addWidget(record_layout_widget)
