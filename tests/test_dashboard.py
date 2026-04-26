import time

import allure

from pages.boards_page import BoardsPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from test_data.users import ADMIN, DIANA

@allure.step('Проверка отображения Dashboard страницы')
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
    dashboard_page.assert_that_information_about_boards()
    dashboard_page.assert_that_information_about_tasks()
    dashboard_page.assert_that_user_admin()

@allure.step("Проверка на соответствие количества досок на Dashboard и Boards")
def test_count_boards_on_dashboard_board(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(DIANA)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
    dashboard_count_boards = dashboard_page.get_boards_count()

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_that_boards_opened()
    boards_count = boards_page.get_boards_count()

    assert dashboard_count_boards == boards_count, \
        f"Количество досок на //Dashboard {dashboard_count_boards}, а на //Boards {boards_count}"

@allure.step('Проверка создания новой доски через dashboard')
def test_create_new_board_dashboard(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    # Получаем количество досок до создания
    initial_count = dashboard_page.get_boards_count()

    # Создаём новую доску
    dashboard_page.create_board_from_dashboard()

    # Обновляем страницу
    dashboard_page.refresh_page()

    # Проверяем, что количество увеличилось
    new_count = dashboard_page.get_boards_count()
    assert new_count == initial_count + 1, \
        f"Количество досок не увеличилось: было {initial_count}, стало {new_count}"
@allure.step('Проверка отображения последних 6 досок')
def test_dashboard_shows_last_6_boards(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(DIANA)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_that_boards_opened()
    # открываем 7 досок
    boards_page.open_n_board(7)

    dashboard_page.open()
    dashboard_page.assert_that_dashboard_opened()
    # Считаем кол-во карточек последних открытых досок
    cards = dashboard_page.get_board_cards()
    assert len(cards) <= 6, f"Отображается {len(cards)} досок, ожидается не более 6"

@allure.step('Проверка отображения последних 6 досок для ADMIN')
def test_dashboard_shows_last_6_boards_for_admin(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_that_boards_opened()
    # открываем n досок
    n = 7
    boards_page.open_n_board(n)

    dashboard_page.open()
    dashboard_page.assert_that_dashboard_opened()
    # Считаем кол-во карточек последних открытых досок
    cards = dashboard_page.get_board_cards()
    assert len(cards) == 6, f"Отображается {len(cards)} досок из {n}, ожидается 6"

@allure.step('Проверка содержимого карточки доски (название, описание, дата, бейдж)')
def test_board_card_details(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(DIANA)
    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_that_boards_opened()
    # открываем 3 доски
    n = 3
    boards_page.open_n_board(n)

    dashboard_page.open()
    dashboard_page.assert_that_dashboard_opened()
    dashboard_page.assert_filling_of_cards(n)
@allure.step('Проверка перехода к доске по клику на карточку')
def test_click_board_card_navigates_to_board(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)
    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_that_boards_opened()
    # открываем 2 доски, чтобы они появились как последние открытые
    n = 3
    boards_page.open_n_board(n)

    dashboard_page.open()
    dashboard_page.assert_that_dashboard_opened()
    cards = dashboard_page.get_board_cards()
    assert len(cards) > 0, "Нет досок для проверки"

    # Берём название первой доски до клика и кликаем по карточке
    board_title = dashboard_page.get_board_card_title(cards[0])
    cards[0].click()
    # Проверяем, что URL изменился
    assert "/boards/" in driver.current_url, "Не выполнен переход на страницу доски"
    # Проверяем  заголовок доски на открывшейся странице
    opened_title = boards_page.wait_visible(boards_page.BOARDS_OPEN_NEW_MAIN_NAME).text
    assert opened_title == board_title, (f"Открылась не та доска: "
                                         f"ожидалась '{board_title}', получено '{opened_title}'")
@allure.step('Проверка наличия кнопки создания доски и открытия модального окна')
def test_create_board_button_opens_modal(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

    # Нажимаем кнопку "Создать доску"
    create_btn = dashboard_page.wait_visible(dashboard_page.CREATE_BOARD_BUTTON)
    create_btn.click()
    # Проверяем, что модальное окно появилось
    assert dashboard_page.is_create_modal_visible(), "Модальное окно создания доски не появилось"
    # закрываем модальное окно через Отмена
    dashboard_page.wait_visible(dashboard_page.CREATE_BOARD_MODAL_CANCEL).click()
    assert dashboard_page.is_create_modal_visible() is False, "Модальное окно не закрылось"

@allure.step('Проверка пустого состояния, если у пользователя нет недавно открытых досок')
# @pytest.mark.my_marker
def test_empty_state_when_no_boards(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
    time.sleep(3)
    dashboard_page.assert_empty_state_when_no_boards()
