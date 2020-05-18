from http import HTTPStatus

from app.main import db
from app.main.model.invitation import Invitation


def create_group_invitation(public_id_sender, public_id_invitee, group_id):
    group_invite = Invitation(
        public_id_sender=public_id_sender,
        public_id_invitee=public_id_invitee,
        resource_type='group',
        resource_id=group_id,
        token='hello'   # TODO: Generate random token
    )
    try:
        db.session.add(group_invite)
        db.session.commit()
        return {
            x: getattr(group_invite, x)
            for x in (
                'id',
                'public_id_sender',
                'public_id_invitee',
                'resource_type',
                'resource_id',
                'token'
            )
        }, HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR


def accept_group_invitation():
    pass

def decline_group_invitation():
    pass

def get_invitations(public_id, resource_type=None):
    qr = Invitation.query.filter_by(public_id_invitee=public_id).all()
    return qr, HTTPStatus.OK if qr else HTTPStatus.NOT_FOUND
