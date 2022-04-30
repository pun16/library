from CommonUtil.LibraryUtil.BookUtil import findBook,borrowBook,returnBook,booksAvailable
import pytest
from Model.Book import Book
from Model.User import User
from datetime import date
import sqlite3
import os

def test_find_book_success():
  books = [Book("test")]
  bookName = "test"
  book = findBook(bookName,books)
  assert book.name == "test"

def test_find_book_failed():
  books = [Book("tes")]
  bookName = "test"
  with pytest.raises(Exception, match=r"can not find book"):
    findBook(bookName,books)

def test_borrowBook_success():
  books = Book("book_1")
  users = User("user_1")
  conA = sqlite3.connect("mydatabase_testi.db")
  cursorObj = conA.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('book_1', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_2', 'True', 'unknown','unknown')''')
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('user_1', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('user_2', '2', '')''')
  conA.commit()
  conA.close()
  borrowBook(books,users,'mydatabase_testi.db')
  time = date.today()
  conB = sqlite3.connect("mydatabase_testi.db")
  cursorObjb = conB.cursor()
  dataBook=cursorObjb.execute('''SELECT * FROM Book''')
  stringBook = ''
  for newLine in dataBook:
    stringBook = stringBook + str(newLine)
  dataUser=cursorObjb.execute('''SELECT * FROM User''')
  stringUser = ''
  for newLine in dataUser:
    stringUser = stringUser + str(newLine)
  conB.commit()
  conB.close()
  os.remove('mydatabase_testi.db')
  assert stringBook == '''('book_1', 'False', '%s', 'user_1')('book_2', 'True', 'unknown', 'unknown')''' % (time) and stringUser == '''('user_1', '1', 'book_1')('user_2', '2', '')'''

def test_borrowBook_max_borrow_fail():
  books = Book("book_test")
  users = User("user_test",0)
  with pytest.raises(Exception, match=r"sorry you own too many book"):
    borrowBook(books,users,'a')

def test_borrowBook_not_in_lib_fail():
  books = Book("book_test",False)
  users = User("user_test")
  with pytest.raises(Exception, match=r"sorry that book is not in the library"):
    borrowBook(books,users,'b')

def test_returnBook_success():
  book = Book("book_1",False,"2021-09-10","user_1")
  user = User("user_1",1,['book_1'])
  conC = sqlite3.connect("mydatabase_testh.db")
  cursorObjc = conC.cursor()
  cursorObjc.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObjc.execute('''INSERT INTO Book VALUES ('book_1', 'False', '2021-09-10','user_1')''')
  cursorObjc.execute('''INSERT INTO Book VALUES ('book_2', 'True', 'unknown','unknown')''')
  cursorObjc.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObjc.execute('''INSERT INTO User VALUES ('user_1', '1', 'book_1')''')
  cursorObjc.execute('''INSERT INTO User VALUES ('user_2', '2', '')''')
  conC.commit()
  conC.close()
  returnBook(book,user,"mydatabase_testh.db")
  conD = sqlite3.connect("mydatabase_testh.db")
  cursorObjd = conD.cursor()
  dataBook=cursorObjd.execute('''SELECT * FROM Book''')
  stringBook = ''
  for newLine in dataBook:
    stringBook = stringBook + str(newLine)
  dataUser=cursorObjd.execute('''SELECT * FROM User''')
  stringUser = ''
  for newLine in dataUser:
    stringUser = stringUser + str(newLine)
  conD.commit()
  conD.close()
  os.remove('mydatabase_testh.db')
  assert stringBook == '''('book_1', 'True', 'unknown', 'unknown')('book_2', 'True', 'unknown', 'unknown')'''  and stringUser == '''('user_1', '2', '')('user_2', '2', '')'''

def test_returnBook_no_borrow_fail():
  book = Book("book_test",False,"2021-09-10","user_test2")
  user = User("user_test",1,["book_test2"])
  with pytest.raises(Exception, match=r"you did not borrow that book"):
    returnBook(book,user,'c')

def test_returnBook_in_lib_fail():
  book = Book("book_test")
  user = User("user_test",1,["book_test"])
  with pytest.raises(Exception, match=r"sorry that book is in the library"):
    returnBook(book,user,'d')

def test_returnBook_no_book_own_fail():
  book = Book("book_test",False,"2021-09-10","user_test2")
  user = User("user_test")
  with pytest.raises(Exception, match=r"sorry you don't own any book"):
    returnBook(book,user,'e')
