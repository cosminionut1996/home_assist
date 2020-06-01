from .. import db
from datetime import datetime
from ._common import GUID
import uuid

class Membership(db.Model):
    """ Model for storing group membership data """
    __tablename__ = "membership"

    _uuid = db.Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    uuid_resource = db.Column(GUID)
    resource_type = db.Column(db.String(16))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
