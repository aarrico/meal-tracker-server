import uuid

import datetime
from common import utils
from common.database import Database

__author__ = 'aarrico'

collection = 'userprofile'


class UserProfile(object):
    def __init__(self, user_id='', name='', protein=0.0, carbs=0.0, fat=0.0, datetime=datetime.datetime.utcnow(), _id=None):
        self.user_id = user_id
        self.name = name
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.datetime = datetime
        #self.date = datetime.date()
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {} Daily goals: protein: {} carbs: {} fat: {} last updated: {}>".format(self.name, self.protein, self.carbs, self.fat, self.datetime)


    def calculate_calories(self):
        return utils.calculate_calories(self.protein, self.carbs, self.fat)

    def json(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'name': self.name,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'datetime': self.datetime
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