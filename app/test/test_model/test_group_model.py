import unittest

from app.main import db
from app.main.model.group import Group
from app.test.base import BaseTestCase
from datetime import datetime

class TestGroupModel(BaseTestCase):

    def test_group_create(self):
        """ Test for group creation """
        group = Group(
            creator_id=123,
            name='TestGroup'
        )
        db.session.add(group)
        db.session.commit()

        creation_date_no_seconds = group.date_created.replace(second=0, microsecond=0)
        now_no_seconds = datetime.utcnow().replace(second=0, microsecond=0)

        self.assertEqual(creation_date_no_seconds, now_no_seconds)
        self.assertEqual(group.creator_id, 123)
        self.assertEqual(group.name, 'TestGroup')
        self.assertTrue(group.id)


if __name__ == '__main__':
    unittest.main()
