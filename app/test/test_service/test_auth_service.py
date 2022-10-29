import datetime
from app.main import db
from app.main.model.user import User
from app.main.service.auth_service import Auth
from app.test.base import BaseTestCase
from unittest.mock import Mock
from app.main.model.blacklist import BlacklistToken
from flask import request


class TestAuthService(BaseTestCase):

    def test_login_user_succes(self):
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        dataD = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        db.session.add(dataU)
        db.session.commit()
        response,status = Auth.login_user(dataD)
        responseStatus = response["status"]
        self.assertTrue(status == 200 and responseStatus == "success" )

    def test_login_user_wrong_password(self):
        dataD = {
            "email":"email.test",
            "username":"userte",
            "password":"password"
        }
        response,status = Auth.login_user(dataD)
        responseStatus = response["status"]
        self.assertTrue(status == 401 and responseStatus == "fail" )

    def test_logout_user_succes(self):
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(dataU)
        db.session.commit()
        token = User.encode_auth_token(1, 1)
        response,status = Auth.logout_user(token)
        responseStatus = response["status"]
        self.assertTrue(status == 200 and responseStatus == "success" and BlacklistToken.query.with_entities(BlacklistToken.token).first()[0] == token)

    def test_logout_user_invalid_token(self):
        response,status = Auth.logout_user("token")
        responseStatus = response["status"]
        self.assertTrue(status == 401 and responseStatus == "fail")
    
    def test_logout_user_invalid_token(self):
        response,status = Auth.logout_user(None)
        responseStatus = response["status"]
        self.assertTrue(status == 403 and responseStatus == "fail")

""" mabe later
    def test_get_logged_in_user_succes(self):
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            registered_on=datetime.datetime.utcnow()
        )
        dataD = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        db.session.add(dataU)
        db.session.commit()
        token = User.encode_auth_token(1, 1)
        responselogin,statuslogin = Auth.login_user(dataD)
        response,status = Auth.get_logged_in_user(request)
        responseStatus = response["status"]
        responseStatuslogin = responselogin["status"]
        print(status, responseStatus, statuslogin,responseStatuslogin)
        self.assertTrue(status == 200 and responseStatus == "success" and statuslogin == 200 and responseStatuslogin == "success" and BlacklistToken.query.with_entities(BlacklistToken.token).first()[0] == token)
"""