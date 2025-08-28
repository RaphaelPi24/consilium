import logging
from typing import Self
from uuid import UUID

import httpx
from httpx import Response

from config import PROJECT_ID
from registers.schemas import ExternalApiPayload, ExternalApiData, ExternalApiMeta

logger = logging.getLogger(__name__)


class ApiClient:
    VALID_METHODS = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH'}

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def _prepare_request(self, method: str, url: str, data: ExternalApiPayload = None):
        if method.upper() not in self.VALID_METHODS:
            raise ValueError(f"Неподдерживаемый HTTP метод: {method}")

        if not isinstance(url, str) and not url:
            raise ValueError("URL должен быть STR и не может быть пустым")

        if method in ("POST", "PUT", "PATCH") and (data is None or len(data) == 0):
            raise ValueError(f"json_data is None(empty) = {data}")

            # json_data = data.model_dump(mode='json') if data else None  # typedDict
        json_data = data
        # try:
        #     json_data = json.dumps(data)
        # except TypeError as e:
        #     logger.error(f"Данные не могут быть сериализованы в JSON: {e}")

        kwargs = {'url': url}
        if json_data and method.lower() not in ['get', 'delete']:
            kwargs['json'] = json_data
        http_method = getattr(self._client, method.lower())
        return http_method, kwargs

    async def _request_execution(self, http_method, kwargs):
        try:
            return await http_method(**kwargs)  # retry, exponential backoff
        except httpx.ConnectError as e:
            logger.error(f'ошибка ConnectError: {e}')
        except httpx.ConnectTimeout as e:
            logger.error(f'Ошибка ConnectTimeout: {e}')
        except httpx.RequestError as e:
            logger.error(f'Ошибка RequestError: {e}')
        except Exception as e:
            logger.error(f'Ошибка Exception: {e}')

    def _raise_for_status(self, response):
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f'HTTPError: {e}')
            raise e

    async def request(self, method: str, url: str, data: ExternalApiPayload = None):
        http_method, kwargs = await self._prepare_request(method, url, data)
        response = await self._request_execution(http_method, kwargs)
        self._raise_for_status(response)
        return response.json()

    async def close(self):
        await self._client.aclose()


class RegistryApiClientForFile:
    URL = f"https://files.reg.skroy.ru/api/file/"

    def __init__(self, api_client: ApiClient):
        self.client = api_client

    @retry(...)
    async def create(self, data: ExternalApiPayload) -> Response:
        return await self.client.request('POST', self.URL, data=data)

    async def get(self, id: UUID):
        return await self._send_request('GET', id)

    async def update(self, id: UUID, data: ExternalApiPayload) -> Response:
        return await self._send_request('PUT', id, data=data)

    async def modify(self, id: UUID, data) -> Response:
        return await self._send_request('PATCH', id, data=data)

    async def delete(self, id: UUID):
        return await self._send_request('DELETE', id)

    async def _send_request(self, method, id, data=None) -> Response:
        url_with_id = self.get_url_with_id(id)
        return await self.client.request(method, url_with_id, data=data)

    def get_url_with_id(self, id) -> str:
        return f'{self.URL}/{id}/'


class FullPrepareData:
    def __init__(self, object_code, name, object_type, _data, _meta):
        data = ExternalApiPayload()

        data.object_code = object_code
        data.name = name
        data.object_type = object_type

        data.project_id = PROJECT_ID  # да, дублирование, так нужно
        data.object_item = PROJECT_ID
        data.account_id = PROJECT_ID
        data.user_id = PROJECT_ID

        data.data = _data
        data.meta = _meta

        self.data = data

    @classmethod
    def from_abc(cls, name, vectorization_date, source, link, status, object_code=None,
                 object_type="Онкологические данные") -> Self:
        small_data = ExternalApiData(vectorization_date=vectorization_date, source=source, link=link, status=status)
        meta_data = ExternalApiMeta()
        _data = ExternalApiPayload(object_code=object_code, name=name, object_type=object_type, data=small_data,
                                   meta=meta_data)
        return _data
