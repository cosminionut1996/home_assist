import random
import unittest
import uuid
from http import HTTPStatus

from app.main import db
from app.main.model.invitation import InvitationStatus
from app.main.model.user import User
from app.main.service.invitation_service import (accept_invitation,
                                                 create_invitation,
                                                 reject_invitation,
                                                 get_invitations,
                                                 rand_alphanum_str)
from app.main.service.user_service import save_new_user
from app.test.base import BaseTestCase


class TestInvitationService(BaseTestCase):

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
        inv1, status = create_invitation(usr1, usr2, grp1, 'group')
        self.assertEqual(status, HTTPStatus.CREATED)

        # Create other entries
        inv2, _ = create_invitation(usr3, usr2, grp2, 'group')
        inv3, _ = create_invitation(usr1, usr4, grp1, 'group')
        inv4, _ = create_invitation(usr2, usr1, grp3, 'group')

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

    def test_invitation_create_accept_invitation(self):
        """ Test for group invitation creation and accept """
        usr1 = uuid.uuid4()
        usr2 = uuid.uuid4()
        usr3 = uuid.uuid4()
        grp1 = uuid.uuid4()

        random.seed(1)
        inv1, status = create_invitation(usr1, usr2, grp1, 'group')
        self.assertEqual(status, HTTPStatus.CREATED)
        inv2, status = create_invitation(usr1, usr3, grp1, 'group')
        self.assertEqual(status, HTTPStatus.CREATED)

        random.seed(1)
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
            'uuid_sender': usr1,
            'uuid_invitee': usr3,
            'uuid_resource': grp1,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        resp_1 = [inv_1, inv_2]

        # Query the entry and make sure it's being returned correctly
        invitations, status = get_invitations(uuid_sender=usr1, resource_type='group')
        for expected, invitation in zip(resp_1, invitations):
            for key, value in expected.items():
                self.assertEqual(getattr(invitation, key), value)
        self.assertEqual(status, HTTPStatus.OK)

        # Accept an invitation that does not exist
        ret, status = accept_invitation(usr2, uuid.uuid4())
        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(ret['error'], 'Invitation not found.')

        # Accept an invitation by an user that should not be able to respond to it
        ret, status = accept_invitation(usr1, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'User not allowed to reject an invitation he is not the receiver of.')

        # Simple invitation accept
        ret, status = accept_invitation(usr2, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(ret['status'], InvitationStatus.ACCEPTED)

        # Accept invitation twice
        ret, status = accept_invitation(usr2, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'Cannot accept an invitation twice.')

        # Accept an ivitation that was previously declined
        reject_invitation(usr3, inv_2['_uuid'])
        ret, status = accept_invitation(usr3, inv_2['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'Cannot accept an invitation that has been rejected.')

    def test_invitation_create_reject_invitation(self):
        """ Test for group invitation creation and decline """
        usr1 = uuid.uuid4()
        usr2 = uuid.uuid4()
        usr3 = uuid.uuid4()
        grp1 = uuid.uuid4()

        random.seed(1)
        inv1, status = create_invitation(usr1, usr2, grp1, 'group')
        self.assertEqual(status, HTTPStatus.CREATED)
        inv2, status = create_invitation(usr1, usr3, grp1, 'group')
        self.assertEqual(status, HTTPStatus.CREATED)

        random.seed(1)
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
            'uuid_sender': usr1,
            'uuid_invitee': usr3,
            'uuid_resource': grp1,
            'resource_type': 'group',
            'token': rand_alphanum_str()
        }

        resp_1 = [inv_1, inv_2]

        # Query the entry and make sure it's being returned correctly
        invitations, status = get_invitations(uuid_sender=usr1, resource_type='group')
        for expected, invitation in zip(resp_1, invitations):
            for key, value in expected.items():
                self.assertEqual(getattr(invitation, key), value)
        self.assertEqual(status, HTTPStatus.OK)

        # Decline an invitation that does not exist
        ret, status = reject_invitation(usr2, uuid.uuid4())
        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(ret['error'], 'Invitation not found.')

        # Decline an invitation by an user that should not be able to respond to it
        ret, status = reject_invitation(usr1, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'User not allowed to reject an invitation he is not the receiver of.')

        # Simple invitation decline
        ret, status = reject_invitation(usr2, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(ret['status'], InvitationStatus.REJECTED)

        # Decline invitation twice
        ret, status = reject_invitation(usr2, inv_1['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'Cannot reject an invitation twice.')

        # Decline an invitation that was previously accepted
        accept_invitation(usr3, inv_2['_uuid'])
        ret, status = reject_invitation(usr3, inv_2['_uuid'])
        self.assertEqual(status, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(ret['error'], 'Cannot reject an invitation that has been accepted.')

if __name__ == '__main__':
    unittest.main()
