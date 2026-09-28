from flask import jsonify, redirect, url_for

from .exceptions import APIException


class ErrorHandler:
    def __init__(self, app):
        app = app

        @app.errorhandler(APIException)
        def handle_exception(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return redirect(url_for('auth.login',), )