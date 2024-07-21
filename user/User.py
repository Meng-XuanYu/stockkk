class User:
    def __init__(self, magic_num, username, encrypted_password=None, password=None):
        self.__magic_num = magic_num
        self.__username = username
        if encrypted_password is not None:
            self.__encrypted_password = encrypted_password
        elif password is not None:
            self.__encrypted_password = self.__encrypt(password, magic_num)
        else:
            self.__encrypted_password = ''

    @staticmethod
    def __decrypt(encrypted_password, key):
        # result = ''
        # for i in range(len(encrypted_password)):
        #     result += chr(ord(encrypted_password[i]) ^ ord(key[i % len(key)]))
        # return result
        return encrypted_password

    @staticmethod
    def __encrypt(password, key):
        # result = ''
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

    def get_encrypted_password(self):
        return self.__encrypted_password

    def rename(self, new_name):
        self.__username = new_name

    def change_password(self, new_password):
        self.__encrypted_password = self.__encrypt(new_password, self.__magic_num)
