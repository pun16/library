import unittest
from datetime import datetime
from urllib import response
from app.main import db
from app.main.service.book_service import *
from app.main.service.user_service import *
from app.main.service.library_service import *
from app.test.base import BaseTestCase
from unittest.mock import Mock

class TestLibraryService(BaseTestCase):

    def test_borrowBook_success(self):
        dataBook = {
            "bookname":"booktest"
        }
        response,status_new_book = save_new_book(dataBook)
        dataUser = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        response,status_new_user = save_new_user(dataUser)
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        time = datetime.now()
        response,status_borrow_book = borrowBook(dataBorrowBook, time)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_new_book == 201 and status_new_user == 201)
        self.assertTrue(status_borrow_book == 200 and book.is_in_lib == False and book.date_borrowed == time and user.limits == 1 and user.books[0].bookname == book.bookname)

    def test_borrowBook_book_not_in_lib_fail(self):
        dataB = Book(
            bookname="booktest",
            is_in_lib=False,
            registered_on=datetime.now()
        )
        db.session.add(dataB)
        db.session.commit()
        dataUser = {
            "email":"email.test",
            "username":"usertesta",
            "password":"password"
        }
        response,status_new_user = save_new_user(dataUser)
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        response,status_borrow_book = borrowBook(dataBorrowBook)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_borrow_book == 409 and response['message'] == 'Sorry that book is not in the library.' and book.is_in_lib == False and user.limits == 2)

    def test_borrowBook_user_limit_fail(self):
        dataBook = {
            "bookname":"booktest"
        }
        response,status_new_book = save_new_book(dataBook)
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=0,
            registered_on=datetime.now()
        )
        db.session.add(dataU)
        db.session.commit()
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        response,status_borrow_book = borrowBook(dataBorrowBook)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_borrow_book == 409 and response['message'] == 'Sorry you own too many book.' and book.is_in_lib == True and user.limits == 0)
    
    def test_returnInTime_success_intime(self):
        timeoftest = datetime.now()
        daydifferent = returnInTime(timeoftest+timedelta(days = -2),timeoftest)
        self.assertTrue(daydifferent == 0)

    def test_returnInTime_success_not_intime(self):
        timeoftest = datetime.now()
        daydifferent = returnInTime(timeoftest+timedelta(days = -9),timeoftest)
        self.assertTrue(daydifferent == 2)

    def test_returnBook_book_in_lib_fail(self):
        dataBook = {
            "bookname":"booktest"
        }
        response,status_new_book = save_new_book(dataBook)
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=0,
            registered_on=datetime.now()
        )
        db.session.add(dataU)
        db.session.commit()
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        response,status_return_book = returnBook(dataBorrowBook)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 409 and response['message'] == 'sorry that book is in the library.' and book.is_in_lib == True and user.limits == 0)

    def test_returnBook_user_didnt_borrow_fail(self):
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=2,
            registered_on=datetime.now()
        )
        dataB = Book(
            is_in_lib=False,
            registered_on=datetime.now(),
            date_borrowed=datetime.now(),
            bookname="booktest"
        )
        db.session.add(dataB)
        db.session.add(dataU)
        db.session.commit()
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        response,status_return_book = returnBook(dataBorrowBook)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 409 and response['message'] == "sorry you don't own any book." and book.is_in_lib == False and user.limits == 2)

    def test_returnBook_user_didnt_borrow_that_book_fail(self):
        dataU = User(
            email="email.test",
            username="usertest",
            password="password",
            limits=0,
            registered_on=datetime.now()
        )
        dataB = Book(
            is_in_lib=False,
            registered_on=datetime.now(),
            date_borrowed=datetime.now(),
            bookname="booktest"
        )
        db.session.add(dataB)
        db.session.add(dataU)
        db.session.commit()
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        response,status_return_book = returnBook(dataBorrowBook)
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 409 and response['message'] == "you did not borrow that book." and book.is_in_lib == False and user.limits == 0)
    
    def test_returnBook_success_intime(self):
        dataBook = {
            "bookname":"booktest"
        }
        save_new_book(dataBook)
        dataUser = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        save_new_user(dataUser)
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        time = datetime.now()
        borrowBook(dataBorrowBook, time)
        response_return,status_return_book = returnBook(dataBorrowBook, time+timedelta(days = 3))
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 200 and response_return['message'] == "Successfully returned." and response_return['moneyown'] == "0 baht" and book.is_in_lib == True and user.limits == 2)
        
    def test_returnBook_success_not_in_time_one_day(self):
        dataBook = {
            "bookname":"booktest"
        }
        save_new_book(dataBook)
        dataUser = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        save_new_user(dataUser)
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        time = datetime.now()
        borrowBook(dataBorrowBook, time)
        response_return,status_return_book = returnBook(dataBorrowBook, time+timedelta(days = 8))
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 200 and response_return['message'] == "Successfully returned." and response_return['moneyown'] == "3 baht" and book.is_in_lib == True and user.limits == 2)
        
    def test_returnBook_success_not_in_time_three_day(self):
        dataBook = {
            "bookname":"booktest"
        }
        save_new_book(dataBook)
        dataUser = {
            "email":"email.test",
            "username":"usertest",
            "password":"password"
        }
        save_new_user(dataUser)
        dataBorrowBook = {
            "bookname":"booktest",
            "email":"email.test"
        }
        time = datetime.now()
        borrowBook(dataBorrowBook, time)
        response_return,status_return_book = returnBook(dataBorrowBook, time+timedelta(days = 10))
        book = get_a_book("booktest")
        user = get_a_user("email.test")
        self.assertTrue(status_return_book == 200 and response_return['message'] == "Successfully returned." and response_return['moneyown'] == "9 baht" and book.is_in_lib == True and user.limits == 2)
        