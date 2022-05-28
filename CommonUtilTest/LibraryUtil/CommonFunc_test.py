from CommonUtil.LibraryUtil.CommonFunc import isLibraryOutOfBooks,isLibraryFull,returnInTime
from Model.Book import Book
from datetime import timedelta, datetime

def test_isLibraryOutOfBook_true():
  books = [Book("book_test",False,"2021-09-10","user_test"),Book("book_test2",False,"2021-09-10","user_test")]
  assert isLibraryOutOfBooks(books) == True

def test_isLibraryOutOfBook_false():
  books = [Book("book_test",False,"2021-09-10","user_test"),Book("book_test2")]
  assert isLibraryOutOfBooks(books) == False

def test_isLibraryFull_true():
  books = [Book("book_test"),Book("book_test2")]
  assert isLibraryFull(books) == True

def test_isLibraryFull_false():
  books = [Book("book_test"),Book("book_test2",False,"2021-09-10","user_test")]
  assert isLibraryFull(books) == False

def test_returnInTime_success():
  Date = str(datetime.today() - timedelta(days=3))[0:10]
  EndDate = returnInTime(Date)
  assert EndDate == 0

def test_returnInTime_overtime_success():
  Date = str(datetime.today() - timedelta(days=8))[0:10]
  EndDate = returnInTime(Date)
  assert EndDate == 1