from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):

    @api.doc('list of registered users', security='jwt')
    @api.marshal_list_with(_user, envelope='data')
    @admin_token_required
    def get(self):
        """ List all registered users """
        return get_all_users()

    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    def post(self):
        """ Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<uuid_user>')
@api.param('uuid_user', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):

    @api.doc('get a user', security='jwt')
    @api.marshal_with(_user)
    @token_required
    def get(self, uuid_user):
        """ Get a user given its identifier"""
        user = get_a_user(uuid_user)
        if not user:
            api.abort(404)
        else:
            return user
