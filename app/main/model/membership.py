import uuid
from datetime import datetime

from sqlalchemy.orm import relationship

from .. import db
from ._common import GUID


class Membership(db.Model):
    """ Model for storing resource membership data """
    __tablename__ = "membership"

    _uuid = db.Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    uuid_member = db.Column(GUID)
    uuid_resource = db.Column(GUID)
    resource_type = db.Column(db.String(16))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
