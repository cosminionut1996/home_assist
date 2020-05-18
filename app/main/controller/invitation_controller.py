# from http import HTTPStatus

# from flask import request
# from flask_restplus import Resource

# from werkzeug.exceptions import BadRequest

# from ..model.user import User
# from ..service.auth_helper import get_logged_in_user
# from ..service.group_service import (create_group, create_group_invite,
#                                      delete_group, get_a_group, get_all_groups,
#                                      update_group)
# from ..util.decorator import token_required
# from ..util.dto import AuthDto, GroupDto


# group_invitation = GroupDto.group_invitation
# group_invitation_create_ret = GroupDto.group_invitation_create_ret


class Invitation(Resource):
    pass

class InvitationList(Resource):
    pass



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
