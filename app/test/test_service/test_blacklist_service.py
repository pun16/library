import unittest

import datetime

from app.main import db
from app.main.model.blacklist import BlacklistToken
from app.main.service.blacklist_service import save_token
from app.test.base import BaseTestCase

class TestBlacklistService(BaseTestCase):

    def test_save_token_true(self):
        token = "abcdefg"
        data,status = save_token(token)
        self.assertTrue(status == 200)