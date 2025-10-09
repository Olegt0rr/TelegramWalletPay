from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import Field

from telegram_wallet_pay.enums import WebhookMessageType

from ._default import DefaultModel, DefaultRootModel
from .webhook_payload import WebhookPayload

if TYPE_CHECKING:
    from collections.abc import Iterator


class WebhookMessage(DefaultModel):
    event_datetime: datetime = Field(alias="eventDateTime")
    event_id: int
    type: Literal[
        WebhookMessageType.ORDER_PAID,
        WebhookMessageType.ORDER_FAILED,
    ]
    payload: WebhookPayload


class WebhookMessages(DefaultRootModel):
    root: list[WebhookMessage]

    def __iter__(self) -> Iterator[WebhookMessage]:  # type: ignore[override]
        """Iterate over root model."""
        return iter(self.root)
