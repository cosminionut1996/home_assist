import datetime
import uuid

from app.main import db
from app.main.model.user import User
from http import HTTPStatus


def save_new_user(data):
    """ data is a dictionary that contains
        public_id, email, username, password, registered_on """
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        return dict(
            error='User already exists. Please Log in.',
        ), HTTPStatus.CONFLICT


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user._uuid)
        return dict(
            data={
                'Authorization': auth_token.decode()
            },
        ), HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error',
        ), HTTPStatus.UNAUTHORIZED


def save_changes(data):
    db.session.add(data)
    db.session.commit()
