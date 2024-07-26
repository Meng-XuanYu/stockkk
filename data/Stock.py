class Stock:
    def __init__(self, interface, stock_code, data_frame):
        self.__interface = interface
        self.__stock_code = stock_code
        self.__data_frame = data_frame

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
