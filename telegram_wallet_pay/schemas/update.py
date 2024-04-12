from datetime import datetime
from typing import Iterator, List, Literal

from pydantic import Field

from ._default import DefaultModel, DefaultRootModel
from .webhook_payload import WebhookPayload


class Update(DefaultModel):
    event_datetime: datetime = Field(alias="eventDateTime")
    event_id: int
    type: Literal["ORDER_FAILED", "ORDER_PAID"]
    payload: WebhookPayload


class Updates(DefaultRootModel):
    root: List[Update]

    def __iter__(self) -> Iterator[Update]:  # type: ignore[override]
        """Iterate over root model."""
        return iter(self.root)
