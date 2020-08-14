from http import HTTPStatus

from flask import request
from flask_restx import Resource

# from ..model.user import User
from ..service.auth_helper import get_logged_in_user
from ..service.invitation_service import (accept_invitation, create_invitation,
                                          get_invitations, reject_invitation)
from ..util.decorator import token_required
from ..util.dto import InvitationDto

# from werkzeug.exceptions import BadRequest

api = InvitationDto.api
invitation = InvitationDto.invitation
invitations_fetch = InvitationDto.invitations_fetch
invitation_create = InvitationDto.invitation_create


@api.route('/<invitation_uuid>/accept')
@api.param('invitation_uuid', 'Invitation uuid')
@api.response(HTTPStatus.NOT_FOUND, 'Invitation not found.')
@api.response(
    HTTPStatus.METHOD_NOT_ALLOWED,
    'Cannot accept an invitation that has been rejected, ' \
    'Cannot accept an invitation twice, ' \
    'User not allowed to accept an invitation he is not the receiver of'
)
@api.response(HTTPStatus.OK, 'Successfully accepted an invitation.')
class InvitationAccept(Resource):
    """ Invitation Resource """

    @api.doc('Accept a specific invitation received by the logged in user',
             security='jwt')
    @api.marshal_with(invitation)
    @token_required
    def post(self, invitation_uuid):
        """ Accept an invitation if the user can perform the action
            and return the updated invitation """
        return accept_invitation(
            request.user._uuid,
            invitation_uuid
        )

@api.route('/<invitation_uuid>/reject')
@api.param('invitation_uuid', 'Invitation uuid')
@api.response(HTTPStatus.NOT_FOUND, 'Invitation not found.')
@api.response(
    HTTPStatus.METHOD_NOT_ALLOWED,
    'Cannot reject an invitation that has been accepted, ' \
    'Cannot reject an invitation twice, ' \
    'User not allowed to reject an invitation he is not the receiver of'
)
@api.response(HTTPStatus.OK, 'Successfully rejected an invitation.')
class InvitationReject(Resource):
    """ Invitation Resource """

    @api.doc('Reject a specific invitation received by the logged in user',
             security='jwt')
    @api.marshal_with(invitation)
    @token_required
    def post(self, invitation_uuid):
        """ Reject an invitation if the user can perform the action
            and return the updated invitation """
        return reject_invitation(
            request.user._uuid,
            invitation_uuid
        )

@api.route('/<invitation_uuid>')
@api.param('invitation_uuid', 'Invitation uuid')
@api.response(HTTPStatus.NOT_FOUND, 'Invitation not found.')
@api.response(HTTPStatus.OK, 'Found the desired invitation.', invitation)
class Invitation(Resource):
    """ Invitation Resource """

    @api.doc('Export an invitation', security='jwt')
    @api.marshal_with(invitation)
    @token_required
    def get(self, invitation_uuid):
        """ Return an invitation if the user has access to it """
        return get_invitation(
            request.user._uuid,
            invitation_uuid
        )


@api.route('')
@api.response(HTTPStatus.NOT_FOUND, 'No invitations were found.')
@api.response(HTTPStatus.BAD_REQUEST, 'Improper API usage.')
@api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Unexpected error.')
class InvitationList(Resource):
    """ Invitation List Resource """

    @api.doc('Export a list of invitations according to the parameters provided',
             security='jwt')
    @api.expect(invitations_fetch)
    @api.marshal_with(invitation)
    @api.response(HTTPStatus.OK, 'Found a list of invitations', invitation)
    @token_required
    def get(self):
        """ Export invitations """
        received = request.args.get('received')
        sent = request.args.get('sent')
        resource_type = request.args.get('resource_type')
        return get_invitations(
            request.user._uuid if received else None,
            request.user._uuid if sent else None,
            resource_type
        )

    @api.doc("Invite a user to the owner's resource",
             security='jwt')
    @api.expect(invitation_create)
    @api.marshal_with(invitation)
    @api.response(HTTPStatus.CREATED, 'Successfully invited a user to the resource.', invitation)
    @token_required
    def post(self):
        """ Create a new invitation """
        return create_invitation(
            request.user._uuid,
            request.json.get('username_invitee'),
            request.json.get('uuid_resource'),
            request.json.get('resource_type'),
            invitation_mode='username'
        )
