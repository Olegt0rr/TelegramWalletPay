from typing import Literal

from ._default import DefaultModel


class MoneyAmount(DefaultModel):
    currency_code: Literal["TON", "BTC", "USDT", "EUR", "USD", "RUB"]
    amount: str
