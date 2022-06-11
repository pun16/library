from CommonUtil.LibraryUtil.BookUtil import borrowBook,returnBook,findBook,showBook,booksAvailable
from CommonUtil.LibraryUtil.UserUtil import findUser,showUser,isUsernameValid
from CommonUtil.LibraryUtil.CommonFunc import isLibraryOutOfBooks,isLibraryFull,returnInTime,calculateMoney,printData
from CommonUtil.IOUtil.BookIOUtil import readBooksFromFile,writeBooksToFile,selectBookFromFile,insertBooksToFile
from CommonUtil.IOUtil.UserIOUtil import readUsersFromFile,writeUsersToFile,selectUserFromFile,insertUsersToFile
from CommonUtil.JsonUtil.BookJsonUtil import booksToJson
from CommonUtil.JsonUtil.UserJsonUtil import usersToJson
from Model.User import User
from Model.Book import Book
from flask import Flask, render_template, request, jsonify
import json

import sqlite3

con = sqlite3.connect('mydatabase.db')
cursorObj = con.cursor()
#data=cursorObj.execute('''SELECT * FROM Book''')
#for row in data: print(row)
#cursorObj.execute("CREATE TABLE Book(name text, isinlib text, borrowdate text, user text)")
#cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
#cursorObj.execute('''INSERT INTO Book VALUES ('Turtle', 'True', 'unknown','unknown')''')
#cursorObj.execute('''INSERT INTO User VALUES ('Pun', '2', '')''')
#cursorObj.execute('''UPDATE Book SET borrowdate = 'a' WHERE name='book';''')
#cursorObj.execute("DELETE FROM Book WHERE name = 'rock'")
#cursorObj.execute("DROP TABLE Book")
#cursorObj.execute('DELETE FROM book;',);
#book = Book("book","testa","testb","testc")
#cursorObj.execute("""UPDATE Book SET isinlib = :isinlib,borrowdate = :date,user = :user WHERE name = :name""",{'name':book.name,'isinlib':str(book.isInLibrary),'date':book.dateBorrowed,'user':book.user})
#data=cursorObj.execute('''SELECT * FROM Book''')
#for row in data: print(row)
#data=cursorObj.execute('''SELECT * FROM User''')
#for row in data: print(row)
#con.commit()
con.close()

#newbrunsh

web_site = Flask(__name__)

@web_site.route("/test")#good
def test():
  return "<p>test have run</p>"

@web_site.route('/allBooks')#good
def allBooks():
  booksData = readBooksFromFile()
  jsonString = booksToJson(booksData)
  return jsonString

@web_site.route('/allUsers')#good
def allUsers():
  usersData = readUsersFromFile()
  jsonString = usersToJson(usersData)
  return jsonString

@web_site.route('/availableBooks')#good
def availableBooks():
  booksData = readBooksFromFile()
  jsonString = booksToJson(booksAvailable(booksData))
  return jsonString

@web_site.route('/myBorrowedBooks/<name>')#good
def myBorrowedBooks(name):
  try:
    user = selectUserFromFile(name)
    borrowedBooks = []
    for book in user.booksBorrowed:
      borrowedBooks.append(selectBookFromFile(book))
    jsonString = booksToJson(borrowedBooks) 
    return jsonString
  except Exception as e:
    return '{"error":"%s"}'%(str(e))

@web_site.route('/addBook', methods = ['POST'])#good
def addBook():
  data = request.json
  name = data["BookName"]
  try:
    selectBookFromFile(name)
    return """{"response": "duplicate book name"}"""
  except:
    book = [Book(name)]
    insertBooksToFile(book)
    return """{"response": "your book have been added"}"""

@web_site.route('/addUser', methods = ['POST'])#good
def addUser():
  data = request.json
  name = data["UserName"]
  try:
    selectUserFromFile(name)
    return """{"response": "duplicate user name"}"""
  except:
    if isUsernameValid(name):
      user = [User(name)]
      insertUsersToFile(user)
      return """{"response": "your user have been added"}"""
    else:
      return """{"response": "your user name is invalid"}"""

@web_site.route('/borrow', methods = ['POST'])#good
def borrow():
  data = request.json
  userName = data["UserName"]
  bookName = data["BookName"]
  try:
    borrowBook(selectBookFromFile(bookName),selectUserFromFile(userName))#good
    return """{"response": "you have borrow that book"}"""
  except Exception as e:
    return '{"error":"%s"}'%(str(e))

@web_site.route('/returnToLib', methods = ['POST'])#tested
def returnToLib():
  data = request.json
  userName = data["UserName"]
  bookName = data["BookName"]
  try:
    book = selectBookFromFile(bookName)
    amountOfMoneyOwned = calculateMoney(returnInTime(book.dateBorrowed))
    returnBook(book,selectUserFromFile(userName))
    return """{"response": "you have return that book","amountOfMoneyOwned":"%s"}"""%str(amountOfMoneyOwned)
  except Exception as e:
    return '{"error":"%s"}'%(str(e))

@web_site.route('/removeUser/<name>')#good
def removeUser(name):
  usersData = readUsersFromFile()
  try:
    user = findUser(name, usersData)
    if user.booksBorrowed == []:
      usersData.remove(user)
      writeUsersToFile(usersData)
      return """{"response": "user has been removed"}"""
    else:
      return """{"response": "user still own some books"}"""
  except Exception as e:
    return '{"error":"%s"}'%(str(e))
  
# @web_site.route('/removeBook/<name>')#tested
# def removeBook(name):
#   booksData = readBooksFromFile()
#   try:
#     book = findBook(name, booksData)
#     if book.isInLibrary == True:
#       booksData.remove(book)
#       writeBooksToFile(booksData)
#       return """{"response": "book has been removed"}"""
#     else:
#       return """{"response": "book still is not in lib"}"""
#   except Exception as e:
#     return '{"error":"%s"}'%(str(e))

    
web_site.run(host='0.0.0.0', port=8080)




# booksData = readBooksFromFile()
# usersData = readUsersFromFile()

# whatToDo = str(input("what do you want to do borrow/return/listbook ? ")).lower()
# if whatToDo == "listbook":
#   showBook(booksData)
# else:
#   print("Here are the available users")
#   showUser(usersData)
#   username = input("What is your username ? ")
#   if whatToDo == "borrow":
#     if isLibraryOutOfBooks(booksData):
#       print("we are out of books")
#       exit()
#     print("Here are the available books")
#     showBook(booksData)
#     bookName = input("what book do you want to borrow? ")
#     newBooks,newUsers = borrowBook(bookName,booksData,username,usersData)
#     writeBooksToFile(newBooks)
#     writeUsersToFile(newUsers)
#   elif whatToDo == "return":
#     if isLibraryFull(booksData):
#       print("we are full of books")
#       exit()
#     printData(findUser(username, usersData).booksBorrowed)
#     bookName = input("what book do you want to return? ")
#     amountOfMoneyOwned = calculateMoney(returnInTime(findBook(bookName,booksData).dateBorrowed))
#     print(f'You need to pay ${amountOfMoneyOwned}')
#     newBooks,newUsers = returnBook(bookName, booksData, username, usersData)
#     writeBooksToFile(newBooks)
#     writeUsersToFile(newUsers)
    
    
    
    




