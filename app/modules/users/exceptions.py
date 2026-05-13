class EmailTakenException(Exception):
    def __init__(self, message: str):
        self.message = message


class UserNameTakenException(Exception):
    def __init__(self, message: str):
        self.message = message

class UserDoesNotExist(Exception):
    def __init__(self, message: str):
        self.message = message

