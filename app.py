import telebot
import os

# Initialize bot with the token from environment variable
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN_BETA'))

# Handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Get the message_id of the /start message
    start_message_id = message.message_id
    chat_id = message.chat.id  # Chat ID where the message was sent

    # Respond with the message ID information or process as needed
    bot.send_message(chat_id, f"Welcome! Your /start message ID is: {start_message_id}")
@bot.message_handler(commands=['play'])
def handle_start(message):
    # Get the message_id of the /start message
    start_message_id = message.message_id
    chat_id = message.chat.id  # Chat ID where the message was sent

    # Respond with the message ID information or process as needed
    bot.send_message(chat_id, f"Welcome! Your /play message ID is: {start_message_id}")

# Start polling
bot.infinity_polling()
