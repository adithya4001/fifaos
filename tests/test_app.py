import pytest
from solution import hash_password, verify_password, normalize_key

def test_password_hashing():
    password = "SecurePassword123!"
    salt, hashed = hash_password(password)
    assert verify_password(password, salt, hashed) == True

def test_password_failure():
    password = "SecurePassword123!"
    salt, hashed = hash_password(password)
    assert verify_password("WrongPassword!", salt, hashed) == False

def test_normalize_key():
    assert normalize_key(" UserEmail@Test.com ") == "useremail@test.com"
    assert normalize_key(None) == ""
