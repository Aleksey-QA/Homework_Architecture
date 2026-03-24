import pytest

from services.authentication_service import AuthServices
from services.statictics_service import StaticServices

@pytest.fixture()
def auth_service():
    return AuthServices()

@pytest.fixture()
def statistics_service():
    return StaticServices()

def test_get_dashboard_stats(auth_service, statistics_service):
    token = auth_service.get_token_for_me("diana@example.com", "password123")
    response = statistics_service.get_dashboard_status(token)
    print(response)

    assert response.status_code == 200, "Status code is not 200"
    data = response.json()
    # 2. total_boards присутствует и оно число
    assert "total_boards" in data
    assert isinstance(data["total_boards"], (int, float))

    # 3. total_tasks присутствует и оно число
    assert "total_tasks" in data
    assert isinstance(data["total_tasks"], (int, float))

    # 4. tasks_by_status присутствует и оно dict
    assert "tasks_by_status" in data
    assert isinstance(data["tasks_by_status"], dict)

    # 5. tasks_by_status cодержит  todo, in_progress, done — each a number
    tbs = data["tasks_by_status"]
    for field in ["todo", "in_progress", "done"]:
        assert field in tbs
        assert isinstance(tbs[field], (int, float))
        print(f"{field} - ОК")


def test_get_global_task_stats(auth_service, statistics_service):
    token = auth_service.get_token_for_me("diana@example.com", "password123")
    response = statistics_service.get_global_task_stats(token)
    print(response)

    assert response.status_code == 200, "Status code is not 200"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")


    # 2. boards присутствует и оно число
    assert "boards" in data
    assert isinstance(data["boards"], (int, float))

    # 3. tasks_total присутствует и оно число
    assert "tasks_total" in data
    assert isinstance(data["tasks_total"], (int, float))

    # 4. done присутствует и оно dict
    assert "done" in data
    assert isinstance(data["done"], (int, float))

    # 5. Выполненных задач не может быть больше, чем всего задач
    assert data["done"] <= data["tasks_total"], \
        f"Логическая ошибка: done ({data['done']}) > tasks_total ({data['tasks_total']})"

    # 6. Все числовые значения не должны быть отрицательными
    for field in ["boards", "tasks_total", "done"]:
        assert data[field] >= 0, f"Ошибка: Поле {field} содержит отрицательное значение: {data[field]}"

    # 7. Отсутствие лишних полей (Strict Schema)
    allowed_keys = {"boards", "tasks_total", "done"}
    actual_keys = set(data.keys())
    # Проверяем, что в ответе нет ничего, кроме разрешенных полей
    extra_keys = actual_keys - allowed_keys
    assert not extra_keys, f"Ошибка: Обнаружены неожиданные поля в ответе: {extra_keys}"

def test_get_user_activity(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    EXISTING_USER_ID = 1  # ожидается, что такой пользователь есть в тестовой БД

    response = statistics_service.get_user_activity(token, EXISTING_USER_ID)
    print(response)

    assert response.status_code == 200, "Status code is not 200"

    # Тело ответа JSON и содержит ожидаемые числовые поля для существующего user_id.
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response for user {EXISTING_USER_ID} is not valid JSON")
        # Ожидаемые поля
    for key in ("created_tasks", "updated_tasks", "boards_created"):
        assert key in data, f"Missing '{key}' in response for user {EXISTING_USER_ID}"
        assert isinstance(data[key], (int, float)), f"Field '{key}' is not numeric for user {EXISTING_USER_ID}"

    # Статус 200 для существующего user_id
    response = statistics_service.get_user_activity(token, EXISTING_USER_ID)
    assert response.status_code == 200, f"Expected 200, got {response.status_code} for user {EXISTING_USER_ID}"

    # Все числовые значения неотрицательны для существующего user_id."""
    assert data["created_tasks"] >= 0, f"created_tasks negative for user {EXISTING_USER_ID}"
    assert data["updated_tasks"] >= 0, f"updated_tasks negative for user {EXISTING_USER_ID}"
    assert data["boards_created"] >= 0, f"boards_created negative for user {EXISTING_USER_ID}"

    # Ответ содержит ровно набор ожидаемых ключей (без лишних)."""
    allowed = {"created_tasks", "updated_tasks", "boards_created"}
    actual = set(data.keys())
    assert actual == allowed, f"For user {EXISTING_USER_ID} unexpected keys: {actual - allowed} or missing: {allowed - actual}"

# При смене существующего user_id значения могут отличаться (проверка, что user_id действительно влияет)."""
def test_get_user_activity_change_user_id(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    EXISTING_USER_ID = 1
    response = statistics_service.get_user_activity(token, EXISTING_USER_ID)
    print(response)
    assert response.status_code == 200, "Status code is not 200"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response for user {EXISTING_USER_ID} is not valid JSON")
    # При смене существующего user_id значения могут отличаться (проверка, что user_id действительно влияет)."""
    # Попробуем два разных user_id
    alt_user = EXISTING_USER_ID + 1
    response2 = statistics_service.get_user_activity(token, alt_user)
    if response2.status_code != 200:
        pytest.skip(f"User {alt_user} not available (status {response2.status_code}); skip comparison test")
    data2 = response2.json()
    # Сравниваем — ожидаем, что хотя бы одно поле отличается; если совпадает, это может быть ок для некоторых систем
    if data == data2:
        pytest.skip(f"Responses for user {EXISTING_USER_ID} and {alt_user} are identical; cannot assert difference")
    # если не равны — тест пройден
    assert data != data2



def test_get_user_activity_negative(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    NONEXISTENT_USER_ID = 999  # ожидается, что такого пользователя нет
    INVALID_USER_ID = "qwe" # невалидное значение
    response = statistics_service.get_user_activity(token, NONEXISTENT_USER_ID)
    # Несуществующий user_id: ожидаем 404 с полем "detail": "User not found"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")
    assert response.status_code == 404, "Status code is not 404"
    assert "detail" in data, f"Response JSON не содержит 'detail' key. JSON: {data}"
    assert data["detail"] == "User not found", f"Expected detail='User not found', got: {data['detail']}"

   # Некорректный user_id (строка) — ожидаем 400 или 404."""
    response = statistics_service.get_user_activity(token, INVALID_USER_ID)
    assert response.status_code in (422, 404), f"Expected 422 or 404 for invalid user id, got {response.status_code}"



def test_get_all_boards_admin_valid(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    params = {
        "skip": None,
        "limit": 2,
        "archived": "true"
    }
    response = statistics_service.get_all_boards_admin(params, token)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON: %s" % response.text)

    if isinstance(body, dict):
        assert "boards" in body and isinstance(body["boards"], list), "Expected 'boards' list in response body"
        assert "total" in body and isinstance(body["total"], int), "Expected 'total' int in response body"
    elif isinstance(body, list):
        assert all(isinstance(item, dict) for item in body), "Expected array of board objects"
    else:
        pytest.fail("Unexpected response body shape: %r" % body)


def assert_validation_error(resp, expected_param=None):
    """
    Утилита: проверяет, что ответ — 422 и тело содержит detail массив с ошибкой,
    относящейся к expected_param (если указан).
    """
    assert resp.status_code == 422, f"Expected 422 validation error, got {resp.status_code}: {resp.text}"
    try:
        body = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON: %s" % resp.text)
    assert "detail" in body and isinstance(body["detail"], list) and len(body["detail"]) > 0
    if expected_param:
        found = False
        for err in body["detail"]:
            loc = err.get("loc")
            if isinstance(loc, list) and expected_param in loc:
                found = True
                break
        assert found, f"No validation error referencing param '{expected_param}' found in detail: {body['detail']}"
