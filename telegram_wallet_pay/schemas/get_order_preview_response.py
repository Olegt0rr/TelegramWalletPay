from __future__ import annotations

from typing import Literal

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_preview import OrderPreview


class GetOrderPreviewResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: str | None = None
    data: OrderPreview | None = None
