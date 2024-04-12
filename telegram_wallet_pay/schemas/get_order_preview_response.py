from typing import Literal, Optional

from ._default import DefaultModel
from .order_preview import OrderPreview


class GetOrderPreviewResponse(DefaultModel):
    status: Literal[
        "SUCCESS",
        "INVALID_REQUEST",
        "INTERNAL_ERROR",
    ]
    message: Optional[str] = None
    data: Optional[OrderPreview] = None
