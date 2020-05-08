from http import HTTPStatus

from flask import request
from flask_restplus import Resource

from werkzeug.exceptions import BadRequest

from ..model.user import User
from ..service.auth_helper import get_logged_in_user
from ..service.group_service import (create_group, create_group_invite,
                                     delete_group, get_a_group, get_all_groups,
                                     update_group)
from ..util.decorator import token_required
from ..util.dto import AuthDto, GroupDto

api = GroupDto.api
group = GroupDto.group
group_write = GroupDto.group_write
group_write_ret = GroupDto.group_write_ret

# group_invitation = GroupDto.group_invitation
# group_invitation_create_ret = GroupDto.group_invitation_create_ret


@api.route('/<group_id>')
class Group(Resource):
    """ Group Resource """

    @api.doc('Export a group', security='jwt')
    @api.marshal_with(group)
    @token_required
    def get(self, group_id):
        """ Export a group """
        group_id = int(group_id)
        return get_a_group(group_id)

    @api.doc('Delete a group', security='jwt')
    @token_required
    def delete(self, group_id):
        """ Delete a group """
        group_id = int(group_id)
        auth_token = request.headers.get('Authorization')
        creator_id = User.decode_auth_token(auth_token)
        return delete_group(group_id, creator_id)

    @api.doc('Update a group', security='jwt')
    @api.expect(group_write, validate=True)
    @api.response(400, 'Bad Request')
    @api.marshal_with(group_write_ret)
    @token_required
    def patch(self, group_id):
        """ Update a group """
        try:
            data = group_write.parse_args(strict=True)
        except BadRequest:
            return dict(
                error="Bad Request"
            ), HTTPStatus.BAD_REQUEST
        else:
            group_id = int(group_id)
            auth_token = request.headers.get('Authorization')
            creator_id = User.decode_auth_token(auth_token)
            return update_group(data, group_id, creator_id)


@api.route('/')
class GroupList(Resource):
    """ Group List Resource """

    @api.doc('Create a new group', security='jwt')
    @api.expect(group_write)
    @api.response(404, 'Unexpected input')
    @api.marshal_with(group_write_ret)
    @token_required
    def post(self):
        """ Create a new group """
        post_data = request.json
        auth_token = request.headers.get('Authorization')
        creator_id = User.decode_auth_token(auth_token)
        return create_group(post_data, creator_id)

    @api.doc('Returns all the groups', security='jwt')
    @api.marshal_list_with(group)
    @token_required
    def get(self):
        """ Return all groups """
        return get_all_groups()


# class GroupInvite(Resource):
#     """ Group Invite Resource """

#     @api.doc('Export a group invite', security='jwt')
#     @api.route('/group/<string:group_id>/invite/<string:invite_id>')
#     def get(self):
#         """ Return a group """
#         return request.json


# @api.route('/<group_id>/invitations')
# @api.param('group_id', 'Group id for which an invitation will be created')
# class GroupInvitationList(Resource):
    
#     """ Group Invitation Resource """
#     @api.doc("Invite a user to the owner's group", security='jwt')
#     @api.expect(group_invitation)
#     @api.marshal_with(group_invitation_create_ret)
#     @token_required
#     def post(self, group_id):
#         """ Create a new group """
#         post_data = request.json
#         auth_token = request.headers.get('Authorization')
#         public_id_sender = User.decode_auth_token(auth_token)
#         return create_group_invite(
#             public_id_sender,
#             post_data['public_id_invitee'],
#             group_id
#         )
