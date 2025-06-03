# lib/models/cashier.py
from sqlalchemy import Column, Integer, String
from lib.db.connection import Base

class Cashier(Base):
    __tablename__ = 'cashiers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Cashier(name={self.name})>"