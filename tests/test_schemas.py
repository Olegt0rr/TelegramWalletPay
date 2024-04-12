from datetime import datetime
from typing import Any, Dict, List

import pytest
from pydantic import BaseModel, RootModel
from telegram_wallet_pay.schemas import (
    MoneyAmount,
    PaymentOption,
    Update,
    Updates,
    WebhookPayload,
)

money_amount = MoneyAmount(currency_code="RUB", amount="42")
payment_option = PaymentOption(
    amount=money_amount,
    amount_fee=money_amount,
    amount_net=money_amount,
    exchange_rate="",
)
payload = WebhookPayload(
    id=1,
    number="",
    external_id="",
    status="PAID",
    order_amount=money_amount,
    selected_payment_option=payment_option,
    order_completed_datetime=datetime.now(),
)
update = Update(
    event_datetime=datetime.now(),
    event_id=1,
    type="ORDER_PAID",
    payload=payload,
)


@pytest.mark.parametrize(
    ("schema", "data"),
    [
        (Updates, [update.model_dump(by_alias=True)]),
    ],
)
def test_iteration(schema: RootModel, data: List[Dict[str, Any]]) -> None:
    """Test object is iterable."""
    iterable_object = schema.model_validate(data)
    for child in iterable_object:
        assert isinstance(child, (RootModel, BaseModel))
