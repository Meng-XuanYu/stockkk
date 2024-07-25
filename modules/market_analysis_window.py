import pandas as pd
from pyecharts import options as opts
from PySide6.QtCore import QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QScrollArea
from pyecharts.charts import Bar, Line, Kline, Grid, Pie
from pyecharts.globals import ThemeType


class MarketAnalysisWindow(QWidget):
    def __init__(self, interface):
        super().__init__()
        self.setWindowTitle('大盘分析')
        self.setMinimumSize(QSize(1200, 800))
        self.interface = interface
        self.html_list = []
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet('''
                                    QScrollArea {
                                        background-color: transparent;
                                        border-radius: 5px;
                                    }
                                ''')
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.html_list.append(self.create_all_stocks_open_close_chart())
        self.html_list.append(self.create_all_stocks_total_volume_chart_code())
        self.html_list.append(self.create_all_stocks_total_volume_chart_date())
        self.html_list.append(self.create_price_change_pie_chart())
        self.html_list.append(self.create_all_stocks_kline_chart())

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
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.webEngineViews = []
        self.export_buttons = []

        for html in self.html_list:
            webEngineView = QWebEngineView()
            webEngineView.setFixedHeight(320)
            webEngineView.setHtml(html)
            self.webEngineViews.append(webEngineView)

            button = QPushButton("导出表格文件")
            button.clicked.connect(lambda _, idx=len(self.webEngineViews) - 1: self.export_table(idx))
            self.export_buttons.append(button)

            layout = QVBoxLayout()
            layout.addWidget(webEngineView)
            layout.addWidget(button)

            scroll_layout.addLayout(layout)

        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

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
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
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

    def create_all_stocks_total_volume_chart_code(self):
        all_stocks_data = self.interface.get_stock_all_data()
        # 计算所有股票的总交易量
        total_volumes = all_stocks_data.groupby('股票代码')['交易量'].sum().reset_index()
        total_volumes.columns = ['股票代码', '总交易量']

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
                                    bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        bar.add_xaxis(total_volumes['股票代码'].tolist())
        bar.add_yaxis('总交易量', total_volumes['总交易量'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title='所有股票总交易量条形图(按股票代码)'),
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

    def create_all_stocks_total_volume_chart_date(self):
        all_stocks_data = self.interface.get_stock_all_data()
        # 计算所有股票的总交易量
        total_volumes = all_stocks_data.groupby('日期')['交易量'].sum().reset_index()
        total_volumes.columns = ['日期', '总交易量']

        bar = Bar(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
                                    bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        bar.add_xaxis(total_volumes['日期'].tolist())
        bar.add_yaxis('总交易量', total_volumes['总交易量'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title='所有股票总交易量条形图(按日期)'),
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

    def create_all_stocks_kline_chart(self):
        stock_data = self.interface.get_stock_all_data()

        # 按日期汇总所有股票的开盘价、收盘价、最高价和最低价
        aggregated_data = stock_data.groupby('日期').agg({
            '开盘价': 'first',
            '收盘价': 'last',
            '最高价': 'max',
            '最低价': 'min'
        }).reset_index()

        dates = aggregated_data['日期'].tolist()

        kline = Kline(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
                                              bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        kline.add_xaxis(dates)
        kline.add_yaxis(
            'K线图',
            aggregated_data[['开盘价', '收盘价', '最高价', '最低价']].values.tolist(),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_='max', name='最大值'),
                    opts.MarkPointItem(type_='min', name='最小值')]
            ),
        )

        ma10 = aggregated_data['收盘价'].rolling(window=10).mean().dropna()

        line_ma10 = Line()
        line_ma10.add_xaxis(dates[8:])
        line_ma10.add_yaxis(
            'MA10',
            ma10.tolist(),
            is_smooth=True,
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )
        line_ma10.set_global_opts(legend_opts=opts.LegendOpts(pos_left='right'))

        ma20 = aggregated_data['收盘价'].rolling(window=20, min_periods=1).mean().dropna()
        line_ma20 = Line()
        line_ma20.add_xaxis(dates[18:])
        line_ma20.add_yaxis(
            'MA20',
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
            datazoom_opts=[opts.DataZoomOpts(type_='inside')],
            title_opts=opts.TitleOpts(title='所有股票汇总K线图'),
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
            toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
        )

        kline.overlap(line_ma10)
        kline.overlap(line_ma20)

        grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
                                            bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        grid.add(
            kline,
            grid_opts=opts.GridOpts(pos_left='10%', pos_right='10%', height='60%'),
        )

        return kline.render_embed()

    def create_price_change_pie_chart(self):
        all_stocks_data = self.interface.get_stock_all_data()

        # 计算每只股票一年内的涨跌幅度
        yearly_price_change = all_stocks_data.groupby('股票代码').agg({
            '开盘价': 'first',
            '收盘价': 'last'
        }).reset_index()
        yearly_price_change['涨跌幅度'] = (yearly_price_change['收盘价'] - yearly_price_change['开盘价']) / \
                                          yearly_price_change['开盘价'] * 100

        # 根据涨跌幅度分类
        yearly_price_change['涨跌分类'] = pd.cut(yearly_price_change['涨跌幅度'],
                                                 bins=[-float('inf'), -5, 0, 5, float('inf')],
                                                 labels=['大跌', '小跌', '小涨', '大涨'])

        # 计算涨跌分类的分布
        price_change_distribution = yearly_price_change['涨跌分类'].value_counts()

        # 转换为DataFrame以便于绘图
        price_change_df = pd.DataFrame({
            '涨跌分类': price_change_distribution.index,
            '数量': price_change_distribution.values
        })

        pie = Pie(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='300%',
                                    bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
        pie.add(
            '',
            [list(z) for z in zip(price_change_df['涨跌分类'].tolist(), price_change_df['数量'].tolist())],
            radius=['40%', '75%'],
            label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {c} ({d}%)")
        )
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title='股票一年涨跌分布饼图'),
            legend_opts=opts.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')
        )
        return pie.render_embed()
