import pymysql
import json
import os

from exceptions.StockCodeNotFoundException import StockCodeNotFoundException
from exceptions.StockDataNotFoundException import StockDataNotFoundException
from exceptions.WrongPassWordException import WrongPassWordException
from exceptions.WrongUsernameException import WrongUsernameException
from exceptions.ConfigNotFoundException import ConfigNotFoundException
from exceptions.ConfigNotFoundException import NotFoundType
from user.User import User
from data.Stock import Stock


class Interface:
    def __init__(self, stock_visualizer):
        self.__stock_visualizer = stock_visualizer
        self.__stock_data_frame_dic = None
        self.__users = None
        self.__magic_num = None
        self.__connection = None
        self.__cursor = None
        self.connect_to_database()

    def connect_to_database(self):
        not_found_types = []
        host = None
        user = None
        password = None

        # 配置文件审查
        if os.path.exists('./config/config.json'):
            with open('./config/config.json', 'r') as f:
                config = json.load(f)
        else:
            not_found_types.append(NotFoundType.FILE)
        if 'host' in config:
            host = config['host']
        else:
            not_found_types.append(NotFoundType.HOST)
        if 'user' in config:
            user = config['user']
        else:
            not_found_types.append(NotFoundType.USER)
        if 'password' in config:
            password = config['password']
        else:
            not_found_types.append(NotFoundType.PASSWORD)
        if len(not_found_types) != 0:
            raise ConfigNotFoundException(not_found_types, '获取配置失败')

        # 连接数据库
        self.__connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('create database if not exists stockkk;')
        self.__cursor.execute('use stockkk;')
        self.__cursor.execute('''
            create table if not exists users (
                username varchar(50) primary key,
                encrypted_password varchar(50)
            );
        ''')

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
        self.__load_user_info()
        if username in self.__users:
            if self.__users[username].check_password(password):
                return self.__users[username]
            else:
                raise WrongPassWordException('密码错误')
        else:
            raise WrongUsernameException('未找到用户名')

    def create_user(self, username, password):
        self.__load_user_info()
        if username in self.__users:
            raise WrongUsernameException('用户名重复')
        else:
            new_user = User(self.__magic_num, username, password)
            self.__users[username] = new_user
            self.__cursor.execute(f'''
                insert into users values('{new_user.get_name()}', '{new_user.get_encrypted_password()}');
            ''')
            self.__connection.commit()

    def __load_user_info(self):
        if self.__users is None:
            self.__users = {}
            self.__magic_num = 'magic_num'
            self.__cursor.execute(f'''
                select * from users;
            ''')
            user_info_rows = self.__cursor.fetchall()
            for user_info_row in user_info_rows:
                username = user_info_row[0]
                encrypted_password = user_info_row[1]
                self.__users[username] = encrypted_password

    def user_rename(self, user, new_name):
        if new_name in self.__users:
            raise WrongUsernameException('用户名已存在')
        ori_name = user.get_name()
        del self.__users[ori_name]
        user.rename(new_name)
        self.__users[new_name] = user
        self.__cursor.execute(f'''
            update users set username = '{new_name}' where username = '{ori_name}';
        ''')
        self.__connection.commit()

    def change_user_password(self, user, new_password):
        user.change_password(new_password)
        self.__cursor.execute(f'''
            update users set password = '{user.get_encrypted_password()}' where username = '{user.get_name()}';
        ''')
        self.__connection.commit()
