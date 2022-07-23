class Book(): 
    def __init__(self, name:str, isInLibrary:str = True, dateBorrowed:str = "unknown", user:str = "unknown"):
        self.name = name
        self.isInLibrary = isInLibrary
        self.dateBorrowed = dateBorrowed
        self.user = user
    def __str__(self): 
      return f"Name: {self.name}, isInLibrary: {self.isInLibrary}, dateBorrowed: {self.dateBorrowed}, user: {self.user}"