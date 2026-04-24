import allure

from pages.admin_page import AdminPage
from pages.login_page import LoginPage
from test_data.users import ADMIN, DIANA

@allure.step('Открытие страницы admin после авторизации')
def admin_open_logged_in(driver):  #Метод открытия страницы /admin через логин под админом
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)
    admin_page = AdminPage(driver)
    admin_page.wait_visible(admin_page.ADMIN_PANEL)
    admin_page.driver.find_element(*admin_page.ADMIN_PANEL).click()
    admin_page.assert_that_admin_opened()
    return admin_page

@allure.step('Проверка на отображение Admin страницы')
def test_admin_opened(driver):
    admin_page = admin_open_logged_in(driver)
    admin_page.assert_that_admin_opened()

@allure.step('Проверка на отображение зарегистрированных пользователей')
def test_displaying_registered_users(driver):
    admin_page = admin_open_logged_in(driver)
    admin_page.assert_that_admin_opened()
    admin_page.assert_admin_reg_user()

@allure.step('Проверка входа под админом и поиск юзеров')
def test_admin_find_of_user(driver):
    admin_page = admin_open_logged_in(driver)
    admin_page.assert_that_admin_opened()
    admin_page.assert_admin_find_of_user()

@allure.step('Проверка разлогина и отсутствия доступа к админке у юзеров')
def test_admin_log_out(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    login_page.log_out()
    login_page.login(DIANA)
    admin_page.assert_noadmin_noaccess()
