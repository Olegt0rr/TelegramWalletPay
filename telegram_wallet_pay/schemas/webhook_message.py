from datetime import datetime
from typing import Iterator, List, Literal

from pydantic import Field

from ._default import DefaultModel, DefaultRootModel
from .webhook_payload import WebhookPayload


class WebhookMessage(DefaultModel):
    event_datetime: datetime = Field(alias="eventDateTime")
    event_id: int
    type: Literal["ORDER_FAILED", "ORDER_PAID"]
    payload: WebhookPayload


class WebhookMessages(DefaultRootModel):
    root: List[WebhookMessage]

    def __iter__(self) -> Iterator[WebhookMessage]:  # type: ignore[override]
        """Iterate over root model."""
        return iter(self.root)
