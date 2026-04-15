import pytest

from services.authentication_service import AuthServices
from services.statictics_service import StaticServices

@pytest.fixture()
def auth_service():
    return AuthServices()

@pytest.fixture()
def statistics_service():
    return StaticServices()

@pytest.fixture()
def take_response(auth_service, statistics_service):
    def _take_response(params=None):
        token = auth_service.get_token_for_me("admin@example.com", "admin123")
        response = statistics_service.get_all_tasks_admin(params, token)
        return response
    return _take_response

def test_assert_success_response(take_response):
    response = take_response({"skip": 0, "limit": 100, "status": None, "priority": None})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Ответ неверен в формате JSON: %s" % response.text)

    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list), "Ожидаемый 'tasks'отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    elif isinstance(body, list):
        assert all(isinstance(item, dict) for item in body), "Ожидаемый массив объектов tasks"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)


# Проверка, что с пустыми значениями запрос выполняется успешно
def test_get_without_parameters(take_response):
    response = take_response({"skip": None, "limit": None, "status": None, "priority": None})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Ответ неверен в формате JSON: %s" % response.text)
    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list), "Ожидаемый 'tasks' отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)




# Проверка, что с фильтр по статусу и приоритету отрабатывают корректно
@pytest.mark.parametrize("skip, limit, status, priority", [
    (1, 100, "ALL", None),
    (1, 100, None, "ALL")
])
def test_get_empty_list(take_response, skip, limit, status, priority):
    response = take_response({"skip": skip, "limit": limit, "status": status, "priority": priority})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Ответ неверен в формате JSON: %s" % response.text)
    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list) and body["tasks"] == [], "Ожидаемый 'tasks' отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)



# Позитивные кейсы
@pytest.mark.parametrize("skip, limit, status, priority", [
    (0, 1, None, None),
    (1, 10, None, None),
    (2, 3, None, None),
])
def test_get_with_valid_values(take_response, skip, limit, status, priority):
    response = take_response({"skip": skip, "limit": limit, "status": status, "priority": priority})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Ответ неверен в формате JSON: %s" % response.text)
    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list), "Ожидаемый 'tasks' отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    elif isinstance(body, list):
        assert all(isinstance(item, dict) for item in body), "Ожидаемый массив объектов tasks"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)


# Проверка, отработки запроса с невалидными значениями
@pytest.mark.parametrize("skip, limit, status, priority", [
    ("abc", None, None, None),
    (None, "ten", None, None),
    ("1.5", None, None, None),
    (None, "2.7", "None", None)
])
def test_invalid_integer_params_trigger_validation(take_response, skip, limit, status, priority):
    response = take_response({"skip": skip, "limit": limit, "status": status, "priority": priority})
    assert response.status_code == 422, f" Ожидали получить 422 ошибку, got {response.status_code}: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f" ответ не в виде JSON. Status: {response.status_code}, Body: {response.text}")

    # Проверяем наличие detail и что это непустой список
    assert "detail" in data, f"'detail' не находится в JSON: {data}"
    assert isinstance(data["detail"], list) and len(
        data["detail"]) > 0, f"'detail' должен быть не пустой список, получили: {data.get('detail')}"

    # Проверяем наличие поля msg и точное соответствие ожидаемой строки
    print(data)
    for error in data["detail"]:
        actual_msg = error.get('msg')
    EXPECTED_MSG = "Input should be a valid integer, unable to parse string as an integer"
    assert actual_msg == EXPECTED_MSG, f" Параметр 'msg' не совпадает с ожидаемым: Expected: '{EXPECTED_MSG}', Actual: '{actual_msg}'"





# Проверка, что поля status и priority соответствуют допустимым значениям
def test_status_values(take_response):
    response = take_response({"skip": 0, "limit": 100, "status": None, "priority": None})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    try:
        body = response.json()
    except ValueError:
        pytest.fail("Ответ неверен в формате JSON: %s" % response.text)

    VALID_STATUSES = {"todo", "in_progress", "done"}
    VALID_PRIORITY = {"low", "medium", "high"}
    tasks = body["tasks"]
    for task in tasks:
        status = task.get("status")
        priority = task.get("priority")
        assert status in VALID_STATUSES, f"Недопустимый статус '{status}' в задаче {task.get('id')}"
        assert priority in VALID_PRIORITY, f"Недопустимый статус '{priority}' в задаче {task.get('id')}"
