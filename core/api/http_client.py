import json
import logging

import requests

from core.api.logger import logger

DOMAIN = "http://localhost:8000"


class HttpClient:

    @staticmethod
    def _request(method, path, data=None, params=None, token=None):
        url = f"{DOMAIN}/{path}"
        payload = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        if token:
            headers['Authorization'] = f"Bearer {token}"
            logger.debug(f'{path}:: Authorization = f"Bearer {token}')

        response = requests.request(method, url, headers=headers, data=payload, params=params)

        try:
            response.raise_for_status()
            logger.info(f'{path}:: Запрос успешен.')
            return response
        except requests.exceptions.HTTPError as err:
            return response
            logging.error(f'Ошибка HTTP: {err}')
            assert False, f"Ошибка HTTP: {err}"

    def get(self, path, params=None, token=None):
        return self._request('GET', path, data=None, params=params, token=token)

    def post(self, path, data=None, token=None):
        return self._request('POST', path, data=data, token=token)

    def put(self, path, data=None, token=None):
        return self._request('PUT', path, data=data, token=token)

    def delete(self, path, token=None):
        return self._request('DELETE', path, token=token)

    def patch(self, path, data=None, token=None):
        return self._request('PATCH', path, data=data, token=token)
