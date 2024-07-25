import numpy as np
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
        ChartType.PRICE_LINE: create_price_line_chart,
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
    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    bar.add_xaxis(dates)
    bar.add_yaxis('最高价', high_prices, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
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

    return bar.render_embed()


def create_low_price_chart(stock_data):
    dates = stock_data['日期'].tolist()
    low_prices = stock_data['最低价'].tolist()

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    bar.add_xaxis(dates)
    bar.add_yaxis('最低价', low_prices, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
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

    return bar.render_embed()


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

    line_ma10 = Line()
    line_ma10.add_xaxis(dates[9:])
    line_ma10.add_yaxis(
        'MA10',
        ma10.tolist(),
        is_smooth=True,
        is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False)
    )
    line_ma10.set_global_opts(legend_opts=opts.LegendOpts(pos_left='right'))

    ma20 = stock_data['收盘价'].rolling(window=20).mean().dropna()
    line_ma20 = Line()
    line_ma20.add_xaxis(dates[19:])
    line_ma20.add_yaxis(
        'MA20',
        ma20.tolist(),
        is_smooth=True,
        is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False)
    )

    ema12 = stock_data['收盘价'].ewm(span=12, adjust=False).mean()
    ema26 = stock_data['收盘价'].ewm(span=26, adjust=False).mean()
    dif = ema12 - ema26
    line_dif = Line()
    line_dif.add_xaxis(dates)
    line_dif.add_yaxis(
        'DIF',
        dif.tolist(),
        is_smooth=True,
        is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False)
    )

    dea = dif.ewm(span=9, adjust=False).mean()
    line_dea = Line()
    line_dea.add_xaxis(dates)
    line_dea.add_yaxis(
        'DEA',
        dea.tolist(),
        is_smooth=True,
        is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False)
    )

    macd = 2 * (dif - dea)
    bar_macd = Bar()
    bar_macd.add_xaxis(dates)
    bar_macd.add_yaxis(
        'MACD',
        macd.tolist(),
        label_opts=opts.LabelOpts(is_show=False)
    )

    # 计算金叉和死叉点
    buy_signal = np.where((macd > dea) & (macd.shift(1) < dea.shift(1)), 1, 0)
    sell_signal = np.where((macd < dea) & (macd.shift(1) > dea.shift(1)), 1, 0)

    buy_dates = np.array(dates)[buy_signal == 1].tolist()
    sell_dates = np.array(dates)[sell_signal == 1].tolist()
    buy_points = stock_data.loc[buy_signal == 1, '收盘价'].tolist()
    sell_points = stock_data.loc[sell_signal == 1, '收盘价'].tolist()

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
    kline.overlap(line_dif)
    kline.overlap(line_dea)
    kline.overlap(bar_macd)

    # 添加金叉和死叉标记点
    kline.add_yaxis(
        '金叉',
        [],
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name='金叉', coord=[buy_dates[i], buy_points[i]], value=buy_points[i],
                                     itemstyle_opts=opts.ItemStyleOpts(color='red')) for i in range(len(buy_dates))],
            symbol='triangle',
            symbol_size=13
        )
    )
    kline.add_yaxis(
        '死叉',
        [],
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name='死叉', coord=[sell_dates[i], sell_points[i]], value=sell_points[i],
                                     itemstyle_opts=opts.ItemStyleOpts(color='green')) for i in range(len(sell_dates))],
            symbol='arrow',
            symbol_size=13
        )
    )

    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                        bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    grid.add(
        kline,
        grid_opts=opts.GridOpts(pos_left='10%', pos_right='10%', height='60%'),
    )

    return kline.render_embed()


def create_price_line_chart(stock_data):
    stock_data = stock_data.reset_index(drop=True)

    dates = stock_data['日期'].tolist()
    open_prices = stock_data['开盘价'].tolist()
    close_prices = stock_data['收盘价'].tolist()

    # 计算移动平均线
    ma5 = stock_data['收盘价'].rolling(window=5).mean()
    ma10 = stock_data['收盘价'].rolling(window=10).mean()
    ma30 = stock_data['收盘价'].rolling(window=30).mean()

    # 找出金叉和死叉
    golden_cross = []
    death_cross = []
    for i in range(1, len(ma5)):
        if ma5[i - 1] < ma30[i - 1] and ma5[i] > ma30[i]:
            golden_cross.append((dates[i], close_prices[i]))
        elif ma5[i - 1] > ma30[i - 1] and ma5[i] < ma30[i]:
            death_cross.append((dates[i], close_prices[i]))

    line = Line(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='500%',
                                bg_color='rgb(40, 44, 52)', is_fill_bg_color=True))
    line.add_xaxis(dates)
    line.add_yaxis('开盘价', open_prices, label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis('收盘价', close_prices, label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis('MA5', ma5.tolist(), label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(width=2, type_='solid'))
    line.add_yaxis('MA10', ma10.tolist(), label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(width=2, type_='dashed'))
    line.add_yaxis('MA30', ma30.tolist(), label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(width=2, type_='dotted'))

    line.set_series_opts(
        markpoint_opts=opts.MarkPointOpts(
            data=[
                     opts.MarkPointItem(
                         name='金叉', coord=[date, price], value='金叉',
                         symbol='triangle', symbol_size=10, itemstyle_opts=opts.ItemStyleOpts(color='gold')
                     ) for date, price in golden_cross
                 ] + [
                     opts.MarkPointItem(
                         name='死叉', coord=[date, price], value='死叉',
                         symbol='triangle-down', symbol_size=10, itemstyle_opts=opts.ItemStyleOpts(color='red')
                     ) for date, price in death_cross
                 ]
        )
    )

    line.set_global_opts(
        title_opts=opts.TitleOpts(title='股票价格折线图'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='line'),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
        ),
        datazoom_opts=[opts.DataZoomOpts(type_='inside')],
        toolbox_opts=opts.ToolboxOpts(is_show=True, feature={'dataZoom': {'yAxisIndex': 'none'}})
    )

    return line.render_embed()

