from flask import request
from flask_restx import Resource

#from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user
from typing import Dict, Tuple

api = UserDto.api
_showuser = UserDto.showUser
_createuser = UserDto.createUser

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    #@admin_token_required
    @api.marshal_list_with(_showuser, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_createuser, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


