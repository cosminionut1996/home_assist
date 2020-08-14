from app.main.model.user import User

from ..service.blacklist_service import save_token
from http import HTTPStatus
import uuid


def login_user(data):
    try:
        # fetch the user data
        user = User.query.filter_by(email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            auth_token = User.encode_auth_token(user._uuid)
            if auth_token:
                return dict(
                    data={
                        'Authorization': auth_token.decode()
                    }
                ), HTTPStatus.OK
        else:
            return dict(
                error='email or password does not match.'
            ), HTTPStatus.FORBIDDEN

    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def logout_user(data):
    if data:
        auth_token = data.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if resp == 'Token blacklisted. Please log in again.':
            return dict(error=resp), HTTPStatus.FORBIDDEN
        if not isinstance(resp, str):
            # mark the token as blacklisted
            return save_token(token=auth_token)
        else:
            dict(
                error='Bad authentication token'
            ), HTTPStatus.UNAUTHORIZED
    else:
        dict(
            error='Provide a valid auth token'
        ), HTTPStatus.FORBIDDEN

def get_logged_in_user(new_request):
    # get the auth token
    auth_token = new_request.headers.get('Authorization')
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(_uuid=resp).first()
            new_request.user = user
            return dict(
                data={
                    '_uuid': user._uuid,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': str(user.registered_on)
                }
            ), HTTPStatus.OK
        return dict(
            error='Bad authentication token'
        ), HTTPStatus.UNAUTHORIZED
    else:
        return dict(
            error='Provide a valid auth token'
        ), HTTPStatus.UNAUTHORIZED
