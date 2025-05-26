# lib/models/sale.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from lib.db.connection import Base

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    book = relationship("Book", back_populates="sales")

    def __repr__(self):
        return f"<Sale(book_id={self.book_id}, quantity={self.quantity}, total_price={self.total_price}, sale_date={self.sale_date})>"