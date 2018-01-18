import uuid
from database import Database

__author__ = 'aarrico'


class Food(object):

    def __init__(self, name, measurement, protein, carbs, fat, id=None):
        self.name = name
        self.measurement = measurement
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.id = uuid.uuid4().hex if id is None else id

    def save_to_mongo(self):
        Database.insert('foods', self.json())

    def json(self):
        return {
            'id': self.id,
            'name' : self.name,
            'measurement': self.measurement,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
        }

    @classmethod
    def from_mongo(cls, id):
        food_data = Database.find_one('foods', {'id': id})
        return cls(food_data['name'],
                   food_data['measurement'],
                   food_data['protein'],
                   food_data['carbs'],
                   food_data['fat'],
                   food_data['id'])

