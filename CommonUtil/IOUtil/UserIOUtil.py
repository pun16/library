from Model.User import User
from typing import List

import sqlite3

def readUsersFromFile(fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> List[User]:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  data=cursorObj.execute('''SELECT * FROM User''')
  users = []
  for newLine in data:
    booklist = list(filter(lambda x: x != "", newLine[2].split("#")))
    user = User(newLine[0],int(newLine[1]),booklist)
    users.append(user)
  con.close()
  return users

def selectUserFromFile(userName:str, fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> User:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  data=cursorObj.execute("SELECT * FROM User WHERE name=?", (userName,)).fetchall()
  if len(data)==0:
    raise Exception('There is no user named %s'%userName)
  for newLine in data:
    booklist = list(filter(lambda x: x != "", newLine[2].split("#")))
    user = User(newLine[0],int(newLine[1]),booklist)
  return user

def writeUsersToFile(users:List[User],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  cursorObj.execute('DELETE FROM User;',)
  for user in users:
    booksBorrowed = "#".join(user.booksBorrowed)
    cursorObj.execute('''INSERT INTO User VALUES (:name, :limits, :booksBorrowed)''',{'name':user.name,'limits':str(user.limit),'booksBorrowed':booksBorrowed})
  con.commit()
  con.close()

def updateUsersToFile(users:List[User],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for user in users:
    booksBorrowed = "#".join(user.booksBorrowed)
    cursorObj.execute("""UPDATE User SET limits = :limits,booksBorrowed = :booksBorrowed WHERE name = :name""",{'name':user.name,'limits':str(user.limit),'booksBorrowed':booksBorrowed})
  con.commit()
  con.close()

def insertUsersToFile(users:List[User],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for user in users:
    booksBorrowed = "#".join(user.booksBorrowed)
    cursorObj.execute("""INSERT INTO User VALUES (:name, :limits, :booksBorrowed)""",{'name':user.name,'limits':str(user.limit),'booksBorrowed':booksBorrowed})
  con.commit()
  con.close()

def deleteUsersFromFile(users:List[User],fileName:str = "/mnt/d/data/coding_learning/library/mydatabase.db") -> None:
  con = sqlite3.connect(fileName)
  cursorObj = con.cursor()
  for user in users:
    cursorObj.execute("""DELETE FROM User WHERE name = :name""",{'name':user.name})
  con.commit()
  con.close()