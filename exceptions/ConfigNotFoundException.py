from enum import Enum


class ConfigNotFoundException(Exception):

    def __init__(self, not_found_types, message):
        super().__init__(message)
        self.not_found_types = not_found_types

    def get_not_found_type(self):
        return self.not_found_types


class NotFoundType(Enum):
    FILE = 1
    HOST = 2
    USER = 3
    PASSWORD = 4
