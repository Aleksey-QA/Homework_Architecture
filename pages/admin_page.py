import time
from selenium.webdriver.support import expected_conditions as EC

import allure
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class AdminPage(BasePage):
    ADMIN_SEL = ("xpath", "//h1[@class ='admin-page-title']")
    ADMIN_PANEL = ("xpath", "//span[text()='Административная панель']")
    ADMIN_FIND_INPUT = ("xpath", "//input[@id='id-input-undefined']")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/admin'
        super().__init__(driver, self.url)
    @allure.step('Проверка открытия страницы')
    def assert_that_admin_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.ADMIN_SEL)
        self.assert_element_visible(self.ADMIN_PANEL)

    @allure.step('Проверка поиска юзеров по name и mail')
    def assert_admin_find_of_user(self):
        self.assert_that_page_opened()
        INPUT_FIND = self.driver.find_element(*self.ADMIN_FIND_INPUT)
        SEND_TEXT = "Example"
        INPUT_FIND.send_keys(SEND_TEXT)
        time.sleep(1)

        # Находим все элементы с классом admin-table-user-name
        user_name_elements = self.driver.find_elements("xpath", "//div[@class='admin-table-user-name']")
        user_mail_elements = self.driver.find_elements("xpath", "//div[@class='admin-table-user-email']")

        # Проверяем, что найдены элементы
        assert len(user_name_elements) > 0, "Не найдены элементы admin-table-user-name"

        # Проверяем КАЖДЫЙ элемент из двух массивов
        if len(user_name_elements) > 0:
            for element, element_2 in zip(user_name_elements, user_mail_elements):
                # Получаем текст и приводим к нижнему регистру
                text = element.text.strip().lower() + element_2.text.strip().lower()
                # Проверяем наличие слова SEND_TEXT
                assert SEND_TEXT.lower() in text, \
                    print(f"Текст '{text}' не содержит искомое слово {SEND_TEXT}. Поиск не работает'")

        print(f"✓ Проверено {len(user_name_elements)} элементов, все содержат {SEND_TEXT}")


    @allure.step('Проверка на недоступность админ.прав для обычных пользователей')
    def assert_noadmin_noaccess(self):
        allure.label('Проверяем, что у обычных пользователей происходит редирект на /dashboard')
        try:
            WebDriverWait(self.driver, 5).until(
                EC.url_matches(".*/dashboard.*")
            )
            print(f"✓ Произошел редирект на: {self.driver.current_url}")

        except TimeoutException:
            current_url = self.driver.current_url
            pytest.fail(f"Редирект не произошел. Текущий URL: {current_url}")

        # или упрощенный вид без ожидания:
        assert self.driver.current_url == "http://localhost:3000/dashboard"

    @allure.step('Проверка на наличие зарегистрированных пользователей')
    def assert_admin_reg_user(self):
        row = self.driver.find_elements("xpath", "//tbody/tr")
        count = len(row)
        print(f"Количество зарегистрированных пользователей: {count}")
        allure.step('Проверка на наличие зарегистрированных пользователей')
        assert count > 1, "Нет зарегистрированных пользователей"
