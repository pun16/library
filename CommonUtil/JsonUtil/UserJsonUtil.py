import json
from Model.User import User
from typing import List

def usersToJson(users:List[User]) -> str:
  usersJson = []
  for user in users:
    usersJson.append(user.__dict__)
  return json.dumps(usersJson, indent=4)