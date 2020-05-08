from .. import db
from datetime import datetime


class Group(db.Model):
    """ Model for storing group data """
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(64))


class GroupInvite(db.Model):
    """ Model for storing group invites """
    __tablename__ = "group_invite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id_sender = db.Column(db.String(100), unique=True)
    public_id_invitee = db.Column(db.String(100), unique=True)
    group_id = db.Column(db.Integer)
    token = db.Column(db.String(64), unique=True)
