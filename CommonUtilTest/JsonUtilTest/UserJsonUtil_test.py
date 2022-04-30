from CommonUtil.JsonUtil.UserJsonUtil import usersToJson
import pytest
from Model.User import User

def test_userToJson_success():
  users = [User("User_test",1,["book"]),User("User_test2"),User("User_test3",0,["book","banana"])]
  f = open("/home/runner/14-output-ThaTaerakul/CommonUtilTest/FilesForTest/JsonUtilTest/Users.json", "r")
  print(usersToJson(users))
  assert usersToJson(users) == f.read()