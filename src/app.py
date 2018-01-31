import datetime

__author__ = 'aarrico'

from models.user import User, Meal
from common.database import Database
from flask import Flask, request, render_template, session

app = Flask(__name__)
app.secret_key = "alex"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/register')
def render_register():
    return render_template('register.html')


@app.route('/login')
def render_login():
    return render_template('login.html')


@app.route('/auth/register', methods=['POST'])
def register_user():
    try:
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        protein = request.form['protein']
        carbs = request.form['carbs']
        fat = request.form['fat']

    except KeyError as error:
        print("Error getting form from HTML: " + error)
        

    User.register(email, password, name, protein, carbs, fat)

    return render_template('profile.html', email=session['email'])


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])


@app.route('/meals/<string>:user_id')
@app.route('/meals')
def user_meals(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    date = datetime.datetime.utcnow()
    meals = user.get_meals(date=date)

    return render_template("user_meals.html", meals=meals, name=user.user_profile['name'], date=date.date())


if __name__ == '__main__':
    app.run()


#chicken = Food('chicken', 'oz', 7.0, 0.0, 1.0)
#oats = Food('oats', 'grams', 0.0252, 0.1359, 0.0159)

#chicken.save_to_mongo()
#oats.save_to_mongo()

#meal1 = Meal({'chicken': '8', 'oats': '234'})

#print(meal1.json())
