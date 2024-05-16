import asyncio
import logging
import sys
from os import getenv
from uuid import uuid4

# install popular Telegram Bot API framework:
#   pip install aiogram
from aiogram import Bot, Dispatcher, Router, html
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# install Telegram Wallet Pay API client library:
#   pip install telegram-wallet-pay
from telegram_wallet_pay import TelegramWalletPay
from telegram_wallet_pay.enums import ButtonName

# store TELEGRAM_BOT_API_TOKEN to your .env
# bot token can be issued via https://t.me/BotFather
TELEGRAM_BOT_API_TOKEN = getenv("TELEGRAM_BOT_API_TOKEN")

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TELEGRAM_WALLET_PAY_TOKEN = getenv("TELEGRAM_WALLET_PAY_TOKEN")

# message handlers should be attached to the Router, so let's create it
router = Router()


@router.message()
async def message_handler(message: Message, wallet: TelegramWalletPay) -> None:
    """Handle any received message."""
    # prepare answer text
    header = html.bold("Welcome to Telegram Wallet API example")
    body = "Click on the button below to make payment"

    # create an order
    wallet_response = await wallet.create_order(
        amount=4.2,
        currency_code="USD",
        description="Example payment description",
        external_id=str(uuid4()),
        timeout_seconds=5 * 60,
        customer_telegram_user_id=message.from_user.id,
    )
    order = wallet_response.data

    # prepare keyboard
    keyboard = InlineKeyboardBuilder()
    wallet_button = InlineKeyboardButton(
        text=ButtonName.PAY_VIA_WALLET,
        url=order.pay_link,
    )
    keyboard.add(wallet_button)

    # send answer message with prepared content and keyboard markup
    await message.answer(
        text=f"{header}\n{body}",
        reply_markup=keyboard.as_markup(),
        parse_mode=ParseMode.HTML,
    )


async def main() -> None:
    """Set up and run bot application."""
    # create wallet client
    wallet = TelegramWalletPay(TELEGRAM_WALLET_PAY_TOKEN)

    # create dispatcher and pass wallet client to every bot handler
    dp = Dispatcher(wallet=wallet)

    # include router with handlers
    dp.include_router(router)

    # initialize Bot instance
    bot = Bot(TELEGRAM_BOT_API_TOKEN)

    # start polling Telegram Bot API
    try:
        await dp.start_polling(bot)
    finally:  # gracefully close sessions on stop
        await wallet.close()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
