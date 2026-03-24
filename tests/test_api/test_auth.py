import pytest

from services.authentication_service import AuthServices


@pytest.mark.parametrize("email, password",
                         [("diana@example.com", "password123"), ],
                         ids=["simple user"], )
def test_login(email, password):
    auth_service = AuthServices()
    token = auth_service.get_token(email, password)

    assert token


@pytest.mark.parametrize(
    "email, password",
    [
        ("diana1@example.com", "password123"),
        ("diana@example.com", "password1123"),
        ("diana1@example.com", "password1123"),
    ],
    ids=["wrong email", "wrong password", "wrong email and password"],
)
def test_login_negative(email, password):
    auth_service = AuthServices()
    response = auth_service.get_token(email, password)

    assert response["detail"] == "Incorrect email or password"

#
# def test_healthy():
#     response = make_request("GET", "health")
#
#     assert response["status"] == "ok"
#     assert response["memory"]["used_mb"]
#     assert response.get("memory", False).get("percent", False)
#     assert response.get("cpu", False).get("percent", False)
#
#