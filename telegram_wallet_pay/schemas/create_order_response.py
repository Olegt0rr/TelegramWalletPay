from __future__ import annotations

from typing import TYPE_CHECKING

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_preview import OrderPreview

if TYPE_CHECKING:
    from typing import Literal


class CreateOrderResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.ALREADY,
        RequestStatus.CONFLICT,
        RequestStatus.ACCESS_DENIED,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: str | None = None
    data: OrderPreview | None = None
