import pytest

from services.authentication_service import AuthServices


@pytest.mark.parametrize("email, password",
                         [("diana@example.com", "password123"), ],
                         ids=["simple user"], )
def test_login(email, password):
    auth_service = AuthServices()
    token = auth_service.get_token(email, password)

    assert token

