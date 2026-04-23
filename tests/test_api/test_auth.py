import pytest

from services.authentication_service import AuthServices

def test_login():
    auth_service = AuthServices()
    token = auth_service.get_token("diana@example.com", "password123")

    assert token

