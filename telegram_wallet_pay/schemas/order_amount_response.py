from typing import Literal, Optional

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_amount import OrderAmount


class OrderAmountResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: Optional[str] = None
    data: Optional[OrderAmount] = None
