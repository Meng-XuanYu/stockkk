from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.WrongPassWordException import WrongPassWordException
from exceptions.WrongUsernameException import WrongUsernameException
from user.User import User
from data.Stock import Stock


class Interface:
    def __init__(self, stock_visualizer):
        self.__stock_visualizer = stock_visualizer
        self.__stock_data_frame_dic = None
        self.__users = None
        self.__magic_num = None

    def import_data_frame(self, data_frame):
        grouped = data_frame.groupby('股票代码')
        self.__stock_data_frame_dic = {str(key): Stock(value) for key, value in grouped}

    def search_stock_by_code(self, stock_code):
        if self.__stock_data_frame_dic is None:
            raise StockDataNotFoundException('未导入股票数据')
        elif stock_code in self.__stock_data_frame_dic:
            return self.__stock_data_frame_dic[stock_code]
        else:
            raise StockCodeNotFoundException('股票代码不存在')

    def get_user(self, username, password):
        self.__load_user_info_txt()
        if username in self.__users:
            if self.__users[username].check_password(password):
                return self.__users[username]
            else:
                raise WrongPassWordException('密码错误')
        else:
            raise WrongUsernameException('未找到用户名')

    def create_user(self, username, password):
        self.__load_user_info_txt()
        if username in self.__users:
            raise WrongUsernameException('用户名重复')
        else:
            self.__users[username] = User(self.__magic_num, username, password)
            with open('./user/user_info.txt', 'a') as user_info_file:
                user_info_file.write('\n' + self.__users[username].get_user_info())

    def __load_user_info_txt(self):
        if self.__users is None:
            self.__users = {}
            with open('./user/user_info.txt', 'r') as user_info_file:
                magic_num = user_info_file.readline().strip()
                self.__magic_num = magic_num
                while True:
                    user_info = user_info_file.readline().strip()
                    if user_info == '':
                        break
                    user = User(magic_num, user_info=user_info)
                    self.__users[user.get_name()] = user

    def user_rename(self, user, new_name):
        ori_name = user.get_name()
        del self.__users[ori_name]
        user.rename(new_name)
        self.__users[new_name] = user
        self.__renew_user_info_file(ori_name, user)

    def change_user_password(self, user, new_password):
        user.change_password(new_password)
        self.__renew_user_info_file(user.get_name(), user)

    @staticmethod
    def __renew_user_info_file(ori_name, user):
        with open('./user/user_info.txt', 'r') as user_info_file:
            lines = user_info_file.readlines()
        with open('./user/user_info.txt', 'w') as user_info_file:
            for line in lines:
                words = tuple(line.strip().split())
                if len(words) == 2:
                    name, encrypted_password = words
                    if name == ori_name:
                        user_info_file.write(user.get_user_info())
                    else:
                        user_info_file.write(line)
                else:
                    user_info_file.write(line)
