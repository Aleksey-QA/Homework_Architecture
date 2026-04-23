import time

import allure
import pytest

from pages.tasks_page import TasksPage
from pages.login_page import LoginPage
from test_data.users import ADMIN

@allure.step('Открытие страницы tasks после авторизации')
def tasks_open_logged_in(driver):  #Метод открытия страницы /board через логин под админом
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)
    time.sleep(1)
    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.assert_that_tasks_opened()
    return tasks_page

@allure.step('Проверка наличия досок у пользователя')
def test_user_have_tasks(driver):
    tasks_page = tasks_open_logged_in(driver)
    tasks_page.assert_user_have_tasks()
