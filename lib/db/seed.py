# lib/db/seed.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.author import Author
from lib.models.genre import Genre
from lib.models.book import Book
from lib.models.sale import Sale
from datetime import datetime, timezone

def seed_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    
    # Sample data
    author1 = Author(name="J.K. Rowling")
    author2 = Author(name="George Orwell")
    genre1 = Genre(name="Fantasy")
    genre2 = Genre(name="Dystopian")
    book1 = Book(title="Harry Potter", author=author1, genre=genre1, price=19.99, quantity=10)
    book2 = Book(title="1984", author=author2, genre=genre2, price=14.99, quantity=15)
    sale1 = Sale(book=book1, quantity=2, total_price=39.98, sale_date=datetime(2025, 5, 25, tzinfo=timezone.utc))
    sale2 = Sale(book=book2, quantity=1, total_price=14.99, sale_date=datetime(2025, 5, 26, tzinfo=timezone.utc))
    
    session.add_all([author1, author2, genre1, genre2, book1, book2, sale1, sale2])
    session.commit()
    session.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()