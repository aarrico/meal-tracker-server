__author__ = 'aarrico'

from flask import Blueprint


food_blueprint = Blueprint('foods', __name__)

@food_blueprint.route('/food/<string:name>')
def food_page():
    pass


@food_blueprint.route('/new', methods=['POST'])
def create_food():
    pass