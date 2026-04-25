import time

import allure
import pytest

from pages.boards_page import BoardsPage

@allure.step('Проверка, что страница досок открыта')
def test_board_opened(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)
    board_page.assert_that_boards_opened()
@allure.step('Проверка наличия досок у пользователя')
def test__user_has_boards(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)
    board_page.assert_test_user_have_board()
@allure.step('Проверка создания новой доски')
@pytest.mark.my_marker2
def test_create_new_board(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)

    # Получаем количество досок до создания
    initial_count = board_page.get_boards_count()

    # Создаём новую доску
    new_board_title = f"Тестовая доска {int(time.time())}"  # Уникальное название
    board_page.create_board(new_board_title, is_public=True)

    # Обновляем страницу
    board_page.refresh_page()

    # Проверяем, что количество увеличилось
    new_count = board_page.get_boards_count()
    assert new_count == initial_count + 1, \
        f"Количество досок не увеличилось: было {initial_count}, стало {new_count}"


@allure.step('Проверка поиска доски')
def test_search_board(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)

    # Получаем название первой доски из таблицы
    rows_before = board_page.driver.find_elements(*board_page.BOARDS_COUNT_ROW)
    assert len(rows_before) > 0, "Нет досок для теста"

    first_board_name = rows_before[0].text.split('\n')[0] #из всего списка выбираем только первое - название доски

    # Выполняем поиск
    board_page.search_board(first_board_name)

    # Проверяем, что найдена хотя бы одна доска
    rows_after = board_page.get_filtered_boards()
    assert len(rows_after) >= 1, "Доска не найдена после поиска"

    # Проверяем, что найденная доска имеет правильное название
    found_board_name = rows_after[0].text
    assert first_board_name in found_board_name or found_board_name == first_board_name, \
        f"Найдена не та доска: ожидалась '{first_board_name}', получено '{found_board_name}'"

@allure.step('Проверка открытия доски')
def test_open_board(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)

    # Получаем название первой доски
    rows = board_page.driver.find_elements(*board_page.BOARDS_COUNT_ROW)
    assert len(rows) > 0, "Нет досок для проверки"
    first_board_name = rows[0].text.split('\n')[0]

    # Кликаем Открыть по первой доске
    board_for_open = board_page.driver.find_elements(*board_page.BOARDS_OPEN)
    board_for_open[0].click()
    #Запоминаем название открытой доски
    main_board_name = driver.find_element(*board_page.BOARDS_OPEN_NEW_MAIN_NAME).text
    # Проверяем, что URL изменился (содержит /boards/)
    assert "/boards/" in driver.current_url, \
        f"Не удалось открыть доску: текущий URL {driver.current_url}"
    # Проверяем, что открылась именно та доска, которую открывали)
    assert first_board_name == main_board_name, f"Открылась не та доска {main_board_name}"

@allure.step('Проверка удаления доски')
@pytest.mark.my_marker
def test_delete_board(driver):
    board_page = BoardsPage(driver)
    board_page.board_open_logged_in(driver)

    # Получаем количество досок до удаления
    initial_count = board_page.get_boards_count()

    #Открываем последнюю доску и удаляем
    board_page.open_last_board()
    board_page.delete_board()

    # Проверяем, что количество досок уменьшилось
    new_count = board_page.get_boards_count()
    assert new_count == initial_count - 1, \
        f"Количество досок не уменьшилось: было {initial_count}, стало {new_count}"

#
# @allure.step('Проверка фильтрации публичных досок')
# def test_filter_public_boards(driver):
#     """Проверка: фильтр 'Только публичные доски' работает."""
#     board_page = BoardsPage(driver)
#     board_page.board_open_logged_in(driver)
#
#     # Получаем все доски
#     all_boards = board_page.driver.find_elements(*board_page.BOARDS_COUNT_ROW)
#     all_count = len(all_boards)
#
#     # Включаем фильтр публичных досок
#     # board_page.checkbox_only_public_boards.check()
#
#     # Ждём обновления
#     time.sleep(1)
#
#     # Получаем отфильтрованные доски
#     filtered_boards = board_page.driver.find_elements(*board_page.BOARDS_COUNT_ROW)
#     filtered_count = len(filtered_boards)
#
#     # Проверяем, что фильтр работает (количество уменьшилось или осталось)
#     assert filtered_count <= all_count, \
#         f"После фильтрации стало больше досок: было {all_count}, стало {filtered_count}"
#
#
# @allure.step('Проверка количества досок на странице администрирования')
# def test_admin_boards_count(driver):
#     """Проверка: отображение количества досок в админской панели."""
#     board_page = BoardsPage(driver)
#     board_page.board_open_logged_in(driver)
#
#     # Получаем количество из заголовка
#     count = board_page.get_boards_count()
#
#     # Проверяем, что количество - положительное число
#     assert isinstance(count, int), f"Количество не является числом: {count}"
#     assert count >= 0, f"Количество не может быть отрицательным: {count}"
#
#     print(f"📊 Количество досок: {count}")
