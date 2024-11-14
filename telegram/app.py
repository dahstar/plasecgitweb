import telebot
import os

# Initialize bot with the token from environment variable
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN_BETA'))

# Handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        # Get the message_id of the /start message
        start_message_id = message.message_id
        chat_id = message.chat.id  # Chat ID where the message was sent

        # Print debug information to the console
        print(f"Received /start command in chat {chat_id} with message_id {start_message_id}")

        # Respond to the user
        bot.send_message(chat_id, f"Welcome! Your /start message ID is: {start_message_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Start polling
bot.infinity_polling()
