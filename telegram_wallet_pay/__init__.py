__version__ = "0.2.0"
__api_version__ = "1.2.0"
__all__ = ["TelegramWalletPay", "schemas", "errors", "tools"]

from . import errors, schemas, tools
from .client import TelegramWalletPay
