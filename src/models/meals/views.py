__author__ = 'aarrico'

from flask import Blueprint


meal_blueprint = Blueprint('meals', __name__)

@meal_blueprint.route('/meal/<string:date>')
def meal_page(date):
    pass


@meal_blueprint.route('/new', methods=['POST'])
def create_meal():
    pass