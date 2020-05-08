from functools import wraps

from flask import request

from app.main.service.auth_helper import get_logged_in_user
from http import HTTPStatus


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            return dict(
                error='Admin token required',
            ), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated
