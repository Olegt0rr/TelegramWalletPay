from datetime import datetime
from typing import Optional

from pydantic import Field

from telegram_wallet_pay.enums import OrderStatus

from ._default import DefaultModel
from .money_amount import MoneyAmount
from .payment_option import PaymentOption


class WebhookPayload(DefaultModel):
    id: int
    number: str
    external_id: str = Field(max_length=255)
    status: Optional[OrderStatus] = None
    custom_data: Optional[str] = Field(None, max_length=255)
    order_amount: MoneyAmount
    selected_payment_option: Optional[PaymentOption] = None
    order_completed_datetime: datetime = Field(alias="orderCompletedDateTime")
