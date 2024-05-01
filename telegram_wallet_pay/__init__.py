__version__ = "0.5.0"
__api_version__ = "1.2.0"
__all__ = ["TelegramWalletPay", "schemas", "errors", "tools", "enums"]

from . import enums, errors, schemas, tools
from .client import TelegramWalletPay
