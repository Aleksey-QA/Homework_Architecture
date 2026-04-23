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

@allure.step('Проверка получения ожидаемого массива объектов')
def test_get_all_boards_admin_valid(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    params = {"skip": None, "limit": 2, "archived": "true"}
    response = statistics_service.get_all_boards_admin(params, token)
    body = response.json()

    if isinstance(body, dict):
        assert "boards" in body and isinstance(body["boards"], list), "Ожидаемый 'boards' в тексте ответа"
        assert "total" in body and isinstance(body["total"], int), "Ожидаемый 'total' в тексте ответа"
    elif isinstance(body, list):
        assert all(isinstance(item, dict) for item in body), "Ожидаемый массив объектов board"
    else:
        pytest.fail(f"Что-то пошло не так: {body}")


@allure.step('Проверка, что с пустыми значениями запрос выполняется успешно')
def test_get_without_parameters(auth_service, statistics_service):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    params = {"skip": None, "limit": None, "archived": None}
    response = statistics_service.get_all_boards_admin(params, token)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"

@allure.step('Проверка отправки запроса получения досок с невалидными параметрами')
@pytest.mark.parametrize("skip, limit, archived", [
    ("abc", None, True),
    (None, "ten", False),
    ("1.5", None, None),
    (None, "2.7", None),
])
def test_invalid_integer_params_trigger_validation(auth_service, statistics_service, skip, limit, archived):
    token = auth_service.get_token_for_me("admin@example.com", "admin123")
    response = statistics_service.get_all_boards_admin({"skip": skip, "limit": limit, "archived": archived}, token)

    assert response.status_code == 422, (f" Ожидали получить 422 ошибку, "
                                         f"got {response.status_code}: {response.text}")
    data = response.json()

    # Проверяем наличие detail и что это непустой список
    assert "detail" in data, f"'detail' не находится в JSON: {data}"
    assert isinstance(data["detail"], list) and len(
        data["detail"]) > 0, f"'detail' должен быть не пустой список, получили: {data.get('detail')}"

    # Проверяем наличие поля msg и точное соответствие ожидаемой строки
    print(data)
    for error in data["detail"]:
        actual_msg = error.get('msg')
    expected_msg = "Input should be a valid integer, unable to parse string as an integer"
    assert actual_msg == expected_msg, (f" Параметр 'msg' не совпадает с ожидаемым: "
                                        f"Expected: '{expected_msg }', Actual: '{actual_msg}'")
