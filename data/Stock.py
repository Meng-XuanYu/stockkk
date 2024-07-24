import numpy as np


class Stock:
    def __init__(self, interface, stock_code, data_frame):
        self.__interface = interface
        self.__stock_code = stock_code
        self.__data_frame = data_frame

        # MACD
        self.__ema12 = self.__data_frame['收盘价'].ewm(span=12, adjust=False).mean()
        self.__ema26 = self.__data_frame['收盘价'].ewm(span=26, adjust=False).mean()
        self.__dif = self.__ema12 - self.__ema26
        self.__dea = self.__dif.ewm(span=9, adjust=False).mean()
        self.__macd = 2 * (self.__dif - self.__dea)
        self.__buy_signal = np.where((self.__macd > self.__dea) & (self.__macd.shift(1) < self.__dea.shift(1)), 1, 0)
        self.__sell_signal = np.where((self.__macd < self.__dea) & (self.__macd.shift(1) > self.__dea.shift(1)), 1, 0)

        # RSI
        self.__price_change = self.__data_frame['收盘价'].diff()
        self.__positive_change = self.__price_change.apply(lambda x: x if x > 0 else 0)
        self.__negative_change = self.__price_change.apply(lambda x: -x if x < 0 else 0)
        self.__average_gain = self.__positive_change.rolling(window=14, min_periods=1).mean()
        self.__average_loss = self.__negative_change.rolling(window=14, min_periods=1).mean()
        self.__si = self.__average_loss / self.__average_gain
        self.__rsi = 100 - (100 / (1 + self.__si))

        # boll
        self.__ma = self.__data_frame['收盘价'].rolling(window=20, min_periods=1).mean()
        self.__sd = self.__data_frame['收盘价'].rolling(window=20, min_periods=1).std()
        self.__upper_bond = self.__ma + 2 * self.__sd
        self.__lower_bond = self.__ma - 2 * self.__sd

        self.__charts = {}

    def get_stock_code(self):
        return self.__stock_code

    def get_data_frame(self):
        return self.__data_frame

    def store_chart(self, chart_type, chart):
        self.__charts[chart_type] = chart
        self.__interface.store_chart_into_db(self.__stock_code, chart_type, chart, self.__data_frame)

    def get_chart(self, chart_type):
        if chart_type not in self.__charts:
            chart = self.__interface.get_chart_from_db(self.__stock_code, chart_type)
            if chart is None:
                return None
            else:
                self.__charts[chart_type] = chart
                self.__interface.store_chart_into_user_db_only(self.__stock_code, chart_type, chart, self.__data_frame)
                return chart
        else:
            self.__interface.store_chart_into_user_db_only(self.__stock_code, chart_type, self.__charts[chart_type],
                                                           self.__data_frame)
            return self.__charts[chart_type]
