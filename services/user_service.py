from core.api.http_client import HttpClient
from models.task import UserMeTaskListResponse


class UserServices:
    """Сервис для работы с пользователями."""
    def __init__(self):
        self.http_client = HttpClient()

    def get_user_task(self, skip=0, limit=100, token=None) -> UserMeTaskListResponse:
        """Получает список задач текущего пользователя."""
        response = self.http_client.get("users/me/tasks",
                                        params={'skip': skip, 'limit': limit}, token=token)

        model = UserMeTaskListResponse(**response)
        return model
