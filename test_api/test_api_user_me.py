import allure
import pytest
import requests
import re

@allure.sub_suite('Тестирование API User me')
def test_get_jwt_token():
    # --- Pre-request: получаем JWT токен (аналог pre-request script) ---
    login_response = requests.post(
        "http://localhost:8000/auth/login",
        headers={"Content-Type": "application/json", "accept": "application/json"},
        json={"email": "admin@example.com", "password": "admin123"}
    )
    jwt_token = login_response.json()["access_token"]
    print(jwt_token)
    # --- Основной запрос ---
    response = requests.get(
        "http://localhost:8000/users/me",
        headers={"accept": "application/json", "Authorization": f"Bearer {jwt_token}"}
    )
    # --- Post-response: тесты (аналог test script) ---
    data = response.json()
    assert response.status_code == 200, "Status code is not 200"
    assert response.elapsed.total_seconds() * 1000 < 1000, "Response time >= 1000ms"
    assert isinstance(data, dict), "Response is not JSON"
    assert "id" in data and isinstance(data["id"], int), "Field 'id' missing or not a number"
    assert "username" in data and isinstance(data["username"], str), "Field 'username' missing or not a string"
    assert "email" in data and isinstance(data["email"], str) and re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", data["email"]), "Field 'email' invalid"
    assert "role" in data and isinstance(data["role"], str), "Field 'role' missing or not a string"
    assert "created_at" in data and isinstance(data["created_at"], str) and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", data["created_at"]), "Field 'created_at' invalid"
    assert "avatar_url" in data and (data["avatar_url"] is None or isinstance(data["avatar_url"], str)), "Field 'avatar_url' missing or wrong type"

    print("All tests passed!")
    print(data)