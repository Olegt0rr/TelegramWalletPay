from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from telegram_wallet_pay.enums import Currency, OrderStatus

from ._default import DefaultModel
from .money_amount import MoneyAmount


class OrderPreview(DefaultModel):
    id: str
    status: Literal[
        OrderStatus.ACTIVE,
        OrderStatus.EXPIRED,
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    ]
    number: str
    amount: MoneyAmount
    auto_conversion_currency: Optional[
        Literal[
            Currency.TON,
            Currency.NOT,
            Currency.BTC,
            Currency.USDT,
        ]
    ] = None
    created_datetime: datetime = Field(alias="createdDateTime")
    expiration_datetime: datetime = Field(alias="expirationDateTime")
    completed_datetime: datetime | None = Field(None, alias="completedDateTime")
    pay_link: str
    direct_pay_link: str
