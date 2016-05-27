class UserError(Exception):

    def __init__(self, message):
        self.message = message

class UserAlreadyHasError(UserError):
    pass

class UserNotExistError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass

class ReTypePasswordError(UserError):
    pass