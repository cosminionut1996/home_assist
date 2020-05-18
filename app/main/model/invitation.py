from .. import db


class Invitation(db.Model):
    """ Model for storing group invites """
    __tablename__ = "invitation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id_sender = db.Column(db.Integer)
    public_id_invitee = db.Column(db.Integer)
    resource_id = db.Column(db.Integer)
    resource_type = db.Column(db.String(16))
    status = db.Column(db.String(16))
    token = db.Column(db.String(64), unique=True)
