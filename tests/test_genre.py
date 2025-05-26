# tests/test_genre.py
import pytest
from sqlalchemy.orm import sessionmaker
from lib.db.connection import Base, engine, Session
from lib.models.genre import Genre

@pytest.fixture
def setup_database():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_genre_creation(setup_database):
    session = setup_database
    genre = Genre(name="Test Genre")
    session.add(genre)
    session.commit()
    assert genre.id is not None
    assert genre.name == "Test Genre"