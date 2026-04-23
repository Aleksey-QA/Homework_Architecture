import time

import allure

from pages.boards_page import BoardsPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from test_data.users import ADMIN, DIANA

@allure.sub_suite('Проверка отображения Dashboard страницы')
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
    dashboard_page.assert_that_information_about_boards()
    dashboard_page.assert_that_information_about_tasks()
    dashboard_page.assert_that_user_admin()

@allure.step("Проверка на соответствие досок на Dashboard и Boards")
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

    assert dashboard_count_boards == boards_count, f"Количество досок на //Dashboard {dashboard_count_boards}, а на //Boards {boards_count}"

