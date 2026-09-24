from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

from database.db import create_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        result = create_user(name, password, email)
        if result == "success":
            return redirect(url_for('app.profile'))
        else:
            return render_template('auth/register.html', error="Es ist ein fehler aufgetreten. Bitte versuche es erneut.")

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        from database.db import verify_user
        if verify_user(email, password):
            return redirect(url_for('app.profile'))
        else:
            return render_template('auth/login.html', error="Passwort und E-Mail stimmen nicht überein. Bitte versuche es erneut.")

    return render_template('auth/login.html')