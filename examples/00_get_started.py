import asyncio
import os
from uuid import uuid4

from telegram_wallet_pay import TelegramWalletPay

TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main():
    wallet = TelegramWalletPay(TOKEN)

    result = await wallet.create_order(
        amount=40,
        currency_code="RUB",
        description="TestPayment",
        external_id=str(uuid4()),
        timeout_seconds=5 * 60,
        customer_telegram_user_id=66812456,
    )

    print("Result:", result)
    print("Order:", result.data)

    result = await wallet.get_preview(result.data.id)
    print("Updated Order Preview:", result.data)

    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())
