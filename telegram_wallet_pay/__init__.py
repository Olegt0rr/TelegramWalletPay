__version__ = "0.5.0"
__api_version__ = "1.2.0"
__all__ = ["TelegramWalletPay", "enums", "errors", "schemas", "tools"]

from . import enums, errors, schemas, tools
from .client import TelegramWalletPay
