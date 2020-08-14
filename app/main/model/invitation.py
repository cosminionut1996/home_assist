import uuid

from .. import db
from ._common import GUID


class Invitation(db.Model):
    """ Model for storing group invites """
    __tablename__ = "invitation"

    _uuid = db.Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    uuid_sender = db.Column(GUID)
    uuid_invitee = db.Column(GUID)
    uuid_resource = db.Column(GUID)
    resource_type = db.Column(db.String(16))
    status = db.Column(db.String(16))
    token = db.Column(db.String(64), unique=True)

class InvitationStatus:

    ACCEPTED = 'accepted'
    PENDING = 'pending'
    REJECTED = 'rejected'
