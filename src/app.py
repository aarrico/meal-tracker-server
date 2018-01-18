from database import Database
from models.food import Food
from models.meal import Meal

__author__ = 'aarrico'

Database.initialize()

chicken = Food('chicken', 'oz', 7.0, 0.0, 1.0)
oats = Food('oats', 'grams', 0.0252, 0.1359, 0.0159)

chicken.save_to_mongo()
oats.save_to_mongo()

meal1 = Meal({'chicken': '8', 'oats': '234'})

print(meal1.json())
