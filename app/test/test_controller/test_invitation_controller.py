import json
import unittest
from http import HTTPStatus

from .base_user_authenticated import BaseUserAuthenticated
from app.main.model.invitation import InvitationStatus

class TestInvitationController(BaseUserAuthenticated):

    def setUp(self):
        super().setUp()

        # create a group
        self.created_group = self.client.post(
            '/groups',
            data=json.dumps(dict(
                name='my_group'
            )),
            headers=dict(
                Authorization=self.auth
            ),
            content_type='application/json'
        )


    def tearDown(self):

        # delete the previously created groups
        response = self.client.get(
            '/groups?owned=True',
            headers=dict(
                Authorization=self.auth
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(data), 1)
        for group in data:
            if group['name'] == 'my_group':
                response = self.client.delete(
                    '/groups/%s' % group['_uuid'],
                    headers=dict(
                        Authorization=self.auth
                    ),
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
                break

        super().tearDown()

    def test_create_reject_invitation(self):
        """ Test for invitation creation and rejection """
        # Register or login another user in order to send him an invitation
        # (sometimes the database might not get cleaned up properly)
        resp_register = self.client.post(
            '/users/',
            data=json.dumps(dict(
                email='gill@gmail.com',
                username='gibilan',
                password='123456'
            )),
            content_type='application/json'
        )
        if resp_register.status_code == HTTPStatus.CONFLICT:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='gill@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            self.assertEqual(resp_login.status_code, HTTPStatus.OK)
            other_user_token = resp_login.json['data']['Authorization']
        else:
            self.assertTrue(resp_register.status_code, HTTPStatus.CREATED)
            other_user_token = resp_register.json['data']['Authorization']

        # send an invitation to the other user for 'my_group'
        resp_invite = self.client.post(
            '/invitations',
            data=json.dumps(dict(
                username_invitee='gibilan',
                resource_type='group',
                uuid_resource=self.created_group.json['group']['_uuid']
            )),
            headers=dict(
                Authorization=self.auth
            ),
            content_type='application/json'
        )
        common_fields = ['_uuid', 'uuid_sender', 'uuid_invitee', 'uuid_resource', 'resource_type', 'token']

        for field in common_fields:
            self.assertTrue(resp_invite.json[field])
        self.assertEqual(
            resp_invite.json.get('status'),
            InvitationStatus.PENDING
        )

        # reject invitation
        resp_reject = self.client.post(
            '/invitations/{}/reject'.format(resp_invite.json['_uuid']),
            headers=dict(
                Authorization=other_user_token
            ),
            content_type='application/json'
        )
        self.assertEqual(resp_reject.status_code, HTTPStatus.OK)
        for field in common_fields:
            self.assertEqual(
                resp_invite.json.get(field),
                resp_reject.json.get(field)
            )
        self.assertEqual(
            resp_reject.json.get('status'),
            InvitationStatus.REJECTED
        )

    def test_create_accept_invitation(self):
        """ Test for invitation creation and acceptance """
        # Register or login another user in order to send him an invitation
        # (sometimes the database might not get cleaned up properly)
        resp_register = self.client.post(
            '/users/',
            data=json.dumps(dict(
                email='gill@gmail.com',
                username='gibilan',
                password='123456'
            )),
            content_type='application/json'
        )
        if resp_register.status_code == HTTPStatus.CONFLICT:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='gill@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            self.assertEqual(resp_login.status_code, HTTPStatus.OK)
            other_user_token = resp_login.json['data']['Authorization']
        else:
            self.assertTrue(resp_register.status_code, HTTPStatus.CREATED)
            other_user_token = resp_register.json['data']['Authorization']

        # send an invitation to the other user for 'my_group'
        resp_invite = self.client.post(
            '/invitations',
            data=json.dumps(dict(
                username_invitee='gibilan',
                resource_type='group',
                uuid_resource=self.created_group.json['group']['_uuid']
            )),
            headers=dict(
                Authorization=self.auth
            ),
            content_type='application/json'
        )
        common_fields = ['_uuid', 'uuid_sender', 'uuid_invitee', 'uuid_resource', 'resource_type', 'token']

        for field in common_fields:
            self.assertTrue(resp_invite.json[field])
        self.assertEqual(
            resp_invite.json.get('status'),
            InvitationStatus.PENDING
        )

        # accept invitation
        resp_reject = self.client.post(
            '/invitations/{}/accept'.format(resp_invite.json['_uuid']),
            headers=dict(
                Authorization=other_user_token
            ),
            content_type='application/json'
        )
        self.assertEqual(resp_reject.status_code, HTTPStatus.OK)
        for field in common_fields:
            self.assertEqual(
                resp_invite.json.get(field),
                resp_reject.json.get(field)
            )
        self.assertEqual(
            resp_reject.json.get('status'),
            InvitationStatus.ACCEPTED
        )


if __name__ == '__main__':
    unittest.main()
