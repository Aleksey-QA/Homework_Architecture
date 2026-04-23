# import pytest
#
# from models.task import UserMeTaskResponse, UserMeTaskListResponse
# from services.authentication_service import AuthServices
# from services.user_service import UserServices
#
#
#
# @pytest.fixture()
# def auth_service():
#     return AuthServices()
#
# @pytest.fixture()
# def user_service():
#     return UserServices()
#
#
# def test_get_my_task(auth_service, user_service):
#     token = auth_service.get_token("diana@example.com", "password123")
#     response: UserMeTaskListResponse = user_service.get_user_task(token=token)
#
#     assert len(response) == 6
#     assert response[0].parent_task_id == 1
