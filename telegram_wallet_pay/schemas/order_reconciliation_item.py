from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from telegram_wallet_pay.enums import Currency, OrderStatus

from ._default import DefaultModel
from .money_amount import MoneyAmount
from .payment_option import PaymentOption


class OrderReconciliationItem(DefaultModel):
    id: int
    status: Literal[
        OrderStatus.ACTIVE,
        OrderStatus.EXPIRED,
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    ]
    amount: MoneyAmount
    auto_conversion_currency: Optional[
        Literal[
            Currency.TON,
            Currency.NOT,
            Currency.BTC,
            Currency.USDT,
        ]
    ] = None
    external_id: str
    customer_telegram_user_id: Optional[int] = None
    created_datetime: datetime = Field(alias="createdDateTime")
    expiration_datetime: datetime = Field(alias="expirationDateTime")
    payment_datetime: Optional[datetime] = Field(None, alias="paymentDateTime")
    selected_payment_option: Optional[PaymentOption] = None
