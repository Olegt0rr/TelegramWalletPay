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
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# install Telegram Wallet Pay API client library:
#   pip install telegram-wallet-pay
from telegram_wallet_pay import TelegramWalletPay
from telegram_wallet_pay.enums import ButtonName, WebhookMessageType
from telegram_wallet_pay.schemas import WebhookMessage, WebhookMessages
from telegram_wallet_pay.tools.aiohttp import check_signature

# store TELEGRAM_BOT_API_TOKEN to your .env
# bot token can be issued via https://t.me/BotFather
TELEGRAM_BOT_API_TOKEN = getenv("TELEGRAM_BOT_API_TOKEN")

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TELEGRAM_WALLET_PAY_TOKEN = getenv("TELEGRAM_WALLET_PAY_TOKEN")

# Set your server domain name (do not forget to set up SSL)
WEBHOOK_HOST = getenv("WEBHOOK_HOST", "https://example.com")

# Set up paths for webhooks
TELEGRAM_BOT_WEBHOOK_PATH = getenv("TELEGRAM_BOT_WEBHOOK_PATH", "/bot")
TELEGRAM_WALLET_WEBHOOK_PATH = getenv("TELEGRAM_WALLET_WEBHOOK_PATH", "/wallet")

# Create bot handlers router
router = Router()


# Prepare message handler
@router.message()
async def message_handler(message: Message, wallet: TelegramWalletPay) -> None:
    """Handle any received message."""
    # prepare answer text
    header = html.bold("Welcome to Telegram Wallet API example")
    body = "Click on the button below to make payment"

    # create an order
    user = message.from_user
    wallet_response = await wallet.create_order(
        amount=4.2,
        currency_code="EUR",
        description="Example payment description",
        external_id=str(uuid4()),
        timeout_seconds=24 * 60 * 60,  # 1 day
        customer_telegram_user_id=user.id,
        custom_data=str(user.id),
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


# Add set webhook on bot startup function
async def on_bot_startup(bot: Bot) -> None:
    """Set up bot before start up."""
    await bot.set_webhook(f"{WEBHOOK_HOST}{TELEGRAM_BOT_WEBHOOK_PATH}")


# Prepare wallet webhook handler
@check_signature(TELEGRAM_WALLET_PAY_TOKEN)
async def wallet_webhook_handler(request: web.Request) -> web.StreamResponse:
    """Handle webhook from Telegram Wallet API."""
    bot: Bot = request.app["bot"]

    json_data = await request.text()
    webhook_messages = WebhookMessages.model_validate_json(json_data)

    for webhook_message in webhook_messages:
        await _process_payment(webhook_message, bot)

    return web.json_response({"success": True})


async def _process_payment(webhook_message: WebhookMessage, bot: Bot) -> None:
    """Process payment."""
    order = webhook_message.payload
    user_id = int(order.custom_data)

    if webhook_message.type == WebhookMessageType.ORDER_PAID:
        text = "Thanks, order has been paid"
    else:
        text = f"Order status was changed to {order.status}"

    await bot.send_message(chat_id=user_id, text=text)


def main() -> None:
    """Set up and run bot application."""
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_bot_startup)

    # Create bot instance
    bot = Bot()

    # Create wallet client
    wallet = TelegramWalletPay(TELEGRAM_WALLET_PAY_TOKEN)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Pass bot instance to the application to make it available in aiohttp handlers
    app["bot"] = bot

    # Register Telegram Bot API webhook handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        wallet=wallet,  # pass wallet here to make it available in bot handlers
    )
    webhook_requests_handler.register(app, path=TELEGRAM_BOT_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Register Wallet Pay API webhook handler
    app.router.add_post(TELEGRAM_WALLET_WEBHOOK_PATH, wallet_webhook_handler)

    # And finally start webserver
    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
