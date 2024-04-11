from datetime import datetime
from typing import Literal

from pydantic import Field, RootModel

from ._default import DefaultModel
from .webhook_payload import WebhookPayload


class Update(DefaultModel):
    event_datetime: datetime = Field(alias="eventDateTime")
    event_id: int
    type: Literal["ORDER_FAILED", "ORDER_PAID"]
    payload: WebhookPayload


Updates = RootModel(list[Update])
