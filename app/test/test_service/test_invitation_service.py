import random
import unittest
from http import HTTPStatus

from app.main import db
from app.main.service.invitation_service import (create_group_invitation,
                                                 get_invitations,
                                                 rand_alphanum_str)
from app.main.service.user_service import save_new_user
from app.test.base import BaseTestCase
import uuid

class TestInvitationService(BaseTestCase):

    # def test_invitation_create_get(self):
    #     # Create the entry
    #     random.seed(1)
    #     ret, status = create_group_invitation(123, 456, 789)
    #     self.assertEqual(status, HTTPStatus.CREATED)
    #     inv_1 = {
    #         'id': 1,
    #         'uuid_sender': 123,
    #         'uuid_invitee': 456,
    #         'resource_type': 'group',
    #         'uuid_resource': 789,
    #         'token': rand_alphanum_str()
    #     }
    #     # Create the user
    #     save_new_user({
    #         'email': 'john@example.com',
    #         'username': 'john'
    #         'password': '123'
    #     })
    #     ret, status = get_invitation(1, 1)
    #     self.assertEqual(status, HTTPStatus.OK)

    def test_invitation_create_get_invitations(self):
        """ Test for group invitation creation and retrieval """
        random.seed(1)
        usr1 = uuid.uuid4()
        usr2 = uuid.uuid4()
        usr3 = uuid.uuid4()
        usr4 = uuid.uuid4()
        grp1 = uuid.uuid4()
        grp2 = uuid.uuid4()
        grp3 = uuid.uuid4()

        # Create the entry
        inv1, status = create_group_invitation(usr1, usr2, grp1)
        self.assertEqual(status, HTTPStatus.CREATED)

        # Create other entries
        inv2, _ = create_group_invitation(usr3, usr2, grp2)
        inv3, _ = create_group_invitation(usr1, usr4, grp1)
        inv4, _ = create_group_invitation(usr2, usr1, grp3)

        random.seed(1)
        # Create expected responses
        inv_1 = {
            '_uuid': inv1.get('_uuid'),
            'uuid_sender': usr1,
            'uuid_invitee': usr2,
            'uuid_resource': grp1,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        inv_2 = {
            '_uuid': inv2.get('_uuid'),
            'uuid_sender': usr3,
            'uuid_invitee': usr2,
            'uuid_resource': grp2,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        inv_3 = {
            '_uuid': inv3.get('_uuid'),
            'uuid_sender': usr1,
            'uuid_invitee': usr4,
            'uuid_resource': grp1,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        inv_4 = {
            '_uuid': inv4.get('_uuid'),
            'uuid_sender': usr2,
            'uuid_invitee': usr1,
            'uuid_resource': grp3,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        resp_1 = [inv_1, inv_3]
        resp_2 = [inv_1, inv_2]
        resp_3 = [inv_1, inv_2, inv_4]

        # Query the entry and make sure it's being returned correctly
        invitations, status = get_invitations(uuid_sender=usr1, resource_type='group')
        for expected, invitation in zip(resp_1, invitations):
            for key, value in expected.items():
                self.assertEqual(getattr(invitation, key), value)
        self.assertEqual(status, HTTPStatus.OK)

        invitations, status = get_invitations(uuid_invitee=usr2)
        for expected, invitation in zip(resp_2, invitations):
            for key, value in expected.items():
                self.assertEqual(getattr(invitation, key), value)
        self.assertEqual(status, HTTPStatus.OK)

        invitations, status = get_invitations(uuid_invitee=usr2, uuid_sender=usr2, resource_type='group')
        for expected, invitation in zip(resp_3, invitations):
            for key, value in expected.items():
                self.assertEqual(getattr(invitation, key), value)
        self.assertEqual(status, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
