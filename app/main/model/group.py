from .. import db
from datetime import datetime
from ._common import GUID
import uuid

class Group(db.Model):
    """ Model for storing group data """
    __tablename__ = "group"

    _uuid = db.Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    uuid_creator = db.Column(GUID)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(64))
