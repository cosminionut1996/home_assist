import unittest

from app.main import db
from app.main.model.blacklist import BlacklistToken
import json
from app.test.base import BaseTestCase
from http import HTTPStatus
from app.main.controller.group_controller import create_group


def register_user(self):
    return self.client.post(
        '/users/',
        data=json.dumps(dict(
            email='joe@gmail.com',
            username='username',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


class TestInvitationController(BaseTestCase):

    def setUp(self):
        super().setUp()
        # user registration
        resp_register = register_user(self)
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['data']['Authorization'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, HTTPStatus.CREATED)
        # user login
        resp_login = login_user(self)
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['data']['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, HTTPStatus.OK)

        self.resp_login = resp_login
        self.auth = json.loads(resp_login.data.decode())['data']['Authorization']

    def tearDown(self):
        # log out
        response = self.client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    self.resp_login.data.decode()
                )['data']['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, HTTPStatus.OK)

        super().tearDown()

    def test_create_delete_group(self):
        """ Test for group creation and deletion """
        with self.client:
            # group creation
            response = self.client.post(
                '/groups/',
                data=json.dumps(dict(
                    name='Apartment'
                )),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            self.assertEqual(data['group']['name'], 'Apartment')
            group_id = data['group']['_uuid']

            # query the group to make sure it is created
            response = self.client.get(
                '/groups/%s' % group_id,
                headers=dict(
                    Authorization=self.auth
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(data['group']['name'], 'Apartment')

            # group deletion
            response = self.client.delete(
                '/groups/%s' % group_id,
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
            self.assertEqual(response.data.decode(), '')

            # query the group to make sure it is deleted
            response = self.client.get(
                '/groups/%s' % group_id,
                headers=dict(
                    Authorization=self.auth
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            self.assertEqual(data['error'], 'Group not found')

    def test_create_modify_delete_group(self):
        """ Test for group update """
        with self.client:
            # group creation
            response = self.client.post(
                '/groups/',
                data=json.dumps(dict(
                    name='Apartment'
                )),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            self.assertEqual(data['group']['name'], 'Apartment')
            group_id = data['group']['_uuid']

            # group update
            response = self.client.patch(
                '/groups/{}'.format(group_id),
                data=json.dumps(dict(
                    name='MyApartment',
                )),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(data['group']['name'], 'MyApartment')

            # group deletion
            response = self.client.delete(
                '/groups/%s' % data['group']['_uuid'],
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
            self.assertEqual(response.data.decode(), '')

    def test_create_badmodify_delete_group(self):
        """ Test for erroneous group update """
        with self.client:
            # group creation
            response = self.client.post(
                '/groups/',
                data=json.dumps(dict(
                    name='Apartment'
                )),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            self.assertEqual(data['group']['name'], 'Apartment')
            group_uuid = data['group']['_uuid']

            # group update with bad data
            response = self.client.patch(
                '/groups/{}'.format(group_uuid),
                data=json.dumps(dict(
                    name='MyApartment',
                    id=123
                )),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(data['error'], 'Unknown arguments')

            # group update with no data
            response = self.client.patch(
                '/groups/{}'.format(group_uuid),
                data=json.dumps(dict()),
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(data['error'], 'Empty body')

            # group deletion
            response = self.client.delete(
                '/groups/%s' % group_uuid,
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
            self.assertEqual(response.data.decode(), '')

if __name__ == '__main__':
    unittest.main()