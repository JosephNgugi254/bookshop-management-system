# lib/db/seed.py
import os
import sys
# Point to the project root (bookshop-management-system/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.author import Author
from lib.models.genre import Genre
from lib.models.book import Book

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
    
    session.add_all([author1, author2, genre1, genre2, book1, book2])
    session.commit()
    session.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()