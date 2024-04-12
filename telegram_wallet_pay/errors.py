class TelegramWalletPayError(Exception):
    """Base TelegramWalletPay exception."""


class InvalidRequestError(TelegramWalletPayError):
    """Invalid request error."""


class InvalidAPIKeyError(TelegramWalletPayError):
    """Invalid API key error."""


class NotFountError(TelegramWalletPayError):
    """Not found error."""


class RequestLimitReachedError(TelegramWalletPayError):
    """Request limit reached error."""


class UnexpectedError(TelegramWalletPayError):
    """Unexpected error."""
