from typing import Literal

from telegram_wallet_pay.enums import Currency

from ._default import DefaultModel


class MoneyAmount(DefaultModel):
    currency_code: Literal[
        Currency.TON,
        Currency.BTC,
        Currency.USDT,
        Currency.EUR,
        Currency.USD,
        Currency.RUB,
    ]
    amount: str
