import datetime

from models.meals.meal import Meal
from models.users.user import User
from flask import Blueprint, session, render_template, request, make_response

__author__ = 'aarrico'

meal_blueprint = Blueprint('meals', __name__)


@meal_blueprint.route('/meal/<string:date>')
def meal_page(date):
    pass


@meal_blueprint.route('/meals')
@meal_blueprint.route('/meals/<string:user_id>')
def user_meals(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    date = datetime.datetime.utcnow()
    meals = user.get_meals(date=date)

    return render_template("user_meals.jinja2", meals=meals, name=user.get_name(), date=date.date())


@meal_blueprint.route('/meals/new', methods=['POST', 'GET'])
def create_new_meal():
    if request.method == 'GET':
        return render_template('new_meal.html')
    else:
        user = User.get_by_email(session['email'])
        foods = request.form(['foods'])

        new_meal = Meal(user._id, foods)
        new_meal.save_to_mongo()

        return make_response(user_meals(user._id))