import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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
        message = (
            "🛒 *Sell Option*\n\n"
            "Sell tokens from your wallet. Choose the token you wish to sell. "
            "Ensure sufficient gas fees are available for the transaction."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "positions":
        message = (
            "📊 *Your Positions*\n\n"
            "Track your active trading positions here. No active positions at the moment."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "limit_orders":
        message = (
            "📈 *Limit Orders*\n\n"
            "Set limit orders to buy or sell tokens at specific prices. "
            "This feature is under development."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "referrals":
        message = (
            "🎉 *Referrals*\n\n"
            "Invite your friends to Trojan on Solana and earn rewards. "
            "Share your referral link to start earning today!"
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "withdraw":
        message = (
            "💸 *Withdraw Funds*\n\n"
            "Withdraw your funds to your external wallet. "
            "Ensure your withdrawal amount exceeds the minimum limit."
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif query.data == "copy_trade":
        message = (
            "🔄 *Copy Trade*\n\n"
            "Copy Trade allows you to copy the buys and sells of any target wallet. \n\n"
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

# Function to run the bot
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot using polling
    application.run_polling()

# Entry point
if __name__ == "__main__":
    run_bot()
