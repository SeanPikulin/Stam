from Backend.Domain import DBHandler


class Authentication(object):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Authentication.__instance == None:
            Authentication()
        return Authentication.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Authentication.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Authentication.__instance = self
            self.db_handler = DBHandler.DBHandler()
            self.cookie_generator=1

    def register(self, username, password):
        if self.db_handler.is_username_exists(username=username):
            return "username already exists"
        else:
            self.db_handler.add_user_to_db(username=username, password=password, cookie=self.cookie_generator)
            self.cookie_generator = self.cookie_generator + 1
            return "registration succeeded"

    def login(self, username, password):
        if not self.db_handler.is_username_exists(username=username):
            return "username doesn't exist in the system"
        else:
            if not self.db_handler.is_password_match(given_password=password, username=username):
                return "password incorrect"
            else:
                return self.db_handler.get_cookie(username)
