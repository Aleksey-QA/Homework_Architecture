import json

import allure
import pytest
import requests

@pytest.mark.parametrize("email, password", [("diana@example.com", "password123"),
                                             ("admin@example.com", "admin123"),
                                             ],
                         ids=['simple user', 'admin'])
def login(email, password):
    url = "http://localhost:8000/auth/login"

    payload = json.dumps({
      "email": email,
      "password": password
    })

    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res_json = response.json()

    assert response.status_code == 200
    assert res_json['access_token']
    assert res_json['token_type'] == 'bearer'

@allure.sub_suite('Тестирование API login')
@pytest.mark.apilogin
def test_login_ai():
    import requests
    import time

    # ── Pre-request ──────────────────────────────────────────────
    url = "http://localhost:8000/auth/login"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    body = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    # ── Отправка запроса ─────────────────────────────────────────
    start_time = time.time()
    response = requests.post(url, headers=headers, json=body)
    response_time_ms = (time.time() - start_time) * 1000

    # ── Post-response тесты ──────────────────────────────────────
    data = response.json()

    # 1. Status code is 200
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✅ Status code is 200")

    # 2. Response time is below 1000ms
    assert response_time_ms < 1000, f"Response time {response_time_ms:.0f}ms >= 1000ms"
    print(f"✅ Response time is below 1000ms ({response_time_ms:.0f}ms)")

    # 3. Response has a JSON body
    assert isinstance(data, dict), "Response is not a JSON object"
    print("✅ Response has a JSON body")

    # 4. Field 'access_token' exists and is a string
    assert "access_token" in data, "Field 'access_token' is missing"
    assert isinstance(data["access_token"], str), "Field 'access_token' is not a string"
    print("✅ Field 'access_token' exists and is a string")

    # 5. Field 'token_type' exists and equals 'bearer'
    assert "token_type" in data, "Field 'token_type' is missing"
    assert isinstance(data["token_type"], str), "Field 'token_type' is not a string"
    assert data["token_type"].lower() == "bearer", f"Expected 'bearer', got '{data['token_type']}'"
    print("✅ Field 'token_type' exists and equals 'bearer'")

    print("\n✅ All tests passed!")
    print(f"access_token: {data['access_token'][:50]}...")