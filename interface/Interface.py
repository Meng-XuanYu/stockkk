from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.WrongPassWordException import WrongPassWordException
from exceptions.WrongUsernameException import WrongUsernameException
from user.User import User


class Interface:
    def __init__(self, stock_visualizer):
        self.__stock_visualizer = stock_visualizer
        self.__stock_data_frame_dic = None
        self.__users = None

    def import_data_frame(self, data_frame):
        grouped = data_frame.groupby('股票代码')
        self.__stock_data_frame_dic = {key: value for key, value in grouped}

    def search_stock_by_code(self, stock_code):
        if self.__stock_data_frame_dic == None:
            raise StockDataNotFoundException('未导入股票数据')
        elif int(stock_code) in self.__stock_data_frame_dic:
            return self.__stock_data_frame_dic[int(stock_code)]
        else:
            raise StockCodeNotFoundException('股票代码不存在')

    def get_user(self, username, password):
        if self.__users == None:
            self.__users = {}
            with open('./user/user_info.txt', 'r') as user_info_file:
                magic_num = user_info_file.readline().strip()
                while True:
                    user_info = user_info_file.readline().strip()
                    if user_info == '':
                        break
                    user = User(magic_num, user_info)
                    self.__users[user.get_name()] = user
        if username in self.__users:
            if self.__users[username].check_password(password):
                return self.__users[username]
            else:
                raise WrongPassWordException('密码错误')
        else:
            raise WrongUsernameException('未找到用户名')

    def create_user(self, username, password):
        pass