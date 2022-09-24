import unittest

import datetime

from app.main import db
from app.main.model.blacklist import BlacklistToken
from app.test.base import BaseTestCase

class TestBlacklistModel(BaseTestCase):

    def test_check_blacklist_true(self):
        token = "abcdefg"
        auth_token = BlacklistToken(token)
        db.session.add(auth_token)
        db.session.commit()
        self.assertTrue(BlacklistToken.check_blacklist(token))

    def test_check_blacklist_false(self):
        token = "abcdefg"
        self.assertFalse(BlacklistToken.check_blacklist(token))