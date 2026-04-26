"""Модуль с тестами для API статистики."""
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
    token = auth_service.get_token_for_me("charlie@example.com", "password123")
    response = statistics_service.get_dashboard_status(token)

    data = response.json()
    # 1. total_boards для diana@example.com
    assert data["total_boards"] == 44
    # 2. total_tasks для diana@example.com
    assert data["total_tasks"] == 1700
    # 3. tasks_by_status для diana@example.com содержит
    assert data["tasks_by_status"]["todo"] == 702
    assert data["tasks_by_status"]["in_progress"] == 495
    assert data["tasks_by_status"]["done"] == 503

@allure.step('Проверка глобальной статистики по пользователю diana@example.com')
def test_get_global_task_stats(auth_service, statistics_service):
    token = auth_service.get_token_for_me("charlie@example.com", "password123")
    response = statistics_service.get_global_task_stats(token)

    data = response.json()
    # 1. boards для diana@example.com = 23
    assert data["boards"] == 47
    # 2. total_tasks для diana@example.com = 1368
    assert data["tasks_total"] == 1700
    # 3. done tasks для diana@example.com = 404
    assert data["done"] == 503

    # 4. Выполненных задач не может быть больше, чем всего задач \ Почему нет?
    assert data["done"] <= data["tasks_total"], \
        f"Логическая ошибка: done ({data['done']}) > tasks_total ({data['tasks_total']})"

    # 5. Все числовые значения не должны быть отрицательными ? Почему нет?
    for field in ["boards", "tasks_total", "done"]:
        assert data[field] >= 0, (f"Ошибка: Поле {field} содержит отрицательное "
                                  f"значение: {data[field]}")


@allure.step('Проверка активности существующего пользователя')
def test_get_user_activity(auth_service, statistics_service):
    token = auth_service.get_token_for_me("charlie@example.com", "password123")
    existing_user_id = 5
    response = statistics_service.get_user_activity(token, existing_user_id )
    data = response.json()

    # 1. created_tasks для admin@example.com = 274
    assert data["created_tasks"] == 315
    # 2. updated_tasks для admin@example.com = 274
    assert data["updated_tasks"] == 315
    # 3. boards_created для admin@example.com = 339
    assert data["boards_created"] == 8

@allure.step('Проверка активности несуществующего пользователя')
def test_get_user_activity_negative(auth_service, statistics_service):
    token = auth_service.get_token_for_me("charlie@example.com", "password123")
    nonexistent_user_id = 999  # ожидается, что такого пользователя нет
    response = statistics_service.get_user_activity(token, nonexistent_user_id)

    data = response.json()
    # Несуществующий user_id: ожидаем 404 с полем "detail": "User not found"
    assert response.status_code == 404, "Status code is not 404"
    assert data["detail"] == "User not found", (f"Expected detail='User not found', "
                                                f"got: {data['detail']}")
