import pytest
from app.main import app
from app.models import Message
from app.database import Base, engine, get_db
from fastapi.testclient import TestClient

# Test database
@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='session')
def client():
    # Test client
    with TestClient(app) as tc:
        yield tc