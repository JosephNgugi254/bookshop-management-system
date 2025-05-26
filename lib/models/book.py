# lib/models/book.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from lib.db.connection import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    sales = relationship("Sale", back_populates="book")  # Add this line

    def __repr__(self):
        return f"<Book(title={self.title}, price={self.price}, quantity={self.quantity})>"