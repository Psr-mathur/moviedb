from flask import make_response, request
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request


def Jwt_required_custom(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        username = request.cookies.get("access_token_cookie")
