import allure

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from test_data.users import ADMIN

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



