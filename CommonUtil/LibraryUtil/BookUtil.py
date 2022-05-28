from Model.Book import Book
from Model.User import User
from typing import List,Tuple
from .UserUtil import findUser
from datetime import date
from CommonUtil.IOUtil.UserIOUtil import updateUsersToFile
from CommonUtil.IOUtil.BookIOUtil import updateBooksToFile

def showBook(books:List[Book]) -> None:
  for book in books:
    if book.isInLibrary == True:
      print(book.name)

def findBook(bookName:str,books:List[Book]) -> Book:
  for book in books:
    if book.name == bookName:
      return book
  raise Exception ("can not find book")

def borrowBook(book:Book,user:User,fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  if book.isInLibrary == False:
    raise Exception("sorry that book is not in the library")
  if user.limit == 0:
    raise Exception("sorry you own too many book")
  updateBooksToFile([Book(book.name,False,date.today(),user.name)],fileName)
  updateUsersToFile([User(user.name,user.limit-1,user.booksBorrowed + [book.name])],fileName)

def returnBook(book:Book,user:User,fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  if book.isInLibrary == True:
    raise Exception("sorry that book is in the library")
  if user.limit == 2:
    raise Exception("sorry you don't own any book")
  if (book.name not in user.booksBorrowed):
    raise Exception("you did not borrow that book")
  updateBooksToFile([Book(book.name,True,"unknown","unknown")],fileName)
  updateUsersToFile([User(user.name,user.limit+1,[bookName for bookName in user.booksBorrowed if bookName != book.name])],fileName)

def booksAvailable(books:List[Book]) -> List[Book]:
  availablebooks = []
  for book in books:
    if book.isInLibrary == True:
      availablebooks.append(book)
  return availablebooks