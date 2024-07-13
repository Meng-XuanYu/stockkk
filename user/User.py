class User:
    def __init__(self, magic_num, user_info):
        self.__magic_num = magic_num
        self.__username, self.__encrypted_password = user_info.split()

    @staticmethod
    def __decrypt(encrypted_password, key):
        result = ""
        for i in range(len(encrypted_password)):
            result += chr(ord(encrypted_password[i]) ^ ord(key[i % len(key)]))
        return result

    @staticmethod
    def __encrypt(password, key):
        result = ""
        for i in range(len(password)):
            result += chr(ord(password[i]) ^ ord(key[i % len(key)]))
        return result

    def get_name(self):
        return self.__username

    def __str__(self):
        return self.__username

    def check_password(self, password):
        return password == User.__decrypt(self.__encrypted_password, self.__magic_num)
