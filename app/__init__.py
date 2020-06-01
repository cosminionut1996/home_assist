from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.group_controller import api as group_ns
from .main.controller.invitation_controller import api as invitation_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus web service',
    authorizations={
        'jwt': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'authorization'
        }
    },
    validate=True
)

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(group_ns, path='/groups')
api.add_namespace(invitation_ns, path='/invitations')
