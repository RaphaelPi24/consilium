from datetime import datetime
from typing import TypedDict, NotRequired
from uuid import UUID


class ExternalApiData(TypedDict):
    vectorization_date: NotRequired[datetime]
    source: NotRequired[str]
    link: NotRequired[str]
    status: NotRequired[str]


class ExternalApiMeta(TypedDict):
    status: NotRequired[str]


class ExternalApiPayload(TypedDict):
    object_type: NotRequired[str]
    object_code: NotRequired[str]
    name: NotRequired[str]
    project_id: NotRequired[UUID]
    object_item: NotRequired[UUID]
    account_id: NotRequired[UUID]
    user_id: NotRequired[UUID]
    data: NotRequired[ExternalApiData]
    meta: NotRequired[ExternalApiMeta]
