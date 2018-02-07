import datetime

from models.user_profile import UserProfile

__author__ = 'aarrico'

from models.user import User
from common.database import Database
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "alex"


@app.before_first_request
def initialize_database():
    Database.initialize()

# RENDERING METHODS


@app.route('/')
def redirect_login():
    session['invalid'] = False
    return render_login()


@app.route('/register')
def render_register():
    return render_template('register.html')


@app.route('/login')
def render_login():
    return render_template('login.html', invalid=session['invalid'])


@app.route('/update')
def render_update():
    return render_template('update_macros.html')

# LOGIN METHODS


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

    return render_template('profile.html', name=name)


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        user = User.login(email)
        session['invalid'] = False
    else:
        session['email'] = None
        session['invalid'] = True
        return redirect(url_for('render_login'))

    return render_template('profile.html', profile=user.user_profile)

# MEAL METHODS


@app.route('/meals')
@app.route('/meals/<string:user_id>')
def user_meals(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    date = datetime.datetime.utcnow()
    meals = user.get_meals(date=date)

    return render_template("user_meals.html", meals=meals, name=user.get_name(), date=date.date())


@app.route('/update/macros')
def update_macros():
    user = User.get_by_email(session['email'])
    user.user_profile = UserProfile(user.get_id(),
                                    user.get_name(),
                                    request.form['protein'],
                                    request.form['carbs'],
                                    request.form['fat'])
    user.user_profile.save_profile()
    return render_template('profile.html', profile=user.user_profile)


if __name__ == '__main__':
    app.run()
