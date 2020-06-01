from flask_restplus import Namespace, fields, Model, reqparse
from flask_restplus.swagger import Model


class UserDto:
    api = Namespace('users', description='user related operations')
    user = api.model('User', {
        '_uuid': fields.String(description='User UUID'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
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
        '_uuid': fields.String(description='Group UUID'),
        'uuid_creator': fields.String(description='uuid of the user that created the group'),
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
    api = Namespace('invitations', description='invitation related operations')

    invitation = api.model('Invitation', {
        '_uuid': fields.String(description='Invitation UUID'),
        'uuid_sender': fields.String(description='The uuid of the sender of the invitation'),
        'uuid_invitee': fields.String(description='The uuid of the invitee of the invitation'),
        'uuid_resource': fields.String(description='The uuid of the resource the invitation belongs to'),
        'resource_type': fields.String(description='The type of resource the invitation is associated with'),
        'token': fields.String(description='Token that can be used for accepting the invitation'),
        'status': fields.String(description='The status of the invitation')
    })

    invitations_fetch = api.model('InvitationFetch', {
        'received': fields.Boolean(description='Return the invitations received by the user'),
        'sent': fields.Boolean(description='Return the invitations sent by the user'),
        'resource_type': fields.String(description='The type of resource the invitation is associated with')
    })
