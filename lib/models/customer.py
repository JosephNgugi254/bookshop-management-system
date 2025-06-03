# lib/models/customer.py
from sqlalchemy import Column, Integer, String
from lib.db.connection import Base
import re

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = self._validate_phone(phone_number)

    def _validate_phone(self, phone):
        pattern = r'^07\d{8}$'
        if not re.match(pattern, phone):
            raise ValueError("Phone number must be in format 07xxxxxxxx (10 digits starting with 07).")
        return phone

    def __repr__(self):
        return f"<Customer(name={self.name}, phone_number={self.phone_number})>"