from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    showUser = api.model('showuser', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'limits': fields.String(required=True, description='user limits')
    })
    createUser = api.model('createuser', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
