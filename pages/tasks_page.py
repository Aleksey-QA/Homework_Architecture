import time

import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.login_page import LoginPage
from test_data.users import ADMIN


class TasksPage(BasePage):
    """Класс для работы со страницей задач."""
    TASKS_H1 = (By.CSS_SELECTOR, '[data-qa="tasks-page-title"]')
    TASKS_INPUT_FIND = ("xpath", "//input[@id='id-input-tasks-search-input']")
    TASKS_SELECTED_STATUS = ("xpath", "//select[@id='id-select-tasks-status-filter']")
    TASKS_COUNT_ROW = ("xpath", "//tbody/tr")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/tasks'

        super().__init__(driver, self.url)

    @allure.step('Проверка открытия страницы задач')
    def assert_that_tasks_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.TASKS_H1)
        self.assert_element_visible(self.TASKS_INPUT_FIND)
        self.assert_element_visible(self.TASKS_SELECTED_STATUS)

    @allure.step('Проверка наличия задач у пользователя')
    def assert_user_have_tasks(self):
        row = self.driver.find_elements(*self.TASKS_COUNT_ROW)
        count = len(row)
        print(f"Количество строк-задач: {count}")
        assert count != 1, "У пользователя нет задач"

    @allure.step('Открытие страницы tasks после авторизации')
    def tasks_open_logged_in(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(ADMIN)
        time.sleep(1)
        tasks_page = TasksPage(driver)
        tasks_page.open()
        tasks_page.assert_that_tasks_opened()
        return tasks_page
