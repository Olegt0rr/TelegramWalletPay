import asyncio
import os
from uuid import uuid4

from telegram_wallet_pay import TelegramWalletPay

# use your token from https://pay.wallet.tg/
TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Create order."""
    wallet = TelegramWalletPay(TOKEN)

    # create your first order
    response = await wallet.create_order(
        amount=40,
        currency_code="RUB",
        description="TestPayment",
        external_id=str(uuid4()),
        timeout_seconds=5 * 60,
        customer_telegram_user_id=66812456,
    )

    # let's print creation response
    print("Response:", response)
    print("Order:", response.data)

    # don't forget close API-client instance on your app shutdown
    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())
