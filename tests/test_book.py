# tests/test_book.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import pytest
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.book import Book
from lib.models.author import Author
from lib.models.genre import Genre
from lib.models.sale import Sale
from datetime import datetime, timezone

@pytest.fixture
def setup_database():
    Base.metadata.create_all(engine)
    session = Session()
    author = Author(name="Test Author")
    genre = Genre(name="Test Genre")
    session.add_all([author, genre])
    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_book_creation(setup_database):
    session = setup_database
    author = session.query(Author).first()
    genre = session.query(Genre).first()
    book = Book(title="Test Book", author=author, genre=genre, price=9.99, quantity=5)
    session.add(book)
    session.commit()
    assert book.id is not None
    assert book.title == "Test Book"
    assert book.quantity == 5

def test_sell_book(setup_database):
    session = setup_database
    author = session.query(Author).first()
    genre = session.query(Genre).first()
    book = Book(title="Test Book", author=author, genre=genre, price=9.99, quantity=5)
    session.add(book)
    session.commit()
    book.quantity -= 2
    sale = Sale(book=book, quantity=2, total_price=19.98, sale_date=datetime.now(timezone.utc))
    session.add(sale)
    session.commit()
    assert book.quantity == 3
    assert len(book.sales) == 1
    assert book.sales[0].quantity == 2