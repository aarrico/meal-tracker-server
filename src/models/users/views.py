from models.users.user import User, UserErrors
from flask import Blueprint, request, session, redirect, url_for, render_template

__author__ = 'aarrico'

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

    try:
        if User.is_login_valid(email, password):
            session['email'] = email
            return redirect(url_for(".user_profile"))
    except UserErrors.UserException as ex:
            return ex.message

    return render_template("users/login.html") #send user error if their login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

    try:
        if User.register_user(email, password):
            session['email'] = email
            return redirect(url_for(".user_profile"))
    except UserErrors.UserException as ex:
        return ex.message

    return render_template("users/register.html")  # send user error if their login was invalid


@user_blueprint.route('/profile')
def user_profile():
    pass


@user_blueprint.route('/get_meals/<string:user_id>')
def get_meals(user_id):
    pass


@user_blueprint.route('/logout')
def logout_user():
    pass

