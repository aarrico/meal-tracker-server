__author__ = 'aarrico'

import uuid
from common.database import Database

collection = 'foods'


class Food(object):

    def __init__(self, name, measurement, protein, carbs, fat, _id=None):
        self.name = name
        self.measurement = measurement
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<{} protein: {} carbs: {} fat: {}>".format(self.name, self.protein, self.carbs, self.fat)

    def json(self):
        return {
            '_id': self._id,
            'name' : self.name,
            'measurement': self.measurement,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
        }

    def save_to_mongo(self):
        Database.insert(collection, self.json())

    @classmethod
    def from_mongo(cls, _id):
        food_data = Database.find_one(collection, {'_id': _id})
        return cls(**food_data)

