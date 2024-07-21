import pandas as pd
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLineEdit, QLabel,
                             QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget,
                             QAction, QStatusBar, QProgressBar, QComboBox, QTabWidget, QMenu, QTableView)
from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Scatter, Line, Grid
from pyecharts.globals import CurrentConfig, ThemeType
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from .change_password_dialog import ChangePasswordDialog
from .change_username_dialog import ChangeUsernameDialog
from .register_dialog import RegisterDialog


class MainWindow(QMainWindow):
    def __init__(self, interface, user):
        super().__init__()
        self.interface = interface
        self.user = user
        self.stock = None
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
                                   '最低价格条形图', '复合增长条形图', '振幅散点图', '换手率条形图', 'K线图'])
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
        self.preview_label = QWebEngineView(self)
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
                stock = self.interface.search_stock_by_code(stock_code)
                self.display_stock_data(stock.get_data_frame())
                QMessageBox.information(self, '搜索成功', f'可在数据表格中查看数据')
                self.statusBar.showMessage(f'搜索成功：{stock_code},在数据表格中查看数据')
                self.stock = stock
            except StockDataNotFoundException:
                QMessageBox.warning(self, '未找到', f'未倒入股票数据，请先导入数据')
            except StockCodeNotFoundException:
                QMessageBox.warning(self, '未找到', f'未找到股票代码：{stock_code}')
            self.statusBar.clearMessage()
        else:
            QMessageBox.warning(self, '警告', '请输入股票代码进行搜索或先导入数据')

    def display_stock_data(self, stock_data):
        model = QStandardItemModel()
        model.setColumnCount(len(stock_data.columns))
        model.setRowCount(len(stock_data))
        model.setHorizontalHeaderLabels(stock_data.columns)

        for row in range(len(stock_data)):
            for col in range(len(stock_data.columns)):
                item = QStandardItem(str(stock_data.iat[row, col]))
                model.setItem(row, col, item)

        self.data_table.setModel(model)

    def generate_chart(self):
        if self.stock is None:
            QMessageBox.warning(self, '未选择股票', f'请先选择股票')
            return

        chart_type = self.chart_combo.currentText()
        self.statusBar.showMessage(f'生成图表类型：{chart_type}')

        # 根据选择的图表类型生成相应的图表
        if chart_type == '开盘和收盘价格平均条形图':
            chart_html = self.create_open_close_chart()
        elif chart_type == '总交易量条形图':
            chart_html = self.create_total_volume_chart()
        elif chart_type == '最高价格条形图':
            chart_html = self.create_high_price_chart()
        elif chart_type == '最低价格条形图':
            chart_html = self.create_low_price_chart()
        elif chart_type == '复合增长条形图':
            chart_html = self.create_compound_growth_chart()
        elif chart_type == '振幅散点图':
            chart_html = self.create_amplitude_scatter_chart()
        elif chart_type == '换手率条形图':
            chart_html = self.create_turnover_rate_chart()
        elif chart_type == 'K线图':
            chart_html = self.create_Kline_chart()
        else:
            QMessageBox.warning(self, '警告', '请选择图表类型')
            return

        # 将图表嵌入到PyQt窗口中
        self.preview_label.setHtml(chart_html)

        self.statusBar.clearMessage()

    def create_open_close_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_total_volume_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_high_price_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

        return line.render_embed(width="100%", height="500%")

    def create_low_price_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_compound_growth_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_amplitude_scatter_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_turnover_rate_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()
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

    def create_Kline_chart(self):
        stock_data = self.stock.get_data_frame()
        dates = stock_data['日期'].dt.strftime('%Y-%m-%d').tolist()

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
        change_username_dialog = ChangeUsernameDialog(self.interface, self.user)
        change_username_dialog.exec_()

    def show_change_password_dialog(self):
        change_password_dialog = ChangePasswordDialog(self.interface, self.user)
        change_password_dialog.exec_()
