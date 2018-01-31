import uuid

from common import utilities
from common.database import Database

__author__ = 'aarrico'

collection = 'userprofile'


class UserProfile(object):
    def __init__(self, user_id='', name='', protein=0.0, carbs=0.0, fat=0.0, _id=None):
        self.user_id = user_id
        self.name = name
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self._id = uuid.uuid4().hex if _id is None else _id

    def calculate_calories(self):
        return utilities.calculate_calories(self.protein, self.carbs, self.fat)

    def json(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'name': self.name,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat
        }

    def save_profile(self):
        Database.insert(collection, self.json())

    @classmethod
    def from_mongo(cls, _id):
        profile_data = Database.find_one(collection, {'_id': _id})
        return cls(**profile_data)

    @classmethod
    def find_by_user_id(cls, user_id):
        profile_data = Database.find_one(collection, {'user_id': user_id})
        return cls(**profile_data)