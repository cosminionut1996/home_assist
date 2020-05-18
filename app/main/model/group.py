from .. import db
from datetime import datetime


class Group(db.Model):
    """ Model for storing group data """
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(64))
