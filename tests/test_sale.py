# tests/test_sale.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import pytest
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.sale import Sale
from lib.models.book import Book
from lib.models.author import Author
from lib.models.genre import Genre
from datetime import datetime, timezone

@pytest.fixture
def setup_database():
    Base.metadata.create_all(engine)
    session = Session()
    author = Author(name="Test Author")
    genre = Genre(name="Test Genre")
    book = Book(title="Test Book", author=author, genre=genre, price=9.99, quantity=5)
    session.add_all([author, genre, book])
    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_sale_creation(setup_database):
    session = setup_database
    book = session.query(Book).first()
    sale = Sale(book=book, quantity=2, total_price=19.98, sale_date=datetime.now(timezone.utc))
    session.add(sale)
    session.commit()
    assert sale.id is not None
    assert sale.quantity == 2
    assert sale.total_price == 19.98
    assert sale.book_id == book.id