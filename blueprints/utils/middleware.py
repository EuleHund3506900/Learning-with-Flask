from flask import request

from base.exceptions import APIException
from base.jwt import verify_jwt


class AuthMiddleware:

    @staticmethod
    def is_valid_token(token):
        try:
            verification = verify_jwt(token)
            if(verification is None):
                return False
            return True
        
        except Exception as e:
            return False

    def authenticate(self):
        auth_token = request.cookies.get('token')
        if not auth_token:
            raise APIException("Unauthorized", status_code=401)
        if not self.is_valid_token(auth_token):
            raise APIException("Unauthorized", status_code=401)


def require_authentication(func):
    def wrapper(*args, **kwargs):
        AuthMiddleware().authenticate()
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper