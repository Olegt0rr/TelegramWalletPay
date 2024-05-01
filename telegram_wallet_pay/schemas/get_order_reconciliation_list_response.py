from typing import Literal, Optional

from telegram_wallet_pay.enums import RequestStatus

from ._default import DefaultModel
from .order_reconciliation_list import OrderReconciliationList


class GetOrderReconciliationListResponse(DefaultModel):
    status: Literal[
        RequestStatus.SUCCESS,
        RequestStatus.INVALID_REQUEST,
        RequestStatus.INTERNAL_ERROR,
    ]
    message: Optional[str] = None
    data: Optional[OrderReconciliationList] = None
