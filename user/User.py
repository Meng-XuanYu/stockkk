import sys
from exceptions.WrongParamException import WrongParamException


class User:
    def __init__(self, magic_num, username=None, password=None, user_info=None):
        self.__magic_num = magic_num
        if user_info is None:
            self.__username = username
            self.__encrypted_password = self.__encrypt(password, magic_num)
        elif username is None and password is None:
            self.__username, self.__encrypted_password = user_info.split()
        else:
            sys.stderr.write('User构造函数参数错误')
            raise WrongParamException('User构造函数参数错误')

    @staticmethod
    def __decrypt(encrypted_password, key):
        # result = ""
        # for i in range(len(encrypted_password)):
        #     result += chr(ord(encrypted_password[i]) ^ ord(key[i % len(key)]))
        # return result
        return encrypted_password

    @staticmethod
    def __encrypt(password, key):
        # result = ""
        # for i in range(len(password)):
        #     result += chr(ord(password[i]) ^ ord(key[i % len(key)]))
        #     print(result)
        # return result
        return password

    def get_name(self):
        return self.__username

    def __str__(self):
        return self.__username

    def check_password(self, password):
        return password == User.__decrypt(self.__encrypted_password, self.__magic_num)

    def get_user_info(self):
        return self.__username + ' ' + self.__encrypted_password
