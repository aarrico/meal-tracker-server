import uuid

from flask import session

from common.database import Database
from models.meal import Meal
from models.user_profile import UserProfile

__author__ = 'aarrico'

collection = 'users'


class User(object):
    def __init__(self, email, password, user_profile=UserProfile(), _id=None):
        self.email = email
        self.password = password
        self.user_profile = user_profile
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection, {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection, {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password, name, protein, carbs, fat):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password, UserProfile(email, name, protein, carbs, fat))
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_meals(self, date=None):
        if date is None:
            return Meal.find_by_user_id(self.email)
        return Meal.find_by_date(self.email, date)

    def new_meal(self, foods):
        meal = Meal(self.email, foods, _id=self._id)
        meal.save_to_mongo()

    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password,
            'user_profile': self.user_profile.json()
        }

    def save_to_mongo(self):
        Database.insert(collection, self.json())

