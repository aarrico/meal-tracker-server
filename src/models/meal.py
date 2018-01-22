__author__ = 'aarrico'

import datetime
import uuid
from common.database import Database

collection = 'meals'


class Meal(object):
    def __init__(self, user_id, foods, date=datetime.datetime.utcnow(), _id=None):
        self.user_id = user_id
        self.foods = foods
        macros = self.calculate_macros()
        self.protein = macros['protein']
        self.carbs = macros['carbs']
        self.fat = macros['fat']
        self.calories = self.calculate_calories()
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date = date

    def calculate_macros(self):
        macros = {'protein': 0, 'carbs': 0, 'fat': 0}
        print(self.foods)
        for key in self.foods:
            fd = Database.find_one('foods', {'name': key})
            amount = float(self.foods[key])
            print(fd['name'])
            macros['protein'] += fd['protein'] * amount
            macros['carbs'] += fd['carbs'] * amount
            macros['fat'] += fd['fat'] * amount
        return macros

    def calculate_calories(self):
        return (self.protein + self.carbs) * 4 + self.fat * 9

    @classmethod
    def new_meal(cls, foods, date=datetime.datetime.utcnow()):
        meal = cls(foods, date)
        Database.insert(collection, meal.json())

    def get_meals(self):
        pass

    def save_to_mongo(self):
        Database.insert(collection, self.json())

    def json(self):
        return {
            'user_id': self.user_id,
            'foods': self.foods,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'calories': self.calories,
            'date': self.date,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        meal_data = Database.find_one(collection, {'_id': _id})
        return cls(**meal_data)

    @classmethod
    def find_by_user_id(cls, user_id):
        meals = Database.find(collection, {'user_id': user_id})
        return [cls(**meal) for meal in meals]