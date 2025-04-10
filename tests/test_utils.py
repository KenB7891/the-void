import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from unittest.mock import MagicMock
from app.models import Message
from app.utils import sanitize_input, get_client_ip, is_ip_allowed, MESSAGE_COOLDOWN_HOURS
from datetime import datetime, timedelta, timezone

def test_sanitize_input_html_removal():
    # Test HTML tag removal
    input_text = '<h1>Hello, World!</h1>'
    sanitized_text = sanitize_input(input_text)
    assert sanitized_text == 'Hello, World!'

def test_sanitize_input_link_removal():
    # Test URL removal
    input_text = 'Visit https://example.com for more info'
    sanitized_text = sanitize_input(input_text)
    assert sanitized_text == 'Visit  for more info'

def test_sanitize_input_combined_html_and_link_removal():
    # Test both HTML and URL removal
    input_text = '<a href="https://example.com">Click here</a>'
    sanitized_text = sanitize_input(input_text)
    assert sanitized_text == 'Click here'

def test_sanitize_input_no_html_or_links():
    # Test normal text with no HTML or URLs
    input_text = 'Hello, World!'
    sanitized_text = sanitize_input(input_text)
    assert sanitized_text == 'Hello, World!'

def test_sanitize_input_whitespace_removal():
    # Test removal of leading and trailing whitespace
    input_text = '  Hello, World!  '
    sanitized_text = sanitize_input(input_text)
    assert sanitized_text == 'Hello, World!'

def test_get_client_ip(client):
    # Mocking the client IP
    mock_request = MagicMock()
    mock_request.client.host = '192.168.1.100'  # Simulating an IP address

    client_ip = get_client_ip(mock_request)
    # Assert that the IP is the one we mocked
    assert client_ip == '192.168.1.100'

def test_is_ip_allowed_no_messages(test_db):
    # Empty test_db
    fake_ip = '192.168.1.100'
    allowed = is_ip_allowed(fake_ip, test_db)
    assert allowed is True

def test_is_ip_allowed_recent_message(test_db):
    # Add recent message that causes cooldown
    fake_ip = '192.168.1.100'
    message_time = datetime.now(timezone.utc) - timedelta(hours=MESSAGE_COOLDOWN_HOURS / 2)

    message = Message(ip=fake_ip, content='Testing', created_at=message_time)
    test_db.add(message)
    test_db.commit()

    allowed = is_ip_allowed(fake_ip, test_db)
    assert allowed is False

    test_db.delete(message)
    test_db.commit()

def test_is_ip_allowed_old_message(test_db):
    # Add old message that does not cause cooldown
    fake_ip = '192.168.1.100'
    message_time = datetime.now(timezone.utc) - timedelta(hours=MESSAGE_COOLDOWN_HOURS + 2)

    message = Message(ip=fake_ip, content='Testing', created_at=message_time)
    test_db.add(message)
    test_db.commit()

    allowed = is_ip_allowed(fake_ip, test_db)
    assert allowed is True

    test_db.delete(message)
    test_db.commit()