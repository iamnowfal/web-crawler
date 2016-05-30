import src.models.favourites.constants as FavouriteConstant
import uuid
from src.common.database import Database


class Favourite:
    def __init__(self, username, titles, tels, urls, addresses, rates, active=False, _id=None):
        self.username = username
        self.titles = titles
        self.tels = tels
        self.urls = urls
        self.addresses = addresses
        self.rates = rates
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username': self.username,
            'titles': self.titles,
            'tels': self.tels,
            'urls': self.urls,
            'addresses': self.addresses,
            'rates': self.rates,
            'active':self.active,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.update(FavouriteConstant.COLLECTION, {'urls':self.urls}, self.json())

    @classmethod
    def find_all_by_username(cls, username):
        return [cls(ele) for ele in Database.find(FavouriteConstant.COLLECTION, {'username':username})]

    @classmethod
    def find_by_title(cls, title):
        return cls(Database.find_one(FavouriteConstant.COLLECTION, {'title':title}))



    def delete(self):
        Database.remove(FavouriteConstant.COLLECTION, {'_id':self._id})

