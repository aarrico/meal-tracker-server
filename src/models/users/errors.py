__author__ = 'aarrico'


class UserException(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistException(UserException):
    pass


class IncorrectPasswordException(UserException):
    pass


class UserAlreadyRegisteredException(UserException):
    pass


class InvalidEmailException(UserException):
    pass