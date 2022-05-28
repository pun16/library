import json
from Model.Book import Book
from typing import List

def booksToJson(books:List[Book]) -> str:
  booksJson = []
  for book in books:
    booksJson.append(book.__dict__)
  return json.dumps(booksJson, indent=4)