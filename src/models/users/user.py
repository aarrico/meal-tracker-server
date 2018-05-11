import uuid
from flask import session
from common.database import Database
from common.utils import Utils
from models.meals.meal import Meal
from models.users.user_profile import UserProfile
import models.users.errors as UserErrors
import models.users.constants as UserConstants

__author__ = 'aarrico'


class User(object):
    def __init__(self, email, password, user_profile=None, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.user_profile = UserProfile(self._id) if user_profile is None else user_profile

    def __repr__(self):
        return "<User {}>".format(self.email)

    def get_id(self):
        return self._id

    def get_name(self):
        return self.user_profile['name']

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(UserConstants.COLLECTION, {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def is_login_valid(email, password):
        user_data = User.get_by_email(email)
        if user_data is None:
            raise UserErrors.UserNotExistException("User {} does not exist".format(email))
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordException("Password incorrect.  Try again.")
        return True

    @classmethod
    def register_user(cls, email, password, name, protein, carbs, fat):
        user_data = cls.get_by_email(email)
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredException("{} is already in use.".format(email))
        if not Utils.is_email_valid(email):
            raise UserErrors.InvalidEmailException("{} is not valid.".format(email))

        new_user = cls(email, Utils.hash_password(password))
        new_user.user_profile = UserProfile(new_user._id, name, protein, carbs, fat)
        new_user.user_profile.save_profile()
        new_user.save_to_mongo()
        return True

    @staticmethod
    def login(user_email):
        session['email'] = user_email
        return User.get_by_email(user_email)

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
        Database.insert(UserConstants.COLLECTION, self.json())

