import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for bot token and other configurations
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in your Render environment
ADMIN_ID = int(os.getenv("ADMIN_ID", "5698476270"))  # Replace with your admin user ID or set via Render
PORT = int(os.getenv("PORT", 8443))  # Render automatically sets this
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Provided by Render

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
            await query.edit_message_text(admin_message, reply_markup=main_menu_keyboard())
        else:
            logger.warning(f"Unauthorized admin page access attempt by user ID {user_id}.")
            await query.answer("You are not authorized to access this page!", show_alert=True)
            return
    elif query.data == "back_to_main":
        await query.edit_message_text("Returning to main menu...", reply_markup=main_menu_keyboard())
    elif query.data == "buy":
        await query.edit_message_text("Buy option selected!", reply_markup=main_menu_keyboard())
    else:
        await query.edit_message_text("Feature not implemented yet.", reply_markup=main_menu_keyboard())

# Set up the bot application
def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set!")

    application = Application.builder().token(BOT_TOKEN).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot using webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"https://{HOSTNAME}/{BOT_TOKEN}"
    )

# Entry point
if __name__ == "__main__":
    run_bot()
