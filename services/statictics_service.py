import allure

from core.api.http_client import HttpClient

@allure.sub_suite('Тестирование API Statistics')
class StaticServices:

    def __init__(self):
        self.http_client = HttpClient()

    def get_dashboard_status(self, token):
        return self.http_client.get("stats/dashboard", None, token)


    def get_global_task_stats(self, token):
        return self.http_client.get("stats/tasks", None, token)

    def get_user_activity(self, token, user_id):
        return self.http_client.get(f"stats/users/{user_id}/activity", None, token)

    def get_all_boards_admin(self, params= None, token=None):
        return self.http_client.get(f"stats/admin/all-boards", params={'skip': params["skip"], 'limit': params["limit"], 'archived': params["archived"]}, token= token)


    def get_all_tasks_admin(self, params=None, token=None):
        return self.http_client.get(f"stats/admin/all-tasks", params={'skip': params["skip"], 'limit': params["limit"], 'status_filter': params["status"], 'priority_filter': params["priority"]}, token=token)