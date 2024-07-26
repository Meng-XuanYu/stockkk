from io import StringIO

import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLineEdit, QPushButton, QToolButton, QMenu, QScrollArea, QLabel, QWidget
from PyQt5.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from data.Stock import Stock
from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from interface.ChartType import ChartType
from modules import picture_generator
from modules.picture_window import ChartDisplayWindow


class PicturePage(QWidget):
    def __init__(self, interface, stackedWidget):
        super().__init__()
        self.interface = interface
        self.stackedWidget = stackedWidget
        self.initUI()

    def initUI(self):
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
                       '最低价格条形图', '复合增长条形图', '振幅散点图', '换手率条形图', 'K线图', '价格折线图', 'RSI图',
                       'MACD图']
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

        self.searchButton_picture.clicked.connect(self.generate_chart)

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
