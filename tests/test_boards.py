import time

import allure
import pytest

from pages.boards_page import BoardsPage
from pages.login_page import LoginPage
from test_data.users import ADMIN

@allure.step('Открытие страницы board после авторизации')
def board_open_logged_in(driver):  #Метод открытия страницы /board через логин под админом
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)
    time.sleep(1)
    board_page = BoardsPage(driver)
    board_page.open()
    board_page.assert_that_boards_opened()
    return board_page

@allure.sub_suite('Проверка наличия досок у пользователя')
@pytest.mark.onlyboard
def test_board_opened(driver):
    board_page = board_open_logged_in(driver)
    board_page.assert_test_user_have_board()






