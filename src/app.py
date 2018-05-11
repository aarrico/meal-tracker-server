from models.meals.views import meal_blueprint
from common.database import Database
from flask import Flask, render_template
from src.models.users.views import user_blueprint

__author__ = 'aarrico'

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "alex"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(meal_blueprint, url_prefix='/meals')
