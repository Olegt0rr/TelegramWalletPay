import asyncio
import os
from uuid import uuid4

from telegram_wallet_pay import TelegramWalletPay

TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Get started example."""
    wallet = TelegramWalletPay(TOKEN)

    response = await wallet.create_order(
        amount=40,
        currency_code="RUB",
        description="TestPayment",
        external_id=str(uuid4()),
        timeout_seconds=5 * 60,
        customer_telegram_user_id=66812456,
    )

    print("Response:", response)
    print("Order:", response.data)

    response = await wallet.get_preview(response.data.id)
    print("Updated Order Preview:", response.data)

    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())
