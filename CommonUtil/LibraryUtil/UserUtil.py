from Model.User import User
from typing import List

def findUser(userName:str,users:List[User]) -> User:
  for user in users:
    if user.name == userName:
      return user
  raise Exception("can not find the user")

def showUser(users:List[User]) -> None:
  for user in users:
    print(user.name)

def isUsernameValid(name:str) -> bool:
  return not(" " in name or len(name) < 3 or len(name) >20)