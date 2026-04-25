#from telnetlib import EC

import allure
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.login_page import LoginPage
from test_data.users import ADMIN


class BoardsPage(BasePage):
    """Класс для работы со страницей управления досками."""
    BOARDS_H1 = (By.CSS_SELECTOR, '[data-qa="boards-page-title"]')
    BOARDS_CREATE_BUTTON = ("xpath", "//button[@class='btn btn-primary btn-md']")
    BOARDS_TABLES = ("xpath", "//div/div/table/thead/tr/th[text()='Название']")
    BOARDS_COUNT_ROW = ("xpath", "//tbody/tr")
    BOARDS_OPEN = ("xpath", "//tbody/tr/td[7]")
    BOARDS_TO_OPEN = ("xpath", "//a[contains(text(), 'Открыть')]")
    BOARDS_OPEN_NEW_MAIN_NAME = ("xpath", "//h1[@data-qa='board-title']")
    ALL_BOARDS_COUNT = ("xpath", "//h2[@class='admin-section-title']")
    CREATE_BOARD_TITLE_INPUT = ("xpath", "//input[@id='id-input-create-board-title-input']")
    CREATE_BOARD_PUBLIC_CHECKBOX = ("xpath", "//input[@data-qa='create-board-public-checkbox']")
    CREATE_BOARD_SUBMIT_BUTTON = ("xpath", "//button[@data-qa='create-board-submit-button']")
    SEARCH_INPUT = ("xpath", "//input[@id='id-input-boards-search-input']")
    PAGE_NUMBER_LAST = ("xpath", "//button[@class='btn btn-outline btn-sm min-w-[36px]'][last()]")
    DELETE_BOARD = ("xpath", "//button[@data-qa='board-delete-button']")
    DELETE_MODAL_BUTTON = ("xpath", "//button[@data-qa='delete-board-confirm-button']")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/boards'

        super().__init__(driver, self.url)

    @allure.step('Проверка открытия и отображения board страницы')
    def assert_that_boards_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.BOARDS_H1)
        self.assert_element_visible(self.BOARDS_CREATE_BUTTON)
        self.assert_element_visible(self.BOARDS_TABLES)

    @allure.step('Проверка наличия досок у пользователя и отсутcвие')
    def assert_test_user_have_board(self):
        row = self.driver.find_elements(*self.BOARDS_COUNT_ROW)
        count = len(row)
        print(f"Количество строк-досок: {count}")
        assert count > 1, "У пользователя нет досок"

    @allure.step("Получение количество досок на boards")
    def get_boards_count(self):
        boards_element = self.driver.find_element(*self.ALL_BOARDS_COUNT)
        text = boards_element.text  # "Доски (13)"
        number = text.split('(')[1].split(')')[0]  # "13"
        return int(number)

    @allure.step("Обновление страницы boards")
    def refresh_page(self):
        self.driver.refresh()
        self.assert_that_boards_opened()

    @allure.step('Открытие страницы board после авторизации')
    def board_open_logged_in(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(ADMIN)
        time.sleep(1)
        board_page = BoardsPage(driver)
        board_page.open()
        board_page.assert_that_boards_opened()
        return board_page

    @allure.step('Создание новой доски с названием {board_title}')
    def create_board(self, board_title: str, is_public: bool = True): #True - публичная, False - приватная
        self.click(self.BOARDS_CREATE_BUTTON)

        # Вводим название доски
        title_input = self.wait.until(
            EC.visibility_of_element_located(self.CREATE_BOARD_TITLE_INPUT)
        )
        title_input.send_keys(board_title)

        # Если нужно проставить галочку "Публичная доска"
        if is_public:
            checkbox = self.wait.until(
                EC.element_to_be_clickable(self.CREATE_BOARD_PUBLIC_CHECKBOX)
            )
            # Проверяем, не отмечена ли уже галочка
            if not checkbox.is_selected():
                checkbox.click()

        # Нажимаем кнопку "Создать"
        submit_button = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_BOARD_SUBMIT_BUTTON)
        )
        submit_button.click()
        # Ждём закрытия попапа
        time.sleep(1)

    @allure.step('Поиск доски по названию')
    def search_board(self, board_name: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(board_name)
        time.sleep(1)

    @allure.step('Получение списка досок после фильтрации')
    def get_filtered_boards(self):
        return self.driver.find_elements(*self.BOARDS_COUNT_ROW)

    @allure.step('Переход на последнию страницу списка досок')
    def going_to_last_page(self):
        last_page = self.wait.until(
            EC.element_to_be_clickable(self.PAGE_NUMBER_LAST)
        )
        #немного проскроллили
        self.driver.execute_script("arguments[0].scrollIntoView(true);", last_page)
        time.sleep(0.5)
        clickable_page = self.wait.until(EC.element_to_be_clickable(self.PAGE_NUMBER_LAST))
        # Пробуем кликнуть обычным способом, если не получится — JS
        try:
            clickable_page.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", clickable_page)
        time.sleep(0.5)

    @allure.step('Открытие первой доски в списке')
    def open_last_board(self):
        self.going_to_last_page()
        open_board = self.driver.find_elements(*self.BOARDS_TO_OPEN)
        open_board[-1].click()
        time.sleep(0.5)

    @allure.step('Открытие первой доски в списке')
    def delete_board(self):
        self.driver.find_element(*self.DELETE_BOARD).click()
        self.wait.until(EC.element_to_be_clickable(self.DELETE_MODAL_BUTTON)).click()
