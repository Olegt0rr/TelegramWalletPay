from ._default import DefaultModel
from .money_amount import MoneyAmount


class PaymentOption(DefaultModel):
    amount: MoneyAmount
    amount_fee: MoneyAmount
    amount_net: MoneyAmount
    exchange_rate: str
