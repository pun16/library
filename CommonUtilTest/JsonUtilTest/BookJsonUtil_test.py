from CommonUtil.JsonUtil.BookJsonUtil import booksToJson
import pytest
from Model.Book import Book

def test_bookToJson_success():
  books = [Book("book_test"),Book("book_test2")]
  f = open("/home/runner/14-output-ThaTaerakul/CommonUtilTest/FilesForTest/JsonUtilTest/Books.json", "r")
  assert booksToJson(books) == f.read()