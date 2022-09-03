import unittest
import datetime
from urllib import response
from app.main import db
from app.main.service.book_service import *
from app.test.base import BaseTestCase
from unittest.mock import Mock


class TestBookService(BaseTestCase):

    def test_save_new_book_succes(self):
        data = {
            "bookname":"booktest"
        }
        response,status = save_new_book(data)
        book = get_a_book("booktest")
        self.assertTrue(status == 201 and book.bookname == "booktest" and book.is_in_lib and book.user_id == None)

    def test_save_new_book_fail(self):
        data = {
            "bookname":"bookname"
        }
        responseA,statusA = save_new_book(data)
        responseB,statusB = save_new_book(data)
        self.assertTrue(statusA == 201 and statusB == 409)

        