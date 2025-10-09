from __future__ import annotations

from typing import TYPE_CHECKING

from telegram_wallet_pay.enums import Currency

from ._default import DefaultModel

if TYPE_CHECKING:
    from typing import Literal


class MoneyAmount(DefaultModel):
    currency_code: Literal[
        Currency.TON,
        Currency.NOT,
        Currency.BTC,
        Currency.USDT,
        Currency.EUR,
        Currency.USD,
        Currency.RUB,
    ]
    amount: str
