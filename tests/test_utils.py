import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from unittest.mock import MagicMock
from app.models import Message
from app.utils import sanitize_input

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