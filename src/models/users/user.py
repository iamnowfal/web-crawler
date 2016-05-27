import uuid
from src.common.database import Database
import src.models.users.constants as UserConstant
import src.models.users.error as UserError
from src.common.utils import Utils

class User:

    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username' : self.username,
            'password' : self.password,
            '_id' : self._id
        }

    def save_to_mongo(self):
        Database.insert(UserConstant.COLLECTION, self.json())

    @staticmethod
    def register_user(username, password):
        user_data = Database.find_one(UserConstant.COLLECTION, {'username':username})
        if user_data is not None:
            raise UserError.UserAlreadyHasError("User is already existing, please use another username")
        password = Utils.hash_password(password)
        user = User(username, password)
        user.save_to_mongo()
        return True

    @staticmethod
    def is_login_valid(username, password):
        user_data = Database.find_one(UserConstant.COLLECTION, {'username':username})
        if user_data is None:
            raise UserError.UserNotExistError("User is not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserError.IncorrectPasswordError("Password is not correct")

        return True

