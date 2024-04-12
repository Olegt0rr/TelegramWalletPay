from typing import Literal, Optional

from ._default import DefaultModel
from .order_amount import OrderAmount


class OrderAmountResult(DefaultModel):
    status: Literal[
        "SUCCESS",
        "INVALID_REQUEST",
        "INTERNAL_ERROR",
    ]
    message: Optional[str] = None
    data: Optional[OrderAmount] = None
