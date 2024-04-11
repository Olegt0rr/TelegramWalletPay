from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from ._default import DefaultModel


class MoneyAmount(DefaultModel):
    currency_code: Literal["TON", "BTC", "USDT", "EUR", "USD", "RUB"]
    amount: str


class OrderNew(DefaultModel):
    amount: MoneyAmount
    auto_conversion_currency: Optional[Literal["TON", "BTC", "USDT"]] = None
    description: str = Field(min_length=5, max_length=100)
    return_url: Optional[str] = Field(None, max_length=255)
    fail_return_url: Optional[str] = Field(None, max_length=255)
    custom_data: Optional[str] = Field(None, max_length=255)
    external_id: str = Field(max_length=255)
    timeout_seconds: int = Field(ge=30, le=864000)
    customer_telegram_user_id: int


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
