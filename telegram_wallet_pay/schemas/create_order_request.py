from typing import Literal, Optional

from pydantic import Field

from telegram_wallet_pay.enums import Currency

from ._default import DefaultModel
from .money_amount import MoneyAmount


class CreateOrderRequest(DefaultModel):
    amount: MoneyAmount
    auto_conversion_currency: Optional[
        Literal[
            Currency.TON,
            Currency.NOT,
            Currency.BTC,
            Currency.USDT,
        ]
    ] = None
    description: str = Field(min_length=5, max_length=100)
    return_url: Optional[str] = Field(None, max_length=255)
    fail_return_url: Optional[str] = Field(None, max_length=255)
    custom_data: Optional[str] = Field(None, max_length=255)
    external_id: str = Field(max_length=255)
    timeout_seconds: int = Field(ge=30, le=864000)
    customer_telegram_user_id: int
