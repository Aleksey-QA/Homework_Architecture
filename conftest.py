from datetime import datetime

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="chrome", help="the name of the browser")
    parser.addoption(
        "--app",
        default=None,
        help="Path to mobile app file (.apk for Android, .app/.ipa for iOS)",
    )
    parser.addoption(
        "--allure-print",
        action="store_true",
        default=True,
        help="Включить вывод шагов Allure в консоль.",
    )
    parser.addoption(
        "--locale",
        action="store",
        default="en",
        help="Locale to run tests in (e.g. en, ru).",
    )


@pytest.fixture(scope="session")
def locale(pytestconfig):
    return pytestconfig.getoption("--locale")

@pytest.fixture(autouse=False)
def driver(request, pytestconfig):
    browser = pytestconfig.getoption("--br")
    if browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("--width=1980")
        opts.add_argument("--height=1600")
        web_driver = webdriver.Firefox(options=opts)

    else:
        opts = Options()
        # opts.add_argument("--headless=new")
        opts.add_argument("--incognito")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        opts.add_experimental_option("prefs", prefs)

        web_driver = webdriver.Chrome(options=opts)
        web_driver.maximize_window()
        web_driver.implicitly_wait(3)

    yield web_driver
    attach = web_driver.get_screenshot_as_png()
    allure.attach(attach, name=f"Screenshot {datetime.today()}", attachment_type=allure.attachment_type.PNG)
    web_driver.quit()