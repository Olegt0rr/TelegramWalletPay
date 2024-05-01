from enum import Enum


class WebhookMessageType(str, Enum):
    ORDER_PAID = "ORDER_PAID"
    ORDER_FAILED = "ORDER_FAILED"
