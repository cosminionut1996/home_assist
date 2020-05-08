
from app.main import db
from app.main.model.blacklist import BlacklistToken
from http import HTTPStatus


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        return dict(), HTTPStatus.OK
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR
