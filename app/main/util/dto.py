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
    # group_write = api.model('GroupUpdate', {
    #     'name': fields.String(required=False, description='The name of the group'),
    # })

    group_write = reqparse.RequestParser()
    group_write.add_argument('name', type=str, required=False, help='The name of the group')

    group_write_ret = api.model('GroupCreateRet', {
        'group': fields.Nested(group),
        'error': fields.String(description='Error message'),
    })


    # group_invitation = api.model('GroupInvitation', {
    #     'name': fields.String(required=True, description="Chosen group name"),
    #     'public_id_invitee': fields.String(required=True, description="The invited person's public id"),
    # })

    # group_invitation_create_ret = api.model('GroupInvitationCreateRet', {
    #     'group_invitation': fields.Nested(api.model('_GroupInvitation', {
    #         'public_id_invitee': fields.String(),
    #         'public_id_sender': fields.String(),
    #         'name': fields.String()
    #     })),
    #     'error': fields.String(description='Error message'),
    # })
