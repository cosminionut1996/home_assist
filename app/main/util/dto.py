from flask_restx import Namespace, fields, Model, reqparse
from flask_restx.swagger import Model


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

    groups_fetch = reqparse.RequestParser()
    groups_fetch.add_argument('owned', type=bool, location='args', help='Return the groups owned by the user')
    groups_fetch.add_argument('member', type=bool, location='args', help='Return the groups the user is a member of')
    groups_fetch.add_argument('name', type=str, location='args', help='Filter only the groups that contain this name')

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

    invitation_create = api.parser()
    invitation_create.add_argument('resource_type', type=str, location='json', help="The resource's type the invitation is associated with")
    invitation_create.add_argument('username_invitee', type=str, location='json', help="The username of the user that will receive the invitation")
    invitation_create.add_argument('uuid_resource', type=str, location='json', help="The resource the recipient of the invitation is invited to")

    invitations_fetch = api.parser()
    invitations_fetch.add_argument('received', type=bool, location='args', help='Return the invitations received by the user')
    invitations_fetch.add_argument('resource_type', type=str, location='args', help='The type of resource the invitation is associated with')
    invitations_fetch.add_argument('sent', type=bool, location='args', help='Return the invitations sent by the user')
