from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, '[data-qa="dashboard-create-board-button"]')
    IS_ADMIN = ("xpath", "//div[text()='Администратор']")
    ALL_BOARDS = ("xpath", "//p[text()='Всего досок']")
    ALL_TASKS = ("xpath", "//p[text()='Всего задач']")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/dashboard'
        super().__init__(driver, self.url)

    def assert_that_dashboard_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.CREATE_BOARD_BUTTON)

    def assert_that_information_about_tasks(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.ALL_TASKS)

    def assert_that_information_about_boards(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.ALL_BOARDS)

    def assert_that_user_admin(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.ALL_BOARDS)

