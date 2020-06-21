import unittest

from app.main.model.blacklist import BlacklistToken
import json

from http import HTTPStatus
from app.main.controller.group_controller import create_group
from .base_user_authenticated import BaseUserAuthenticated


class TestGroupController(BaseUserAuthenticated):

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
            uuid_group = data['group']['_uuid']

            # query the group to make sure it is created
            response = self.client.get(
                '/groups/%s' % uuid_group,
                headers=dict(
                    Authorization=self.auth
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(data['group']['name'], 'Apartment')

            # group deletion
            response = self.client.delete(
                '/groups/%s' % uuid_group,
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
            self.assertEqual(response.data.decode(), '')

            # query the group to make sure it is deleted
            response = self.client.get(
                '/groups/%s' % uuid_group,
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
            group_id = data['group']['_uuid']

            # group update with bad data
            response = self.client.patch(
                '/groups/{}'.format(group_id),
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
                '/groups/{}'.format(group_id),
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
                '/groups/%s' % group_id,
                headers=dict(
                    Authorization=self.auth
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
            self.assertEqual(response.data.decode(), '')

if __name__ == '__main__':
    unittest.main()
