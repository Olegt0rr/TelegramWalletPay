from typing import Literal, Optional

from ._default import DefaultModel
from .order_reconciliation_list import OrderReconciliationList


class GetOrderReconciliationListResponse(DefaultModel):
    status: Literal[
        "SUCCESS",
        "INVALID_REQUEST",
        "INTERNAL_ERROR",
    ]
    message: Optional[str] = None
    data: Optional[OrderReconciliationList] = None
