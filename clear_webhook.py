from telegram import Bot

BOT_TOKEN = "7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU"  # Replace with your actual bot token
bot = Bot(BOT_TOKEN)
bot.delete_webhook(drop_pending_updates=True)
print("Webhook cleared.")
