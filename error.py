class MyError(Exception):
    pass

class AnyError(MyError):

    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return("Error !!! "+self.error_msg)
