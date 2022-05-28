from Model.Book import Book
from typing import List

import sqlite3

def readBooksFromFile(fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> List[Book]:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  data=cursorObj.execute('''SELECT * FROM Book''')
  books = []
  for newLine in data:
    book = Book(newLine[0],bool(newLine[1].replace("False","")),newLine[2],newLine[3])
    books.append(book)
  con.close()
  return books

def selectBookFromFile(bookName:str, fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> Book:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  data=cursorObj.execute("SELECT * FROM Book WHERE name=?", (bookName,)).fetchall()
  if len(data)==0:
    raise Exception('There is no book named %s'%bookName)
  for newLine in data:
    book = Book(newLine[0],bool(newLine[1].replace("False","")),newLine[2],newLine[3])
  return book

def writeBooksToFile(books:List[Book],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  cursorObj.execute('DELETE FROM Book;',)
  for book in books:
    cursorObj.execute('''INSERT INTO Book VALUES (:name, :isinlib, :date, :user)''',{'name':book.name,'isinlib':str(book.isInLibrary),'date':book.dateBorrowed,'user':book.user})
  con.commit()
  con.close()

def updateBooksToFile(books:List[Book],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for book in books:
    cursorObj.execute("""UPDATE Book SET isinlib = :isinlib,borrowdate = :date,user = :user WHERE name = :name""",{'name':book.name,'isinlib':str(book.isInLibrary),'date':book.dateBorrowed,'user':book.user})
  con.commit()
  con.close()

def insertBooksToFile(books:List[Book],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for book in books:
    cursorObj.execute("""INSERT INTO Book VALUES (:name, :isinlib, :date, :user)""",{'name':book.name,'isinlib':str(book.isInLibrary),'date':book.dateBorrowed,'user':book.user})
  con.commit()
  con.close()

def deleteBooksFromFile(books:List[Book],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for book in books:
    cursorObj.execute("""DELETE FROM Book WHERE name = :name""",{'name':book.name})
  con.commit()
  con.close()