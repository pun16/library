from flask_restx import Api
from flask import Blueprint

import typing

#from .main.controller.user_controller import api as user_ns
#from .main.controller.auth_controller import api as auth_ns

blueprint: Blueprint = Blueprint('api', __name__)
authorizations: typing.Dict[str, typing.Dict[str, str]] = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api: Api = Api(
    blueprint,
    title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey'
)

#api.add_namespace(user_ns, path='/banana')
#api.add_namespace(auth_ns)
