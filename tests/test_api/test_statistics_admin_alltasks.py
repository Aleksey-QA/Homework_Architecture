import allure
import pytest

from services.authentication_service import AuthServices
from services.statictics_service import StaticServices

@pytest.fixture()
def auth_service():
    return AuthServices()

@pytest.fixture()
def statistics_service():
    return StaticServices()

@allure.step('Проверка получения ожидаемого массива объектов по запросу get_all_tasks_admin')
def test_assert_success_response(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 100, "status": None, "priority": None}, token)
    body = response.json()

    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list), "Ожидаемый 'tasks' отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    elif isinstance(body, list):
        assert all(isinstance(item, dict) for item in body), "Ожидаемый массив объектов tasks"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)


@allure.step('Проверка, что с пустыми значениями запрос выполняется успешно по запросу get_all_tasks_admin')
def test_get_without_parameters(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": None, "limit": None, "status": None, "priority": None}, token)
    body = response.json()

    if isinstance(body, dict):
        assert "tasks" in body and isinstance(body["tasks"], list), "Ожидаемый 'tasks' отсутствует в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' отсутствует в тексте ответа"
    else:
        pytest.fail("Что-то пошло не так: %r" % body)

@allure.step('Проверка, что с фильтрация по статусу "in_progress" отрабатывают корректно')
def test_all_tasks_filter_status_in_progress(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None}, token)
    body_all_status = response.json()
    # Подсчет задач со статусом "in_progress" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len([task for task in tasks if task["status"] == "in_progress"]) #кол-во тасок "in_progress" без фильтра

    # Подсчет задач со статусом "in_progress" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": "in_progress", "priority": None}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter) #кол-во тасок "in_progress" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по статусу in_progress работает неправильно"


@allure.step('Проверка, что с фильтрация по статусу "todo" отрабатывают корректно')
def test_all_tasks_filter_status_todo(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None}, token)
    body_all_status = response.json()
    # Подсчет задач со статусом "todo" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len([task for task in tasks if task["status"] == "todo"]) #кол-во тасок "todo" без фильтра

    # Подсчет задач со статусом "todo" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": "todo", "priority": None}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter) #кол-во тасок "todo" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по статусу todo работает неправильно"


@allure.step('Проверка, что с фильтрация по статусу "done" отрабатывают корректно')
def test_all_tasks_filter_status_done(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None}, token)
    body_all_status = response.json()
    # Подсчет задач со статусом "done" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len([task for task in tasks if task["status"] == "done"]) #кол-во тасок "done" без фильтра

    # Подсчет задач со статусом "done" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": "done", "priority": None}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter) #кол-во тасок "done" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по статусу done работает неправильно"

@allure.step('Проверка, что с фильтрация по приоритету "low" отрабатывают корректно')
def test_all_tasks_filter_priority_low(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None},
                                                      token)
    body_all_status = response.json()
    # Подсчет задач с приоритетом "low" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len(
        [task for task in tasks if task["priority"] == "low"])  # кол-во тасок "low" без фильтра

    # Подсчет задач с приоритетом "low" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": None, "priority": "low"}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter)  # кол-во тасок "low" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по приоритету low работает неправильно"

@allure.step('Проверка, что с фильтрация по приоритету "medium" отрабатывают корректно')
def test_all_tasks_filter_priority_medium(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None}, token)
    body_all_status = response.json()
    # Подсчет задач с приоритетом "medium" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len([task for task in tasks if task["priority"] == "medium"]) #кол-во тасок "medium" без фильтра

    # Подсчет задач с приоритетом "medium" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": None, "priority": "medium"}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter) #кол-во тасок "medium" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по приоритету done работает неправильно"


@allure.step('Проверка, что с фильтрация по приоритету "high" отрабатывают корректно')
def test_all_tasks_filter_priority_high(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": 0, "limit": 2000, "status": None, "priority": None},
                                                      token)
    body_all_status = response.json()
    # Подсчет задач с приоритетом "high" без фильтров
    tasks = body_all_status["tasks"]
    in_progress_count = len(
        [task for task in tasks if task["priority"] == "high"])  # кол-во тасок "high" без фильтра

    # Подсчет задач с приоритетом "medium" c вкл фильтром
    response_filter = statistics_service.get_all_tasks_admin(
        {"skip": 0, "limit": 2000, "status": None, "priority": "high"}, token)
    body_filter_status = response_filter.json()
    tasks_filter = body_filter_status["tasks"]
    filter_in_progress_count = len(tasks_filter)  # кол-во тасок "high" c включенным фильтром

    assert in_progress_count == filter_in_progress_count, "Фильтрация по приоритету high работает неправильно"


@allure.step('Проверка отработки запроса get_all_tasks_admin с невалидными значениями')
@pytest.mark.parametrize("skip, limit, status, priority", [
    ("abc", None, None, None),
    (None, "ten", None, None),
    ("1.5", None, None, None),
    (None, "2.7", "None", None)
])
def test_invalid_integer_params_trigger_validation(auth_service, statistics_service, skip, limit, status, priority):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_tasks_admin({"skip": skip, "limit": limit, "status": status, "priority": priority}, token)
    data = response.json()

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




