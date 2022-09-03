import uuid
import datetime

from app.main import db
from app.main.model.book import Book
from typing import Dict, Tuple


def save_new_book(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    book = Book.query.filter_by(bookname=data['bookname']).first()
    if not book:
        new_book = Book(
            bookname=data['bookname'],
            is_in_lib=True,
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_book)
        return generate_response_object()
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book already exists.',
        }
        return response_object, 409


def get_all_book():
    return Book.query.all()


def get_a_book(bookname):
    return Book.query.filter_by(bookname=bookname).first()


def generate_response_object() -> Tuple[Dict[str, str], int]:
    response_object = {
        'status': 'success',
        'message': 'Successfully registered book.'
    }
    return response_object, 201

def save_changes(data: Book) -> None:
    db.session.add(data)
    db.session.commit()