from enum import Enum

from telegram_wallet_pay.constants import WALLET_EMOJI


class ButtonName(str, Enum):
    """Enum with available button names.

    The payment button should be named exactly like one of these names.

    Source:
    https://docs.wallet.tg/pay/#section/Design-Guidelines
    """

    WALLET_PAY = f"{WALLET_EMOJI} Wallet Pay"
    PAY_VIA_WALLET = f"{WALLET_EMOJI} Pay via Wallet"
