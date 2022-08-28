import unittest
import datetime
from urllib import response
from app.main import db
from app.main.service.user_service import *
from app.test.base import BaseTestCase
from unittest.mock import Mock


class TestUserService(BaseTestCase):

    def test_save_new_user_succes(self):
        data = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        response,status = save_new_user(data)
        self.assertTrue(status == 201)
    
    def test_save_new_user_fail(self):
        data = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        responseA,statusA = save_new_user(data)
        responseB,statusB = save_new_user(data)
        self.assertTrue(statusA == 201 and statusB == 409)

    def test_generate_token_fail(self):
        new_user = User(
            email='email',
            username='username',
            password='password',
            registered_on=datetime.datetime.utcnow()
        )
        userStatic = Mock()
        userStatic.encode_auth_token.side_effect=KeyError('foo')
        respondA,statusA = generate_token(new_user, userStatic)
        self.assertTrue(statusA == 401)