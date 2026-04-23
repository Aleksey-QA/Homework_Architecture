import time

import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from config import BaseConfig

class BasePage:

    HOME_PAGE = "http://localhost:3000/"

    HOST_BUTTON_LOCATOR = ("xpath", "//button[text()='Host']")

    @allure.step('Инициализация страницы')
    def __init__(self, driver, url, timeout=BaseConfig.WEB_DRIVER_WAIT, title='Task Management Board'):
        self.driver: WebDriver = driver
        self.url = url
        self.title = title

        self.wait = WebDriverWait(driver, timeout)

    @allure.step('Открываем страницу')
    def open(self):
        self.driver.get(f"{BaseConfig.ROOT_PATH}{self.url}")

    @allure.step('Дожидаемся отображения элемента по локатору')
    def wait_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el

    @allure.step('Дожидаемся открытия страницы')
    def wait_page_opened(self):
        self.wait.until(EC.url_contains(self.url))

    @allure.step('Кликаем по локатору')
    def click(self, locator, is_force=False):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        if is_force:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)

        else:
            el.click()

    @allure.step('Ввод символов')
    def send_keys(self, locator, value):
        el = self.wait_visible(locator)
        el.send_keys(value)

    @allure.step('Проверка отображения по локатору')
    def assert_element_visible(self, locator):
        el = self.wait_visible(locator)
        assert el.is_displayed(), f"Element '{locator[-1]}' does not found on the page"

    @allure.step('Проверка, что страница открылась по title и URL')
    def assert_that_page_opened(self):
        self.wait_page_opened()

        assert self.url in self.driver.current_url, f"Expected: {self.url}, but {self.driver.current_url}"
        assert self.title == self.driver.title
