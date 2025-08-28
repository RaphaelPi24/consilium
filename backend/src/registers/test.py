import asyncio
from uuid import UUID

import httpx

from registers.base import RegistryApiClientForFile, ApiClient
from registers.schemas import ExternalApiPayload

ID = UUID('2fbca7b1-cb56-499b-b171-7bb09dc58c85')

PAYLOAD_FOR_POST = {
    "object_type": "clinical_record",
    "object_code": None,
    "name": "Тестовая запись пациента Жопникова И.И.",

    "project_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "object_item": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "account_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "user_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",

    "data": {
        "name": "Исследование мозга",
        "created_at": "2022-08-17T18:30:00Z",
        "site": "example.com"
    },
    "meta": {
        "status": "active",
        "flags": 0
    }
}

PAYLOAD_FOR_PUT = {
    "id": "cf9d49bc-8fbf-42f8-ab4b-ba64d9f0c6db",
    "created_date": "2025-08-18T19:07:49.444841+03:00",
    "modified_date": "2025-08-25T19:41:24.760074+03:00",
    "project_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "account_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "user_id": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "object_type": "clinical_record",
    "object_item": "61b3922c-33db-4d38-8f66-4ba5f9dabf6e",
    "object_code": None,
    "name": "Тестовая запись пациента Жопникова И.И.",
    "meta": {
        "flags": 0,

        "internal_id": 93
    },
    "data": {
        "name": "ХАХАХАХ",
        "created_at": "2022-08-17T18:30:00Z",
        "vectorize_at": "2023-08-17T19:30:00Z"
    }
}

PAYLOAD_FOR_PATCH = {

    "data": {
        "name": "ACTIVATION",

    }
}


async def main_get():
    http_client = httpx.AsyncClient()
    api_client = ApiClient(http_client)
    client = RegistryApiClientForFile(api_client)

    data = await client.get(ID)
    print(data)


async def main_post():
    http_client = httpx.AsyncClient()
    api_client = ApiClient(http_client)
    client = RegistryApiClientForFile(api_client)

    payload_dict = PAYLOAD_FOR_POST
    payload_model = ExternalApiPayload(**payload_dict)

    result = await client.create(payload_model)
    print(result)


async def main_delete():
    http_client = httpx.AsyncClient()
    api_client = ApiClient(http_client)
    client = RegistryApiClientForFile(api_client)

    data = await client.delete(ID)
    print(data)


async def main_put():
    http_client = httpx.AsyncClient()
    api_client = ApiClient(http_client)
    client = RegistryApiClientForFile(api_client)

    payload_dict = PAYLOAD_FOR_PUT
    payload_model = ExternalApiPayload(**payload_dict)

    result = await client.update(ID, payload_model)
    print(result)


async def main_modify():
    http_client = httpx.AsyncClient()
    api_client = ApiClient(http_client)
    client = RegistryApiClientForFile(api_client)

    payload_dict = PAYLOAD_FOR_PATCH
    payload_model = ExternalApiPayload(**payload_dict)

    result = await client.modify(ID, payload_model)
    print(result)


# возможно нужен новый ID для всех и в PUT пробрось новый id
if __name__ == "__main__":
    print("--- Запуск GET ---")
    asyncio.run(main_get())
    print("\n--- Запуск POST ---")
    asyncio.run(main_post())
    print("\n--- Запуск PUT ---")
    asyncio.run(main_put())
    print("\n--- Запуск MODIFY ---")
    asyncio.run(main_modify())
    print("\n--- Запуск DELETE ---")
    asyncio.run(main_delete())
    print("\n--- Повторный запуск GET ---")
    asyncio.run(main_get())
