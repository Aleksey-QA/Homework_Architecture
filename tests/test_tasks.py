import allure

from pages.tasks_page import TasksPage

@allure.step('Проверка наличия досок у пользователя')
def test_user_have_tasks(driver):
    tasks_page = TasksPage(driver)
    tasks_page.tasks_open_logged_in(driver)
    tasks_page.assert_user_have_tasks()
