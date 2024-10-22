class User:
    def __init__(self, interface, magic_num, username, encrypted_password=None, password=None):
        self.__interface = interface
        self.__magic_num = magic_num
        self.__username = username
        self.__connection = None
        self.__cursor = None
        if encrypted_password is not None:
            self.__encrypted_password = encrypted_password
        elif password is not None:
            self.__encrypted_password = self.__encrypt(password, magic_num)
        else:
            self.__encrypted_password = ''

    @staticmethod
    def __decrypt(encrypted_password, key):
        result = ''
        skip_len = len('stockkk_password_')
        skipped_encrypted_password = encrypted_password[skip_len:]
        for i in range(len(skipped_encrypted_password)):
            result += chr(ord(skipped_encrypted_password[i]) ^ ord(key[i % len(key)]))
        return result

    @staticmethod
    def __encrypt(password, key):
        result = 'stockkk_password_'
        for i in range(len(password)):
            result += chr(ord(password[i]) ^ ord(key[i % len(key)]))
        return result

    def get_name(self):
        return self.__username

    def __str__(self):
        return self.__username

    def check_password(self, password):
        return password == User.__decrypt(self.__encrypted_password, self.__magic_num)

    def get_encrypted_password(self):
        return self.__encrypted_password

    def rename(self, new_name):
        self.__cursor.execute(f'''
            create database stockkk_user_{new_name};
        ''')
        self.__cursor.execute(f'''use stockkk_user_{self.__username};''')
        self.__cursor.execute(f'''show tables;''')
        tables = self.__cursor.fetchall()
        for table_dic in tables:
            table_name = list(table_dic.values())[0]
            self.__cursor.execute(f'''
                rename table stockkk_user_{self.__username}.{table_name} to stockkk_user_{new_name}.{table_name};
            ''')
        self.__cursor.execute(f'''drop database stockkk_user_{self.__username};''')
        self.__cursor.execute(f'''use stockkk_user_{new_name};''')
        self.__username = new_name

    def change_password(self, new_password):
        self.__encrypted_password = self.__encrypt(new_password, self.__magic_num)

    def login(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()
        self.__cursor.execute(f'create database if not exists stockkk_user_{self.__username};')
        self.__cursor.execute(f'use stockkk_user_{self.__username};')
        self.__cursor.execute('''
            create table if not exists log_records (
                id int auto_increment primary key,
                is_login bool,
                log_time datetime default current_timestamp
            );
        ''')
        self.__cursor.execute('''
            create table if not exists chart_records (
                store_time datetime primary key default current_timestamp,
                stock_code varchar(50),
                chart_type varchar(50),
                chart longtext,
                file_name varchar(260),
                stock_data json
            );
        ''')
        self.__cursor.execute('''
            insert into log_records (is_login) values (true);
        ''')
        self.__connection.commit()

    def logout(self):
        self.__cursor.execute('''
            insert into log_records (is_login) values (false);
        ''')
        self.__connection.commit()
        self.__cursor = None
        self.__connection = None

    def get_log_records(self):
        self.__cursor.execute('''
            select * from log_records order by id desc;
        ''')
        return self.__cursor.fetchall()

    def clear_log_records(self):
        self.__cursor.execute('''
            truncate table log_records;
        ''')

    def clear_chart_records(self):
        self.__cursor.execute('''
            truncate table chart_records;
        ''')

    def get_chart_records(self):
        self.__cursor.execute('''
            select store_time, stock_code, chart_type, file_name from chart_records order by store_time asc;
        ''')
        return self.__cursor.fetchall()

    def get_chart_and_data_in_records(self, store_time):
        self.__cursor.execute(f'''
            select chart, stock_data from chart_records where store_time = %s
        ''', store_time)
        return self.__cursor.fetchall()[0]

    def store_chart_into_user_db(self, stock_code, chart_type, chart_html, file_name, stock_data):
        self.__cursor.execute(f'''
            insert ignore into chart_records (stock_code, chart_type, chart, file_name, stock_data)
            values (%s, %s, %s, %s, %s);
        ''', (stock_code, chart_type.get_chart_type_name(), chart_html, file_name, stock_data.to_json()))
        self.__connection.commit()

    def delete(self):
        self.__cursor.execute(f'''
            drop database stockkk_user_{self.__username};
        ''')
        self.__connection.commit()

    def get_lastest_chart(self):
        self.__cursor.execute('''
            select store_time, stock_code, chart_type, file_name from chart_records order by store_time desc limit 1;
        ''')
        return self.__cursor.fetchall()[0]
