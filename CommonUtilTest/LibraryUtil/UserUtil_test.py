from CommonUtil.LibraryUtil.UserUtil import findUser,isUsernameValid
from Model.User import User
import pytest

def test_find_user_success():
  users = [User("test")]
  userName = "test"
  user = findUser(userName,users)
  assert user.name == "test"

def test_find_user_failed():
  users = [User("tes")]
  userName = "test"
  with pytest.raises(Exception, match=r"can not find the user"):
    findUser(userName,users)

def test_isUsernameValid_success():
  assert isUsernameValid("valid")

def test_isUsernameValid_max_len_fail():
  assert isUsernameValid("thisistoooooooooolong") == False

def test_isUsernameValid_min_len_fail():
  assert isUsernameValid("a") == False

def test_isUsernameValid_space_fail():
  assert isUsernameValid("test fail") == False