from flask import Blueprint, make_response, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

from database.db import create_user, verify_user

from base.jwt import make_jwt_payload, sign_jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

import logging
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        result = create_user(name, password, email)
        if result != "error":
            res = make_response(redirect(url_for('auth.login')))
            payload = make_jwt_payload(result)
            token = sign_jwt(payload)
            res.set_cookie('token', token, httponly=True, samesite='Strict',)
            return res
        else:
            return render_template('auth/register.html', error="Es ist ein fehler aufgetreten. Bitte versuche es erneut.")

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']      
        user = verify_user(email, password)
        if user != False:
            res = make_response(redirect(url_for('app.profile')))
            payload = make_jwt_payload(user[0])
            token = sign_jwt(payload)
            res.set_cookie('token', token, httponly=True, samesite='Strict')
            logger.info(f"User {user[0]} logged in successfully.")
            return res
        else:
            logger.warning(f"Failed login attempt for email: {email}")
            return render_template('auth/login.html', error="Passwort und E-Mail stimmen nicht überein. Bitte versuche es erneut.")

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    res = make_response(redirect(url_for('auth.logout_success')))
    res.delete_cookie('token')
    return res

@auth_bp.route('/logout_success', methods=['GET'])
def logout_success():
    return render_template('auth/logout.html')