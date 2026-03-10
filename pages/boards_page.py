import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class BoardsPage(BasePage):
    BOARDS_H1 = (By.CSS_SELECTOR, '[data-qa="boards-page-title"]')
    BOARDS_CREATE_BUTTON = ("xpath", "//button[@class='btn btn-primary btn-md']")
    BOARDS_TABLES = ("xpath", "//div/div/table/thead/tr/th[text()='Название']")
    BOARDS_COUNT_ROW = ("xpath", "//tbody/tr")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/boards'

        super().__init__(driver, self.url)

    @allure.sub_suite('Проверка открытия и отображения board страницы')
    def assert_that_boards_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.BOARDS_H1)
        self.assert_element_visible(self.BOARDS_CREATE_BUTTON)
        self.assert_element_visible(self.BOARDS_TABLES)

    @allure.sub_suite('Проверка наличия досок у пользователя и отсутcвие')
    def assert_test_user_have_board(self):
        row = self.driver.find_elements(*self.BOARDS_COUNT_ROW)
        count = len(row)
        print(f"Количество строк-досок: {count}")
        assert count > 1, "У пользователя нет досок"



