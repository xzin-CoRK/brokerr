from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.form import Form
from wtforms.validators import EqualTo, InputRequired, Length, Regexp, ValidationError

import sys
sys.path.append('/brokerr')
from data import dataLayer
from utils import security
from data.model import User
from app.extensions import db

auth_blueprint = Blueprint("auth", __name__, template_folder="../templates")

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    error = None

    # Check if 'next' parameter is present
    next_url = request.args.get('next')
    if next_url:
        error = "You must be logged in to view that page"

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = dataLayer.get_user_by_username(username)

        if user and security.validate_password(user.hash, password):
            login_user(user, remember = remember)
            return redirect(url_for('home.home'))
        else:
            form.password.errors.append("Login failed, please try again.")
        
    return render_template('login.html', form=form, error=error)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        # Registration form is valid

        # First, create and add the user to the database
        username = form.username.data
        password = form.password.data
        hash = security.hash_pw(password)

        user = User(
            username = username,
            hash = hash
        )

        db.session.add(user)
        db.session.commit()

        # Now generate the master key
        security.generate_master_key(password)


        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


class RegisterForm(Form):

    complexity_regex = r'^(?=.*[A-Z])(?=.*[!@#$&*_;-^%])(?=.*[0-9])(?=.*[a-z]).{12}$'

    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match'),
        Regexp(complexity_regex,
            message='Password must have at least 12 characters, one lowercase, one uppercase, one digit, and one special character (any of !@#$&*_;-^%).'
        )])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # ensure unique usernames
        exists = dataLayer.get_user_by_username(username.data)
        if exists:
            raise ValidationError("That username already exists. Please choose a different username or use the Login link to access your account.")
        
    

class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    remember = BooleanField('Remember Me')