from __future__ import annotations

from typing import TYPE_CHECKING

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_reconciliation_list import OrderReconciliationList

if TYPE_CHECKING:
    from typing import Literal


class GetOrderReconciliationListResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: str | None = None
    data: OrderReconciliationList | None = None
