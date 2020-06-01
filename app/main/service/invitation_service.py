from http import HTTPStatus

from app.main import db
from app.main.model.invitation import Invitation, InvitationStatus
from app.main.model.membership import Membership
from app.main.model.user import User

import random
import string


def rand_alphanum_str(stringLength=64):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def create_group_invitation(uuid_sender, uuid_invitee, uuid_group):
    group_invite = Invitation(
        uuid_sender=uuid_sender,
        uuid_invitee=uuid_invitee,
        uuid_resource=uuid_group,
        resource_type='group',
        status=InvitationStatus.PENDING,
        token=rand_alphanum_str()
    )
    try:
        db.session.add(group_invite)
        db.session.commit()
        return {
            x: getattr(group_invite, x)
            for x in (
                '_uuid',
                'uuid_sender',
                'uuid_invitee',
                'resource_type',
                'uuid_resource',
                'status',
                'token'
            )
        }, HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def accept_group_invitation():
    pass

def decline_group_invitation(uuid_invitee, uuid_invitation):
    """ Impersonates an invitee to decline a group invitation and
        updates it's status.
    """
    invitation = Invitation.query.filter_by(_uuid=uuid_invitation).first()
    if not invitation:
        return dict(
            error='Invitation not found.'
        ), HTTPStatus.NOT_FOUND
    if invitation.status == InvitationStatus.ACCEPTED:
        return dict(
            error='Cannot decline an invitation that has been accepted.'
        ), HTTPStatus.METHOD_NOT_ALLOWED
    if invitation.status == InvitationStatus.REJECTED:
        return dict(
            error="Cannot decline an invitation twice."
        ), HTTPStatus.METHOD_NOT_ALLOWED
    if invitation.uuid_invitee == uuid_invitee:
        invitation.status = InvitationStatus.REJECTED
        db.session.add(invitation)
        db.session.commit()
        return {
            x: getattr(invitation, x)
            for x in (
                '_uuid',
                'uuid_sender',
                'uuid_invitee',
                'resource_type',
                'uuid_resource',
                'status',
                'token'
            )
        }, HTTPStatus.OK
    else:
        return dict(
            error='User not allowed to reject an invitation he is not the receiver of.'
        ), HTTPStatus.METHOD_NOT_ALLOWED

# def get_invitation(invitation_id, user_id):
#     """ Get an invitation if the user has privilege to see it or is an admin """
#     qr = Invitation.query \
#         .filter(Invitation.id == invitation_id) \
#         .join(User, (
#             (User.id == user_id)
#             & ( (User.public_id == Invitation.uuid_sender) 
#                 | (User.public_id == Invitation.uuid_invitee)))) \
#         .first()
#     return qr, HTTPStatus.OK if qr else HTTPStatus.NOT_FOUND

def get_invitations(
    uuid_invitee=None,
    uuid_sender=None,
    resource_type=None
):
    """
    Queries the invitations table
    if no public_ids parameters are given, return all invitations
    if uuid_invitee is given, it will search for the invitations received by this user
    if uuid_sender is given, it will search for the invitations sent by this user
    if both public_ids are given it will search for the invitations sent or received by this user
    if resource_type is given, it will search for the invitations for this resource type

    returns a list of invitations
    """
    qr = Invitation.query

    if uuid_invitee and uuid_sender:
        qr = qr.filter(
            (Invitation.uuid_invitee==uuid_invitee) 
            | (Invitation.uuid_sender==uuid_sender)
        )
    elif uuid_invitee:
        qr = qr.filter_by(uuid_invitee=uuid_invitee)
    elif uuid_sender:
        qr = qr.filter_by(uuid_sender=uuid_sender)

    if resource_type:
        qr = qr.filter_by(resource_type=resource_type)

    qr = qr.all()

    return qr, HTTPStatus.OK if qr else HTTPStatus.NOT_FOUND
