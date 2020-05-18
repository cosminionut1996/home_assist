import unittest
from http import HTTPStatus

from app.main import db
from app.main.service.invitation_service import (create_group_invitation,
                                                 get_invitations)
from app.test.base import BaseTestCase


class TestInvitationService(BaseTestCase):

    def test_invitation_create_fetch(self):
        """ Test for group invitation creation and retrieval """
        ret, status = create_group_invitation(123, 456, 789)
        expected = {
            'id': 1,
            'public_id_sender': 123,
            'public_id_invitee': 456,
            'resource_type': 'group',
            'resource_id': 789,
            'token': 'hello'        # TODO: Test using seed when updating create_group_invitation
        }
        # Create the entry
        self.assertEqual(ret, expected)
        self.assertEqual(status, HTTPStatus.CREATED)

        # Query the entry and make sure it's being returned correctly
        invitations, status = get_invitations(456)
        for key, value in expected.items():
            self.assertEqual(getattr(invitations[0], key), value)
        self.assertEqual(status, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
