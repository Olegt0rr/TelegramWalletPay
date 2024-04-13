import asyncio
import os

from telegram_wallet_pay import TelegramWalletPay

TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Get order preview."""
    wallet = TelegramWalletPay(TOKEN)

    response = await wallet.get_order_preview("<your-order-id>")

    print("Response:", response)
    print("Order Preview:", response.data)

    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())
