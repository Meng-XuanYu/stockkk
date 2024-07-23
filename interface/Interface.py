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
    def __init__(self, window=None):
        self.__file_name = None
        self.__stock_data_frame_dic = None
        self.__users = None
        self.__magic_num = '114514'
        self.__connection = None
        self.__cursor = None
        self.__connect_to_database()
        self.__cur_user = None
        self.__window = window
        self.__set_default_file_name()

    @staticmethod
    def __create_connection():
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
        return pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __connect_to_database(self):
        self.__connection = self.__create_connection()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('create database if not exists stockkk;')
        self.__cursor.execute('use stockkk;')
        self.__cursor.execute('''
            create table if not exists users (
                username varchar(50) primary key,
                encrypted_password varchar(50)
            );
        ''')
        self.__cursor.execute('''
            create table if not exists stocks (
                stock_code varchar(50) primary key,
                open_close longtext default null,
                total_volume longtext default null,
                high_price longtext default null,
                low_price longtext default null,
                compound_growth longtext default null,
                amplitude_scatter longtext default null,
                turnover_rate longtext default null,
                kline longtext default null
            );
        ''')
        self.__cursor.execute('''
            create table if not exists log_records (
                id int auto_increment primary key,
                username varchar(50),
                is_login bool,
                log_time datetime default current_timestamp
            );
        ''')
        self.__cursor.execute('''
            create table if not exists default_file_name (
                magic_num varchar(50) primary key,
                file_name varchar(260) default null
            );
        ''')
        self.__cursor.execute(f'''
            insert ignore into default_file_name (magic_num) values (%s)
        ''', (self.__magic_num,))
        self.__connection.commit()

    def __set_default_file_name(self):
        self.__cursor.execute(f'''
            select file_name from default_file_name where magic_num = %s;
        ''', (self.__magic_num,))
        self.__file_name = list(self.__cursor.fetchall()[0].values())[0]

    def set_file_name(self, file_name):
        if file_name != self.__file_name:
            self.__file_name = file_name
            self.__cursor.execute(f'''
                update default_file_name set file_name = %s where magic_num = %s
            ''', (file_name, self.__magic_num))
            self.__connection.commit()
            self.__cursor.execute('''
                truncate table stocks;
            ''')

    def import_data_frame(self, data_frame):
        grouped = data_frame.groupby('股票代码')
        self.__stock_data_frame_dic = {str(key): Stock(self, str(key), value) for key, value in grouped}

    def search_stock_by_code(self, stock_code):
        if self.__stock_data_frame_dic is None:
            raise StockDataNotFoundException('未导入股票数据')
        elif stock_code in self.__stock_data_frame_dic:
            return self.__stock_data_frame_dic[stock_code]
        else:
            raise StockCodeNotFoundException('股票代码不存在')

    def user_login(self, username, password):
        self.__cur_user = self.__get_user(username, password)
        self.__cur_user.login(self.__create_connection())
        self.__cursor.execute(f'''
            insert into log_records (username, is_login) values (%s, true);
        ''', (username,))
        self.__connection.commit()

    def user_logout(self, username):
        self.__cur_user.logout()
        self.__cur_user = None
        self.__cursor.execute(f'''
            insert into log_records (username, is_login) values (%s, false);
        ''', (username,))
        self.__connection.commit()

    def get_current_user(self):
        return self.__cur_user

    def __get_user(self, username, password):
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
            new_user = User(self, self.__magic_num, username, password=password)
            self.__users[username] = new_user
            self.__cursor.execute(f'''
                insert into users values (%s, %s);
            ''', (new_user.get_name(), new_user.get_encrypted_password()))
            self.__connection.commit()

    def __load_user_info(self):
        if self.__users is None:
            self.__users = {}
            self.__cursor.execute(f'''
                select * from users;
            ''')
            user_info_rows = self.__cursor.fetchall()
            for user_info_row in user_info_rows:
                username = user_info_row['username']
                encrypted_password = user_info_row['encrypted_password']
                self.__users[username] = User(self, self.__magic_num, username, encrypted_password)

    def user_rename(self, user, new_name):
        if new_name in self.__users:
            raise WrongUsernameException('用户名已存在')
        ori_name = user.get_name()
        del self.__users[ori_name]
        user.rename(new_name)
        self.__users[new_name] = user
        self.__cursor.execute(f'''
            update users set username = %s where username = %s;
        ''', (new_name, ori_name))
        self.__connection.commit()

    def change_user_password(self, user, new_password):
        user.change_password(new_password)
        self.__cursor.execute(f'''
            update users set encrypted_password = %s where username = %s;
        ''', (user.get_encrypted_password(), user.get_name()))
        self.__connection.commit()

    def store_chart_into_db(self, stock_code, chart_type, chart_html):
        if self.__cur_user is not None:
            self.__cur_user.store_chart_into_user_db(stock_code, chart_type, chart_html)
        sql = f'''
            insert into stocks (stock_code, {chart_type.get_chart_type_name()})
            values (%s, %s)
            on duplicate key update {chart_type.get_chart_type_name()} = values ({chart_type.get_chart_type_name()});
        '''
        self.__cursor.execute(sql, (stock_code, chart_html))
        self.__connection.commit()

    def get_chart_from_db(self, stock_code, chart_type):
        # TODO
        # 由于在整体和用户级都有存储，需要考虑一下调用的优先级
        self.__cursor.execute(f'''
            select {chart_type.get_chart_type_name()} from stocks where stock_code = %s;
        ''', (stock_code,))
        result = self.__cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            return list(result[0].values())[0]

    def change_window(self, window):
        self.__window.close()
        self.__window = window

    def set_window(self, window):
        self.__window = window

    def get_window(self):
        return self.__window
