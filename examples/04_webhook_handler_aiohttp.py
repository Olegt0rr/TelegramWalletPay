import os

from aiohttp import web
from telegram_wallet_pay.schemas import WebhookMessages
from telegram_wallet_pay.tools.aiohttp import check_signature

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TELEGRAM_WALLET_PAY_TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


# add `check_signature` decorator to your handler
@check_signature(TELEGRAM_WALLET_PAY_TOKEN)
async def webhook_handler(request: web.Request) -> web.StreamResponse:
    """Handle webhook from Telegram Wallet API."""
    json_data = await request.text()
    webhook_messages = WebhookMessages.model_validate_json(json_data)
    for webhook_message in webhook_messages:
        # process every webhook message as you wish
        # e.g. store them to your database. We just print it here
        print(f"Received webhook message: {webhook_message}")

    return web.json_response({"success": True})


if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/wallet", webhook_handler)
    web.run_app(app)
