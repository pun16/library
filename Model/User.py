from typing import List
class User:
  def __init__(self, name:str,limit:int = 2,booksBorrowed:List[str] = list()):
    self.name = name
    self.limit = limit
    self.booksBorrowed = booksBorrowed
  def __str__(self): 
        return f"Name: {self.name}, limit: {self.limit}, booksBorrowed: {self.booksBorrowed}"