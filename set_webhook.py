import telebot

BOT_TOKEN = "7466824505:AAH3FfBXa9lYWsDZhPO1b5wn23NZmR-7e5Y"
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your actual ngrok URL or server URL
WEBHOOK_URL = "https://your-ngrok-url.ngrok.io/place-order/"

bot.set_webhook(url=WEBHOOK_URL)
print("Webhook set successfully!")
