import allure
import pytest

from pages.tasks_page import TasksPage

@allure.step('Проверка наличия задач у пользователя')
@pytest.mark.my_marker
def test_user_have_tasks(driver):
    tasks_page = TasksPage(driver)
    tasks_page.tasks_open_logged_in(driver)
    tasks_page.assert_user_have_tasks()
