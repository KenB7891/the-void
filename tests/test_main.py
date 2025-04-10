import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Message
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from unittest.mock import MagicMock


def test_yell_valid(client, test_db):
    # Valid message
    message = {'message': 'Hello Void!'}
    response = client.post("/yell", json=message)
    assert response.status_code == 200
    client.get('/peek')

def test_yell_empty_message(client, test_db):
    # Submit empty message
    message = {'message': ''}
    response = client.post("/yell", json=message)
    assert response.status_code == 400

def test_yell_ip_on_cooldown(client, test_db):
    # Submitting during cooldown period
    message_one = {'message': 'First Message'}
    client.post("/yell", json=message_one)

    message_two = {'message': 'Second Message!'}
    response = client.post("/yell", json=message_two)
    assert response.status_code == 429
    client.get('/peek')
    client.get('/peek')

def test_peek_empty(client, test_db):
    # Peeking with empty test_db
    response = client.get("/peek")
    assert response.status_code == 404

def test_peek_with_message(client, test_db):
    # Peeking with non-empty test_db
    message = {'message': 'Hello Void!'}
    client.post("/yell", json=message)
    response = client.get("/peek")    
    assert response.status_code == 200


