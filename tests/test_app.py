import pytest
import os
import json
from pathlib import Path
from solution import (
    hash_password, verify_password, normalize_key, 
    normalize_text, default_user_store, normalize_user_store
)

def test_password_hashing_and_verification():
    password = "SuperSecretFifa2026!"
    salt, hashed = hash_password(password)
    assert verify_password(password, salt, hashed) is True
    assert verify_password("WrongPassword!", salt, hashed) is False

def test_normalize_key():
    assert normalize_key(" FanEmail@FIFA.com ") == "fanemail@fifa.com"
    assert normalize_key(None) == ""
    assert normalize_key("ORG-123") == "org-123"

def test_normalize_text():
    assert normalize_text("  John Doe  ") == "John Doe"
    assert normalize_text(None) == ""

def test_default_user_store():
    store = default_user_store()
    assert "Audience" in store
    assert "Organizer" in store
    assert "Volunteer" in store
    assert isinstance(store["Audience"], list)

def test_normalize_user_store():
    raw_data = {
        "Audience": [{"name": "Test Fan"}],
        "Organizer": "Invalid Data", # Should be filtered out
        "Volunteer": [{"volunteer_id": "VOL-001"}]
    }
    clean_store = normalize_user_store(raw_data)
    assert isinstance(clean_store["Organizer"], list)
    assert len(clean_store["Organizer"]) == 0
    assert len(clean_store["Audience"]) == 1
