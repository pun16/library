import unittest

import datetime

from app.main import db
from app.main.model.book import Book
from app.test.base import BaseTestCase

class TestBookModel(BaseTestCase):

    def test_book_id(self):
        book = Book(
            bookname='rabbit',
            is_in_lib=False,
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(book)
        db.session.commit()
        self.assertTrue(book.id == 1)