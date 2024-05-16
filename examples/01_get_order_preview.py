import asyncio
import os

from telegram_wallet_pay import TelegramWalletPay

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Get order preview."""
    # create wallet client instance
    wallet = TelegramWalletPay(TOKEN)

    # get order preview
    response = await wallet.get_order_preview("<your-order-id>")

    # let's print received response
    print("Response:", response)
    print("Order Preview:", response.data)

    # don't forget close API-client instance on your app shutdown
    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())
