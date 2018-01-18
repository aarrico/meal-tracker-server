import datetime
import uuid
from database import Database

__author__ = 'aarrico'


class Meal(object):
    def __init__(self, foods, date=datetime.datetime.utcnow(), id=None):
        self.foods = foods
        macros = self.calculate_macros()
        self.protein = macros['protein']
        self.carbs = macros['carbs']
        self.fat = macros['fat']
        self.calories = self.calculate_calories()
        self.id = uuid.uuid4().hex if id is None else id
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

    def get_meals(self):
        pass

    def save_to_mongo(self):
        Database.insert('meals', self.json())

    def json(self):
        return {
            'foods': self.foods,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'calories': self.calories,
            'date': self.date,
            'id': self.id
        }

    @classmethod
    def from_mongo(cls, id):
        meal_data = Database.find_one('meals', {'id': id})
        return cls(meal_data['foods'],
                   meal_data['date'],
                   meal_data['id'])