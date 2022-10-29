from app.main.model.book import Book
from app.main.model.user import User
from typing import Dict, Tuple
from datetime import date, datetime, timedelta
from .. import db

def borrowBook(data: Dict[str, str], time:datetime = datetime.now()) -> Tuple[Dict[str, str], int]:
    book = Book.query.filter_by(bookname=data['bookname'],is_in_lib=True).first()
    user = User.query.filter_by(email=data['email']).filter(User.limits > 0).first()
    if not book:
        response_object = {
            'status': 'fail',
            'message': 'Sorry that book is not in the library.',
        }
        return response_object, 409
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'Sorry you own too many book.',
        }
        return response_object, 409
    book.is_in_lib = False
    book.user_id = user.id
    user.limits = User.limits - 1
    book.date_borrowed = time
    db.session.add(user)
    db.session.add(book)
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully borrowed.',
    }
    return response_object, 200

def calculateMoney(day:int) -> int:
    return day * 3 # 3 baht per day

def returnInTime(dateBorrowed:datetime, dateNow:datetime) -> int:
    dateBeforeReturn = dateBorrowed + timedelta(days = 7)
    dayDifferent = (dateNow - dateBeforeReturn).days
    if dayDifferent <= 0:
        return 0
    else:
        return dayDifferent

def returnBook(data: Dict[str, str], dateNow:datetime = datetime.now()) -> Tuple[Dict[str, str], int]:
    book = Book.query.filter_by(bookname=data['bookname'],is_in_lib=False).first()
    user = User.query.filter_by(email=data['email']).filter(User.limits < 2).first()
    if not book:
        response_object = {
            'status': 'fail',
            'message': 'sorry that book is in the library.',
        }
        return response_object, 409
    if not user:
        response_object = {
            'status': 'fail',
            'message': "sorry you don't own any book.",
        }
        return response_object, 409
    if (book not in user.books):
        response_object = {
            'status': 'fail',
            'message': "you did not borrow that book.",
        }
        return response_object, 409
    money = calculateMoney(returnInTime(book.date_borrowed, dateNow))
    book.is_in_lib = True
    book.user_id = None
    user.limits = User.limits + 1
    book.date_borrowed = None
    db.session.add(user)
    db.session.add(book)
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully returned.',
        "moneyown": str(money) + " baht"
    }
    return response_object, 200