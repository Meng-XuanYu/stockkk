from pyecharts import options as opts
from pyecharts.charts import Kline, Bar, Scatter, Line, Grid
from pyecharts.globals import ThemeType

from interface.ChartType import ChartType


def create_chart(stock, chart_type):
    chart = stock.get_chart(chart_type)
    if chart is not None:
        return chart

    # 数据库没有则生成并存入
    mapping = {
        ChartType.OPEN_CLOSE: create_open_close_chart,
        ChartType.TOTAL_VOLUME: create_total_volume_chart,
        ChartType.HIGH_PRICE: create_high_price_chart,
        ChartType.LOW_PRICE: create_low_price_chart,
        ChartType.COMPOUND_GROWTH: create_compound_growth_chart,
        ChartType.AMPLITUDE_SCATTER: create_amplitude_scatter_chart,
        ChartType.TURNOVER_RATE: create_turnover_rate_chart,
        ChartType.KLINE: create_kline_chart,
    }
    chart = mapping[chart_type](stock.get_data_frame())
    stock.store_chart(chart_type, chart)
    return chart


def create_open_close_chart(stock_data):
    dates = stock_data['日期'].tolist()
    open_prices = stock_data['开盘价'].tolist()
    close_prices = stock_data['收盘价'].tolist()

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))  # 设置响应式布局
    bar.add_xaxis(dates)
    bar.add_yaxis('开盘价', open_prices, label_opts=opts.LabelOpts(is_show=False))  # 不显示数值
    bar.add_yaxis('收盘价', close_prices, label_opts=opts.LabelOpts(is_show=False))  # 不显示数值
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title='开盘和收盘价格平均条形图'),
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


def create_total_volume_chart(stock_data):
    dates = stock_data['日期'].tolist()
    volumes = stock_data['交易量'].tolist()

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    bar.add_xaxis(dates)
    bar.add_yaxis('交易量', volumes, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title='总交易量条形图'),
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


def create_high_price_chart(stock_data):
    dates = stock_data['日期'].tolist()
    high_prices = stock_data['最高价'].tolist()

    line = Line(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    line.add_xaxis(dates)
    line.add_yaxis('最高价', high_prices, label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title='最高价格条形图'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),

        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),

        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
        ),
        datazoom_opts=[opts.DataZoomOpts(type_='inside')],
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
    )

    return line.render_embed()


def create_low_price_chart(stock_data):
    dates = stock_data['日期'].tolist()
    low_prices = stock_data['最低价'].tolist()

    line = Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                        bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    line.add_xaxis(dates)
    line.add_yaxis('最低价', low_prices, label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title='最低价格条形图'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),

        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
        ),
        datazoom_opts=[opts.DataZoomOpts(type_='inside')],
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
    )

    return line.render_embed()


def create_compound_growth_chart(stock_data):
    dates = stock_data['日期'].tolist()
    growths = stock_data['涨跌幅'].tolist()

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    bar.add_xaxis(dates)
    bar.add_yaxis('涨跌幅', growths, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title='复合增长条形图'),
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


def create_amplitude_scatter_chart(stock_data):
    dates = stock_data['日期'].tolist()
    amplitudes = stock_data['振幅'].tolist()

    scatter = Scatter(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                              bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    scatter.add_xaxis(dates)
    scatter.add_yaxis('振幅', amplitudes, label_opts=opts.LabelOpts(is_show=False))
    scatter.set_global_opts(
        title_opts=opts.TitleOpts(title='振幅散点图'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),

        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
        ),
        datazoom_opts=[opts.DataZoomOpts(type_='inside')],
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
    )

    return scatter.render_embed()


def create_turnover_rate_chart(stock_data):
    dates = stock_data['日期'].tolist()
    turnover_rates = stock_data['换手率'].tolist()

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    bar.add_xaxis(dates)
    bar.add_yaxis('换手率', turnover_rates, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title='换手率条形图'),
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


def create_kline_chart(stock_data):
    dates = stock_data['日期'].tolist()

    kline = Kline(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                          bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    kline.add_xaxis(dates)
    kline.add_yaxis(
        'K线图',
        stock_data[['开盘价', '收盘价', '最高价', '最低价']].values.tolist(),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='max', name='最大值'),
                opts.MarkPointItem(type_='min', name='最小值')]
        ),
    )

    ma10 = stock_data['收盘价'].rolling(window=10).mean().dropna()
    start_date = ma10.index[0]

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

    ma20 = stock_data['收盘价'].rolling(window=20, min_periods=1).mean().dropna()
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
        title_opts=opts.TitleOpts(title='K线图'),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
    )

    kline.overlap(line_ma10)
    kline.overlap(line_ma20)

    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                        bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    grid.add(
        kline,
        grid_opts=opts.GridOpts(pos_left='10%', pos_right='10%', height='60%'),
    )

    return kline.render_embed()
