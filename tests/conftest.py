import pytest
from app.main import app
from app.models import Message
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.database import Base, get_db

# Test database
@pytest.fixture(scope='session', autouse=True)
def test_db():
    # Test connection
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    '''
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    '''
    yield SessionLocal()

@pytest.fixture(scope='session')
def client(test_db):
    # Test client
    with TestClient(app) as tc:
        yield tc