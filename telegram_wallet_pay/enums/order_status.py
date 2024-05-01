from enum import Enum


class OrderStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
