# tests/test_author.py
import pytest
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.author import Author

@pytest.fixture
def setup_database():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_author_creation(setup_database):
    session = setup_database
    author = Author(name="Test Author")
    session.add(author)
    session.commit()
    assert author.id is not None
    assert author.name == "Test Author"