import pandas as pd
from pyecharts import options as opts
from PySide6.QtCore import QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType


class MarketAnalysisWindow(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.setWindowTitle('大盘分析')
        self.setMinimumSize(QSize(1200, 800))
        self.interface = interface
        self.html_list = []
        self.html_list.append(self.create_all_stocks_open_close_chart())
        self.html_list.append(self.create_all_stocks_total_volume_chart())

        self.setStyleSheet('''
            QWidget {
                background-color: rgb(40, 44, 52);
                color: rgb(221, 221, 221);
                font: 10pt "Arial";
            }
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
            }
        ''')

        main_layout = QVBoxLayout()

        self.webEngineViews = []
        self.export_buttons = []

        for html in self.html_list:
            webEngineView = QWebEngineView()
            webEngineView.setHtml(html)
            self.webEngineViews.append(webEngineView)

            button = QPushButton("导出表格文件")
            button.clicked.connect(lambda _, idx=len(self.webEngineViews)-1: self.export_table(idx))
            self.export_buttons.append(button)

            layout = QVBoxLayout()
            layout.addWidget(webEngineView)
            layout.addWidget(button)

            main_layout.addLayout(layout)

        self.setLayout(main_layout)

    def export_table(self, index):
        file_path, _ = QFileDialog.getSaveFileName(None, "保存图表文件", "", "HTML files (*.html);;All files (*)")

        if file_path:
            with open(file_path, mode='w', encoding='utf-8') as file:
                file.write(self.html_list[index])

    def create_all_stocks_open_close_chart(self):
        all_stocks_data = self.interface.get_stock_all_data()
        # 计算所有股票的开盘和收盘价格的平均值
        avg_open_prices = all_stocks_data.groupby('股票代码')['开盘价'].mean()
        avg_close_prices = all_stocks_data.groupby('股票代码')['收盘价'].mean()

        # 转换为DataFrame以便于绘图
        avg_prices_df = pd.DataFrame({
            '股票代码': avg_open_prices.index,
            '开盘价平均值': avg_open_prices.values,
            '收盘价平均值': avg_close_prices.values
        })

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='340%',
                                    bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        bar.add_xaxis(avg_prices_df['股票代码'].tolist())
        bar.add_yaxis('开盘价平均值', avg_prices_df['开盘价平均值'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        bar.add_yaxis('收盘价平均值', avg_prices_df['收盘价平均值'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title='所有股票开盘和收盘价格平均条形图'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_='inside')],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
        )
        return bar.render_embed()

    def create_all_stocks_total_volume_chart(self):
        all_stocks_data = self.interface.get_stock_all_data()
        # 计算所有股票的总交易量
        total_volumes = all_stocks_data.groupby('股票代码')['交易量'].sum().reset_index()
        total_volumes.columns = ['股票代码', '总交易量']

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='340%',
                                    bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        bar.add_xaxis(total_volumes['股票代码'].tolist())
        bar.add_yaxis('总交易量', total_volumes['总交易量'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title='所有股票总交易量条形图'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            datazoom_opts=[opts.DataZoomOpts(type_='inside')],
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
        )
        return bar.render_embed()


