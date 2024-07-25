from enum import Enum


class ChartType(Enum):
    OPEN_CLOSE = 1
    TOTAL_VOLUME = 2
    HIGH_PRICE = 3
    LOW_PRICE = 4
    COMPOUND_GROWTH = 5
    AMPLITUDE_SCATTER = 6
    TURNOVER_RATE = 7
    KLINE = 8
    PRICE_LINE = 9
    RSI = 10
    MACD = 11

    def get_chart_type_name(self):
        mapping = {
            ChartType.OPEN_CLOSE: 'open_close',
            ChartType.TOTAL_VOLUME: 'total_volume',
            ChartType.HIGH_PRICE: 'high_price',
            ChartType.LOW_PRICE: 'low_price',
            ChartType.COMPOUND_GROWTH: 'compound_growth',
            ChartType.AMPLITUDE_SCATTER: 'amplitude_scatter',
            ChartType.TURNOVER_RATE: 'turnover_rate',
            ChartType.KLINE: 'kline',
            ChartType.PRICE_LINE: 'price_line',
            ChartType.RSI: 'rsi',
            ChartType.MACD: 'macd',
        }
        return mapping[self]

    @staticmethod
    def get_chart_type_from_text(text):
        mapping = {
            '开盘和收盘价格平均条形图': ChartType.OPEN_CLOSE,
            '总交易量条形图': ChartType.TOTAL_VOLUME,
            '最高价格条形图': ChartType.HIGH_PRICE,
            '最低价格条形图': ChartType.LOW_PRICE,
            '复合增长条形图': ChartType.COMPOUND_GROWTH,
            '振幅散点图': ChartType.AMPLITUDE_SCATTER,
            '换手率条形图': ChartType.TURNOVER_RATE,
            'K线图': ChartType.KLINE,
            '价格折线图': ChartType.PRICE_LINE,
            'RSI图': ChartType.RSI,
            'MACD图': ChartType.MACD,
        }
        if text in mapping:
            return mapping[text]
        else:
            return None

    @staticmethod
    def get_back_chart_type_name(text):
        mapping = {
            'open_close': '开盘和收盘价格平均条形图',
            'total_volume': '总交易量条形图',
            'high_price': '最高价格条形图',
            'low_price': '最低价格条形图',
            'compound_growth': '复合增长条形图',
            'amplitude_scatter': '振幅散点图',
            'turnover_rate': '换手率条形图',
            'kline': 'K线图',
            'price_line': '价格折线图',
            'rsi': 'RSI图',
            'macd': 'MACD图',
        }
        return mapping[text]
