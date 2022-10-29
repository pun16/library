import unittest

import datetime

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_check_password(self):
        user = User(
            email='test@test.com',
            password='test',
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        self.assertTrue(user.check_password("test"))

    def test_check_password_fail(self):
        user = User(
            email='test@test.com',
            password='test',
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        self.assertFalse(user.check_password("thiswillfail"))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            limits=2,
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8") ) == 1)

    def test_decode_auth_token_invalid(self):
        self.assertTrue(User.decode_auth_token("ajdisj") == 'Invalid token. Please log in again.')

    def test_decode_auth_token_expired(self):
        user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        auth_token = User.encode_auth_token(user.id, -1)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8") ) == 'Signature expired. Please log in again.')

if __name__ == '__main__':
    unittest.main()

