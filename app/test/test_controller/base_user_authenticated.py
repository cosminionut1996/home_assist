import json
from app.test.base import BaseTestCase
from http import HTTPStatus



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


class BaseUserAuthenticated(BaseTestCase):

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
