from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLineEdit, QLabel,
                             QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget,
                             QAction, QTableView, QStatusBar, QProgressBar, QComboBox, QTabWidget, QDialog, QMenu)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from .change_password_dialog import ChangePasswordDialog
from .change_username_dialog import ChangeUsernameDialog
from .register_dialog import RegisterDialog
import pandas as pd

from interface.Interface import Interface
from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from exceptions.StockDataNotFoundException import StockDataNotFoundException


class MainWindow(QMainWindow):
    def __init__(self, interface, user):
        super().__init__()
        self.interface = interface
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('股市数据可视化与分析工具')
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('stock_icon.png'))

        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.statusBar.addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        # 菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        account_menu = menubar.addMenu('账户')

        open_action = QAction('打开', self)
        open_action.triggered.connect(lambda: self.choose_file(False))
        file_menu.addAction(open_action)

        default_open_action = QAction('默认打开', self)
        default_open_action.triggered.connect(lambda: self.choose_file(True))
        file_menu.addAction(default_open_action)

        register_action = QAction('注册', self)
        register_action.triggered.connect(self.show_register_dialog)
        account_menu.addAction(register_action)

        # 创建一个子菜单
        change_info_menu = QMenu('修改信息', self)
        account_menu.addMenu(change_info_menu)

        # 在子菜单中添加修改用户名和修改密码的选项
        change_username_action = QAction('修改用户名', self)
        change_username_action.triggered.connect(self.show_change_username_dialog)
        change_info_menu.addAction(change_username_action)

        change_password_action = QAction('修改密码', self)
        change_password_action.triggered.connect(self.show_change_password_dialog)
        change_info_menu.addAction(change_password_action)

        exit_action = QAction('退出登录', self)
        exit_action.triggered.connect(self.show_login_dialog_and_close)
        account_menu.addAction(exit_action)

        # 中央窗口小部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # 文件选择布局
        file_layout = QHBoxLayout()
        self.choose_file_btn = QPushButton('选择Excel文件', self)
        self.choose_file_btn.setFont(QFont('Arial', 12))
        self.choose_file_btn.clicked.connect(lambda: self.choose_file(False))
        file_layout.addWidget(self.choose_file_btn)

        self.file_label = QLabel('未选择文件', self)
        self.file_label.setFont(QFont('Arial', 12))
        file_layout.addWidget(self.file_label)

        main_layout.addLayout(file_layout)

        # 搜索布局
        search_layout = QHBoxLayout()
        self.search_label = QLabel('搜索股票代码:', self)
        self.search_label.setFont(QFont('Arial', 12))
        search_layout.addWidget(self.search_label)

        self.search_entry = QLineEdit(self)
        self.search_entry.setFont(QFont('Arial', 12))
        search_layout.addWidget(self.search_entry)

        self.search_btn = QPushButton('搜索', self)
        self.search_btn.setFont(QFont('Arial', 12))
        self.search_btn.clicked.connect(self.search_stock)
        search_layout.addWidget(self.search_btn)

        main_layout.addLayout(search_layout)

        # 图表选择布局
        chart_layout = QHBoxLayout()
        self.chart_label = QLabel('选择图表类型:', self)
        self.chart_label.setFont(QFont('Arial', 12))
        chart_layout.addWidget(self.chart_label)

        self.chart_combo = QComboBox(self)
        self.chart_combo.setFont(QFont('Arial', 12))
        self.chart_combo.addItems(['开盘和收盘价格平均条形图', '总交易量条形图', '最高价格条形图',
                                   '最低价格条形图', '复合增长条形图', '振幅散点图', '换手率条形图'])
        chart_layout.addWidget(self.chart_combo)

        self.generate_chart_btn = QPushButton('生成图表', self)
        self.generate_chart_btn.setFont(QFont('Arial', 12))
        self.generate_chart_btn.clicked.connect(self.generate_chart)
        chart_layout.addWidget(self.generate_chart_btn)

        main_layout.addLayout(chart_layout)

        # 选项卡布局
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont('Arial', 12))

        self.preview_tab = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_label = QLabel('预览区', self)
        self.preview_label.setFont(QFont('Arial', 12))
        self.preview_label.setStyleSheet('background-color: lightgray; border: 1px solid #ccc;')
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedHeight(300)
        self.preview_layout.addWidget(self.preview_label)
        self.preview_tab.setLayout(self.preview_layout)
        self.tab_widget.addTab(self.preview_tab, '预览')

        self.data_tab = QWidget()
        self.data_layout = QVBoxLayout()
        self.data_table = QTableView(self)
        self.data_layout.addWidget(self.data_table)
        self.data_tab.setLayout(self.data_layout)
        self.tab_widget.addTab(self.data_tab, '数据表格')

        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_table = QTableView(self)
        self.history_layout.addWidget(self.history_table)
        self.history_tab.setLayout(self.history_layout)
        self.tab_widget.addTab(self.history_tab, '历史记录')

        main_layout.addWidget(self.tab_widget)

        central_widget.setLayout(main_layout)

    def choose_file(self, default):
        if default:
            try:
                with open('./default_file_path/default_file_path.txt', 'r') as default_file_path_file:
                    file_path = default_file_path_file.readline().strip()
            except FileNotFoundError:
                QMessageBox.critical(self, '错误', f'路径记录文件不存在，请先进行手动导入')
                return
            except Exception as e:
                QMessageBox.critical(self, '错误', f'路径记录文件错误：{e}')
                return
        else:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, '选择Excel文件', '', 'Excel Files (*.xlsx *.xls)',
                                                       options=options)
        if file_path:
            try:
                self.file_label.setText(file_path)
                if file_path.endswith('.xlsx'):
                    data_frame = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    data_frame = pd.read_csv(file_path)
                else:
                    QMessageBox.critical(self, '错误', f'文件格式错误')
                    return
            except Exception as e:
                QMessageBox.critical(self, '错误', f'无法导入文件：{e}')
                return
            self.statusBar.showMessage(f'选择的文件是：{file_path}')
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(50)

            # 文件读取
            self.interface.import_data_frame(data_frame)

            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            QMessageBox.information(self, '选择的文件', f'您选择的文件是：{file_path}')
            if not default:
                with open('./default_file_path/default_file_path.txt', 'w') as default_file_path_file:
                    default_file_path_file.write(file_path)
        elif default:
            QMessageBox.critical(self, '错误', f'路径为空')

    def search_stock(self):
        stock_code = self.search_entry.text()
        if stock_code:
            self.statusBar.showMessage(f'正在搜索股票代码：{stock_code}')
            try:
                stock_data = self.interface.search_stock_by_code(stock_code)
                self.display_stock_data(stock_data)
            except StockDataNotFoundException:
                QMessageBox.warning(self, '错误', f'请先导入股票数据文件')
            except StockCodeNotFoundException:
                QMessageBox.warning(self, '未找到', f'未找到股票代码：{stock_code}')
            self.statusBar.clearMessage()
        else:
            QMessageBox.warning(self, '警告', '请输入股票代码进行搜索')

    def display_stock_data(self, stock_data):
        QMessageBox.information(self, '成功', f'成功找到股票，但输出还是要交给前端')

    def generate_chart(self):
        chart_type = self.chart_combo.currentText()
        self.statusBar.showMessage(f'生成图表类型：{chart_type}')
        # 模拟图表生成逻辑
        QMessageBox.information(self, '图表生成', f'图表类型：{chart_type} 已生成')
        self.statusBar.clearMessage()

    def show_login_dialog_and_close(self):
        self.close()
        from .login_dialog import LoginDialog
        login_dialog = LoginDialog()
        login_dialog.exec_()

    def show_register_dialog(self):
        register_dialog = RegisterDialog(self.interface)
        register_dialog.exec_()

    def close_window(self):
        self.close()

    def show_change_username_dialog(self):
        change_username_dialog = ChangeUsernameDialog()
        change_username_dialog.exec_()

    def show_change_password_dialog(self):
        change_password_dialog = ChangePasswordDialog()
        change_password_dialog.exec_()
