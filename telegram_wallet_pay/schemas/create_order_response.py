from typing import Literal, Optional

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_preview import OrderPreview


class CreateOrderResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.ALREADY,
        RequestStatus.CONFLICT,
        RequestStatus.ACCESS_DENIED,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: Optional[str] = None
    data: Optional[OrderPreview] = None
