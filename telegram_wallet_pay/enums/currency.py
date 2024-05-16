from enum import Enum


class Currency(str, Enum):
    TON = "TON"
    NOT = "NOT"
    BTC = "BTC"
    USDT = "USDT"
    EUR = "EUR"
    USD = "USD"
    RUB = "RUB"
