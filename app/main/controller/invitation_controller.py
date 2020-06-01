# from http import HTTPStatus

from flask import request
from flask_restplus import Resource

from ..service.invitation_service import get_invitations
# from ..model.user import User
from ..service.auth_helper import get_logged_in_user
from ..util.decorator import token_required
from ..util.dto import InvitationDto

# from werkzeug.exceptions import BadRequest

api = InvitationDto.api
invitation = InvitationDto.invitation
invitations_fetch = InvitationDto.invitations_fetch


# @api.route('/invitations/<invitation_id>')
# @api.param('invitation_id', 'Invitation id')
# class Invitation(Resource):
#     """ Invitation Resource """

#     @api.doc('Export an invitation', security='jwt')
#     @api.expect(invitation_fetch)
#     @api.marshal_with(invitation)
#     @token_required
#     def get(self, invitation_id):
#         """ Return a group """
#         post_data = request.json
#         return get_invitation(invitation_id, request.user_id)

@api.route('/invitations')
class InvitationList(Resource):
    """ Invitation List Resource """

    @api.doc('Export a list of invitations according to the parameters provided')
    @api.expect(invitations_fetch)
    @api.marshal_with(invitation)
    @token_required
    def get(self):
        received = request.args.get('received')
        sent = request.args.get('sent')
        resource_type = request.args.get('resource_type')
        return get_invitations(
            request.user._uuid if received else None,
            request.user._uuid if sent else None,
            resource_type
        )

    # @api.doc("Invite a user to the owner's resource", security='jwt')
    # @api.expect(group_invitation)
    # @api.marshal_with(invitation)
    # @token_required
    # def post(self):
    #     """ Create a new group """
    #     post_data = request.json
    #     auth_token = request.headers.get('Authorization')
    #     public_id_sender = User.decode_auth_token(auth_token)
    #     return create_group_invitation(
    #         public_id_sender,
    #         post_data['public_id_invitee'],
    #         group_id
    #     )



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
