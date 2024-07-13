def __decrypt(encrypted_password, key):
    result = ""
    for i in range(len(encrypted_password)):
        result += chr(ord(encrypted_password[i]) ^ ord(key[i % len(key)]))
    return result


print(__decrypt('admin', '114514'))