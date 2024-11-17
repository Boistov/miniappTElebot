import telebot

BOT_TOKEN = "7466824505:AAH3FfBXa9lYWsDZhPO1b5wn23NZmR-7e5Y"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, "Welcome! How can I assist you?")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    bot.reply_to(message, "You said: " + message.text)

bot.polling()
