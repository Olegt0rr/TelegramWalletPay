from typing import Literal, Optional

from ._default import DefaultModel
from .order_preview import OrderPreview


class OrderResult(DefaultModel):
    status: Literal[
        "SUCCESS",
        "ALREADY",
        "CONFLICT",
        "ACCESS_DENIED",
        "INVALID_REQUEST",
        "INTERNAL_ERROR",
    ]
    message: Optional[str] = None
    data: Optional[OrderPreview] = None
