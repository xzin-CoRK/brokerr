from flask import Blueprint, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import EqualTo, InputRequired, Length

import sys
sys.path.append('/brokerr')
from data import dataLayer
from utils import common

auth_blueprint = Blueprint("auth", __name__, template_folder="../templates")

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    
    error = None

    # Check if 'next' parameter is present
    next_url = request.args.get('next')
    if next_url:
        error = "You must be logged in to view that page"

    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=form, error=error)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        return redirect('/login')
    
    return render_template('register.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    pass


class RegisterForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(min=4, max=256)])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password')

class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    rememberMe = BooleanField('RememberMe')