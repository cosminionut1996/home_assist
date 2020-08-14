import unittest
import uuid
from datetime import datetime

from app.main import db
from app.main.model.group import Group
from app.test.base import BaseTestCase


class TestGroupModel(BaseTestCase):

    def test_group_create(self):
        """ Test for group creation """
        new_uuid = uuid.uuid4()

        group = Group(
            uuid_creator=new_uuid,
            name='TestGroup'
        )
        db.session.add(group)
        db.session.commit()

        creation_date_no_seconds = group.date_created.replace(second=0, microsecond=0)
        now_no_seconds = datetime.utcnow().replace(second=0, microsecond=0)

        self.assertEqual(creation_date_no_seconds, now_no_seconds)
        self.assertEqual(group.uuid_creator, new_uuid)
        self.assertEqual(group.name, 'TestGroup')
        self.assertTrue(group._uuid)


if __name__ == '__main__':
    unittest.main()
