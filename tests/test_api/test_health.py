# from core.api.http_client import HttpClient
#
# # ТАК не делаем
# def test_healthy():
#     response = HttpClient()._request("GET", "health")
#
#     assert response["status"] == "ok"
#     assert response["memory"]["used_mb"]
#     assert response.get("memory", False).get("percent", False)
#     assert response.get("cpu", False).get("percent", False)


