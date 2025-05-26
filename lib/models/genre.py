# lib/models/genre.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.db.connection import Base

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return f"<Genre(name={self.name})>"