import random
import unittest
import uuid
from http import HTTPStatus

from app.main import db
from app.main.model.invitation import InvitationStatus
from app.main.model.group import Group
from app.main.model.membership import Membership
from app.test.base import BaseTestCase

from app.main.service.group_service import get_groups

class TestGroupService(BaseTestCase):

    def test_get_groups(self):
        """ Test for group export """
        usr1 = uuid.uuid4()
        usr2 = uuid.uuid4()
        usr3 = uuid.uuid4()
        
        group1 = Group(
            uuid_creator=usr1,
            name='group1'
        )
        group2 = Group(
            uuid_creator=usr2,
            name='group2'
        )
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

        membership1 = Membership(
            uuid_member=usr2,
            uuid_resource=group1._uuid,
            resource_type='group'
        )
        membership2 = Membership(
            uuid_member=usr3,
            uuid_resource=group1._uuid,
            resource_type='group'
        )
        membership3 = Membership(
            uuid_member=usr3,
            uuid_resource=group2._uuid,
            resource_type='group'
        )
        db.session.add(membership1)
        db.session.add(membership2)
        db.session.add(membership3)
        db.session.commit()

        # Test get groups owned
        groups, status = get_groups(uuid_user=usr1, owned=True)
        self.assertEqual(groups[0]._uuid, group1._uuid)
        self.assertEqual(len(groups), 1)
        self.assertEqual(status, HTTPStatus.OK)

        # Test get groups user is member of
        groups, status = get_groups(uuid_user=usr3, member=True)
        self.assertEqual(len(groups), 2)
        self.assertEqual(status, HTTPStatus.OK)

        # Test bad request (owned or member not selected)
        groups, status = get_groups(uuid_user=usr1, name='group')
        self.assertEqual(groups, [])
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
