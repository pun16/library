from CommonUtil.IOUtil.UserIOUtil import readUsersFromFile,writeUsersToFile,updateUsersToFile,selectUserFromFile,insertUsersToFile,deleteUsersFromFile
from Model.User import User
import os
import pytest

import sqlite3

def test_read_User_from_file():
  con = sqlite3.connect('mydatabase_testa.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  cursorObj.execute('''INSERT INTO User VALUES ('pun', '0', 'turtle#fox')''')
  con.commit()
  con.close()
  users = readUsersFromFile('mydatabase_testa.db')
  os.remove('mydatabase_testa.db')
  assert users[0].name == "Jump" and users[0].limit == 2 and users[0].booksBorrowed == [] and users[1].name == "Jess" and users[1].limit == 1 and users[1].booksBorrowed == ["rabbit"] and users[2].name == "pun" and users[2].limit == 0 and users[2].booksBorrowed == ["turtle","fox"]

def test_writeUsersToFile_success():
  users = [User("User_test",1,["book"]),User("User_test2"),User("User_test3",0,["book","banana"])]
  con = sqlite3.connect("mydatabase_testb.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  writeUsersToFile(users,'mydatabase_testb.db')
  data=cursorObj.execute('''SELECT * FROM User''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  con.commit()
  con.close()
  os.remove('mydatabase_testb.db')
  assert string == '''('User_test', '1', 'book')('User_test2', '2', '')('User_test3', '0', 'book#banana')'''

def test_select_user_from_file_success():
  con = sqlite3.connect('mydatabase_testc.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  cursorObj.execute('''INSERT INTO User VALUES ('pun', '2', '')''')
  con.commit()
  con.close()
  user = selectUserFromFile("Jess","mydatabase_testc.db")
  os.remove('mydatabase_testc.db')
  assert user.name == "Jess" and user.limit == 1 and user.booksBorrowed == ["rabbit"]

def test_select_user_from_file_fail():
  con = sqlite3.connect('mydatabase_testm.db')
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  con.commit()
  con.close()
  with pytest.raises(Exception, match=r"There is no user named rabbits"):
    selectUserFromFile("rabbits","mydatabase_testm.db")
  os.remove('mydatabase_testm.db')

def test_updateBookToFile_success():
  users = [User("Jess",1,["fox"]),User("Jump",0,["book","banana"])]
  con = sqlite3.connect("mydatabase_teste.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  cursorObj.execute('''INSERT INTO User VALUES ('pun', '2', '')''')
  con.commit()
  con.close()
  updateUsersToFile(users ,"mydatabase_teste.db")
  conn = sqlite3.connect("mydatabase_teste.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM User''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_teste.db')
  assert string == '''('Jump', '0', 'book#banana')('Jess', '1', 'fox')('pun', '2', '')'''

def test_updateUserToFile_no_name_success():
  users = [User("user",1,["fox"])]
  con = sqlite3.connect("mydatabase_testf.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  cursorObj.execute('''INSERT INTO User VALUES ('pun', '2', '')''')
  con.commit()
  con.close()
  updateUsersToFile(users ,"mydatabase_testf.db")
  conn = sqlite3.connect("mydatabase_testf.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM User''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testf.db')
  assert string == '''('Jump', '2', '')('Jess', '1', 'rabbit')('pun', '2', '')'''

def test_insertUserToFile_success():
  users = [User("user")]
  con = sqlite3.connect("mydatabase_testh.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  con.commit()
  con.close()
  insertUsersToFile(users ,"mydatabase_testh.db")
  conn = sqlite3.connect("mydatabase_testh.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM User''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testh.db')
  assert string == '''('Jump', '2', '')('user', '2', '')'''

def test_deleteUsersFromFile_success():
  users = [User("Jess")]
  con = sqlite3.connect("mydatabase_testk.db")
  cursorObj = con.cursor()
  cursorObj.execute("CREATE TABLE User(name text, limits text, booksBorrowed text)")
  cursorObj.execute('''INSERT INTO User VALUES ('Jump', '2', '')''')
  cursorObj.execute('''INSERT INTO User VALUES ('Jess', '1', 'rabbit')''')
  con.commit()
  con.close()
  deleteUsersFromFile(users ,"mydatabase_testk.db")
  conn = sqlite3.connect("mydatabase_testk.db")
  cursorObjb = conn.cursor()
  data=cursorObjb.execute('''SELECT * FROM User''')
  string = ''
  for newLine in data:
    string = string + str(newLine)
  conn.commit()
  conn.close()
  os.remove('mydatabase_testk.db')
  assert string == '''('Jump', '2', '')'''