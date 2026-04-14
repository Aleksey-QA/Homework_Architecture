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

@allure.step('Проверка статистики по пользователю diana@example.com')
def test_get_dashboard_stats(auth_service, statistics_service):
    token = auth_service.get_token_for_me("diana@example.com", "password123")
    response = statistics_service.get_dashboard_status(token)

    data = response.json()
    # 1. total_boards для diana@example.com = 20
    assert data["total_boards"] == 20
    # 2. total_tasks для diana@example.com = 1148
    assert data["total_tasks"] == 1148
    # 3. tasks_by_status для diana@example.com содержит todo: 473, in_progress: 336, done: 339
    assert data["tasks_by_status"]["todo"] == 473
    assert data["tasks_by_status"]["in_progress"] == 336
    assert data["tasks_by_status"]["done"] == 339

@allure.step('Проверка глобальной статистики по пользователю diana@example.com')
def test_get_global_task_stats(auth_service, statistics_service):
    token = auth_service.get_token_for_me("diana@example.com", "password123")
    response = statistics_service.get_global_task_stats(token)

    data = response.json()
    # 1. boards для diana@example.com = 23
    assert data["boards"] == 23
    # 2. total_tasks для diana@example.com = 1148
    assert data["tasks_total"] == 1148
    # 3. total_tasks для diana@example.com = 339
    assert data["done"] == 339

    # 4. Выполненных задач не может быть больше, чем всего задач \ Почему нет?
    assert data["done"] <= data["tasks_total"], \
        f"Логическая ошибка: done ({data['done']}) > tasks_total ({data['tasks_total']})"

    # 5. Все числовые значения не должны быть отрицательными ? Почему нет?
    for field in ["boards", "tasks_total", "done"]:
        assert data[field] >= 0, f"Ошибка: Поле {field} содержит отрицательное значение: {data[field]}"


@allure.step('Проверка активности существующего пользователя')
def test_get_user_activity(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    EXISTING_USER_ID = 1
    response = statistics_service.get_user_activity(token, EXISTING_USER_ID)
    data = response.json()

    # 1. created_tasks для admin@example.com = 234
    assert data["created_tasks"] == 234
    # 2. updated_tasks для diana@example.com = 234
    assert data["updated_tasks"] == 234
    # 3. boards_created для diana@example.com = 339
    assert data["boards_created"] == 5

@allure.step('Проверка активности несуществующего пользователя')
def test_get_user_activity_negative(auth_service, statistics_service): #Почему нет?
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    NONEXISTENT_USER_ID = 999  # ожидается, что такого пользователя нет
    response = statistics_service.get_user_activity(token, NONEXISTENT_USER_ID)

    data = response.json()
    # Несуществующий user_id: ожидаем 404 с полем "detail": "User not found"
    assert response.status_code == 404, "Status code is not 404"  #Почему нет?
    assert data["detail"] == "User not found", f"Expected detail='User not found', got: {data['detail']}"




