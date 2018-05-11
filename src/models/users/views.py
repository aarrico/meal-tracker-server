from datetime import datetime
from models.users.user import User, UserErrors
from flask import Blueprint, request, session, redirect, url_for, render_template
from models.users.user_profile import UserProfile
import models.users.decorators as user_decorators

__author__ = 'aarrico'

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_profile"))
        except UserErrors.UserException as ex:
                return ex.message

    return render_template("users/login.jinja2")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        protein = request.form['protein']
        carbs = request.form['carbs']
        fat = request.form['fat']

        try:
            if User.register_user(email, password, name, protein, carbs, fat):
                session['email'] = email
                return redirect(url_for(".user_profile"))
        except UserErrors.UserException as ex:
            return ex.message

    return render_template("users/register.jinja2")  # send user error if their login was invalid


@user_blueprint.route('/profile')
@user_decorators.requires_login
def user_profile():
    pass


@user_blueprint.route('/update/macros')
@user_decorators.requires_login
def update_macros():
    user = User.get_by_email(session['email'])
    user.user_profile = UserProfile(user.get_id(),
                                    user.get_name(),
                                    request.form['protein'],
                                    request.form['carbs'],
                                    request.form['fat'])
    user.user_profile.save_profile()
    return render_template('users/profile.jinja2', profile=user.user_profile)


@user_blueprint.route('/meals')
@user_decorators.requires_login
def get_meals():
    user = User.get_by_email(session['email'])
    meals = user.get_meals()
    return render_template('meals/user_meals.jinja2', name=user.get_name(), date=datetime.today(), meals=meals)


@user_blueprint.route('/logout')
@user_decorators.requires_login
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))
