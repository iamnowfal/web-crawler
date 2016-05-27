import src.models.favourites.constants as FavouriteConstant
import uuid
from src.common.database import Database


class Favourite:
    def __init__(self, username, _id=None):
        self.username = username
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username': self.username,
            '_id' : self._id
        }

    def save_to_mongo(self):
        Database.insert(FavouriteConstant.COLLECTION, self.json())

