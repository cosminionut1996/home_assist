from flask_restplus import Namespace, fields, Model, reqparse
from flask_restplus.swagger import Model


class UserDto:
    api = Namespace('users', description='user related operations')
    user = api.model('User', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('AuthDetails', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class GroupDto:
    api = Namespace('groups', description='group related operations')

    group = api.model('Group', {
        'id': fields.Integer(description='Group numeric ID'),
        'creator_id': fields.Integer(description='Id of the user that created the group'),
        'date_created': fields.DateTime(description='Date of creation for the group'),
        'name': fields.String(required=True, description='The name of the group')
    })

    # Perform create / update ops only on those fields
    group_write = api.model('GroupUpdate', {
        'name': fields.String(description='The name of the group'),
    })

    group_post_parser = reqparse.RequestParser()
    group_post_parser.add_argument('name', type=str, required=True, location='json')

    group_patch_parser = reqparse.RequestParser()
    group_patch_parser.add_argument('name', type=str, required=False, location='json')

    group_write_ret = api.model('GroupCreateRet', {
        'group': fields.Nested(group),
        'error': fields.String(description='Error message'),
    })

class InvitationDto:
    api = Namespace('invitations', description='???')

    invitation = api.model('Invitation', {
        'id': fields.Integer(description='Invitation numeric ID'),
        'public_id_sender': fields.String(description='The id of the sender of the invitation'),
        'public_id_invitee': fields.String(description='The id of the invitee of the invitation'),
        'resource_id': fields.Integer(description='The id of the resource the invitation belongs to'),
        'resource_type': fields.String(description='The type of resource the invitation is associated with'),
        'token': fields.String(description='Token that can be used for accepting the invitation'),
        'status': fields.String(description='The status of the invitation')
    })
