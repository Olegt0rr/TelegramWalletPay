from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from ._default import DefaultModel
from .money_amount import MoneyAmount


class OrderPreview(DefaultModel):
    id: str
    status: Literal["ACTIVE", "EXPIRED", "PAID", "CANCELLED"]
    number: str
    amount: MoneyAmount
    auto_conversion_currency: Optional[Literal["TON", "BTC", "USDT"]] = None
    created_datetime: datetime = Field(alias="createdDateTime")
    expiration_datetime: datetime = Field(alias="expirationDateTime")
    completed_datetime: Optional[datetime] = Field(None, alias="completedDateTime")
    pay_link: str
    direct_pay_link: str
