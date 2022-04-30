from Model.Book import Book
from typing import List
from datetime import date,timedelta

def isLibraryOutOfBooks(books:List[Book]) -> bool:
  numOfBook = 0
  for book in books:
    if book.isInLibrary == True:
      numOfBook += 1
  if numOfBook == 0:
    return True
  else:
    return False

def isLibraryFull(books:List[Book]) -> bool:
  numOfBook = 0
  for book in books:
    if book.isInLibrary == False:
      numOfBook += 1
  if numOfBook == 0:
    return True
  else:
    return False

def returnInTime(dateBorrowed:str) -> int:
  y = int(dateBorrowed[0:4])
  mo = int(dateBorrowed[5:7])
  d = int(dateBorrowed[8:10])
  dateBeforeReturn = date(y, mo, d) + timedelta(days = 7)
  today = date.today()
  dayDifferent = (today - dateBeforeReturn).days
  if dayDifferent <= 0:
    return 0
  else:
    return dayDifferent

def calculateMoney(day:int) -> int:
  return day * 3

def printData(dataList:List) -> None:
  for data in dataList:
    print(data)

