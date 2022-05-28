from CommonUtil.IOUtil.BookIOUtil import readBooksFromFile,selectBookFromFile, writeBooksToFile, updateBooksToFile,insertBooksToFile,deleteBooksFromFile
from Model.Book import Book
import os
import pytest
import sqlite3

def test_read_books_from_file_success():
  con = sqlite3.connect('mydatabase_testa.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('rabbit', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('turtle', 'False', '2021-09-10','user_test')''')
  con.commit()
  con.close()
  books = readBooksFromFile("mydatabase_testa.db")
  os.remove('mydatabase_testa.db')
  assert books[0].name == "rabbit" and books[0].isInLibrary == True and books[0].user == "unknown" and books[0].dateBorrowed == "unknown" and books[1].name == "turtle" and books[1].isInLibrary == False and books[1].user == "user_test" and books[1].dateBorrowed == "2021-09-10"

def test_select_book_from_file_success():
  con = sqlite3.connect('mydatabase_testc.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('rabbit', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('turtle', 'False', '2021-09-10','user_test')''')
  con.commit()
  con.close()
  book = selectBookFromFile("rabbit","mydatabase_testc.db")
  os.remove('mydatabase_testc.db')
  assert book.name == "rabbit" and book.isInLibrary == True and book.user == "unknown" and book.dateBorrowed == "unknown"

def test_select_book_from_file_fail():
  con = sqlite3.connect('mydatabase_testd.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('rabbit', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('turtle', 'False', '2021-09-10','user_test')''')
  con.commit()
  con.close()
  with pytest.raises(Exception, match=r"There is no book named rabbits"):
    selectBookFromFile("rabbits","mydatabase_testd.db")
  os.remove('mydatabase_testd.db')
    
def test_writeBooksToFile_success():
  book = [Book('book_1',True,'unknown','unknown'),Book('book_2',False,'29-01-2022','user')]
  con = sqlite3.connect("mydatabase_testb.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  writeBooksToFile(book ,"mydatabase_testb.db")
  data=cursorObj.execute('''SELECT * FROM Book''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  con.commit()
  con.close()
  os.remove('mydatabase_testb.db')
  assert string == '''('book_1', 'True', 'unknown', 'unknown')('book_2', 'False', '29-01-2022', 'user')'''

def test_updateBooksToFile_success():
  book = [Book('book_1',True,'unknown','unknown'),Book('book_2',False,'29-01-2022','user')]
  con = sqlite3.connect("mydatabase_teste.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('book_1', 'False', '2021-09-10','user_test')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_2', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_3', 'True', 'unknown','unknown')''')
  con.commit()
  con.close()
  updateBooksToFile(book ,"mydatabase_teste.db")
  conn = sqlite3.connect("mydatabase_teste.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM Book''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_teste.db')
  assert string == '''('book_1', 'True', 'unknown', 'unknown')('book_2', 'False', '29-01-2022', 'user')('book_3', 'True', 'unknown', 'unknown')'''

def test_updateBooksToFile_no_name_success():
  book = [Book('book',True,'unknown','unknown')]
  con = sqlite3.connect("mydatabase_testf.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('book_1', 'False', '29-01-2022','user')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_2', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_3', 'True', 'unknown','unknown')''')
  con.commit()
  con.close()
  updateBooksToFile(book ,"mydatabase_testf.db")
  conn = sqlite3.connect("mydatabase_testf.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM Book''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testf.db')
  assert string == '''('book_1', 'False', '29-01-2022', 'user')('book_2', 'True', 'unknown', 'unknown')('book_3', 'True', 'unknown', 'unknown')'''

def test_insertBooksToFile_success():
  book = [Book('book_2',True,'unknown','unknown')]
  con = sqlite3.connect("mydatabase_testg.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('book_1', 'True', 'unknown','unknown')''')
  con.commit()
  con.close()
  insertBooksToFile(book ,"mydatabase_testg.db")
  conn = sqlite3.connect("mydatabase_testg.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM Book''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testg.db')
  assert string == '''('book_1', 'True', 'unknown', 'unknown')('book_2', 'True', 'unknown', 'unknown')'''

def test_deleteBooksFromFile_success():
  book = [Book('book_2')]
  con = sqlite3.connect("mydatabase_testj.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
  cursorObj.execute('''INSERT INTO Book VALUES ('book_1', 'False', '29-01-2022','user')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_2', 'True', 'unknown','unknown')''')
  cursorObj.execute('''INSERT INTO Book VALUES ('book_3', 'True', 'unknown','unknown')''')
  con.commit()
  con.close()
  deleteBooksFromFile(book ,"mydatabase_testj.db")
  conn = sqlite3.connect("mydatabase_testj.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM Book''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testj.db')
  assert string == '''('book_1', 'False', '29-01-2022', 'user')('book_3', 'True', 'unknown', 'unknown')'''