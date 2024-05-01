from enum import Enum


class Currency(str, Enum):
    TON = "TON"
    BTC = "BTC"
    USDT = "USDT"
    EUR = "EUR"
    USD = "USD"
    RUB = "RUB"
