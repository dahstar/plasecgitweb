import os
import telebot
import requests
import PlasecImage  
# Initialize the bot with your token
bot_token = os.getenv('TELEGRAM_BOT_TOKEN_BETA')  # Replace with your bot's token
bot = telebot.TeleBot(bot_token)

# Environment variable for chat ID (replace 'YOUR_CHAT_ID_ENV' with the correct env variable name)
chat_id = os.getenv('TELEGRAM_CHAT_ID', '108704602')  # Default to 108704602 if not set

# Handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        # Get message ID and chat ID
        start_message_id = message.message_id
        chat_id = message.chat.id

        # Debug information
        print(f"Received /start command in chat {chat_id} with message_id {start_message_id}")

        # Respond to the user
        bot.send_message(chat_id, f"Welcome! Your /start message ID is: {start_message_id}")
    except Exception as e:
        print(f"An error occurred in /start handler: {e}")

# Handler for the /play command
@bot.message_handler(commands=['play'])
def handle_play(message):
    try:
        # Get message ID and chat ID
        play_message_id = message.message_id
        chat_id = message.chat.id

        # Debug information
        print(f"Received /plays command in chat {chat_id} with message_id {play_message_id}")

        # Respond to the user
        bot.send_message(chat_id, f"Let’s play! Your /play message ID is: {play_message_id}")
    except Exception as e:
        print(f"An error occurred in /play handler: {e}")

# Function to send a message directly using Telegram API
def send_message_via_api(chat_id, message):
    try:
        # Telegram API URL
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

        # Prepare the data to send
        payload = {
            'chat_id': chat_id,
            'text': message
        }

        # Send the message using POST request
        response = requests.post(url, data=payload)

        # Parse the response from Telegram API
        response_data = response.json()

        if response_data['ok']:
            print(f"Message sent successfully! Message ID: {response_data['result']['message_id']}")
            return response_data['result']['message_id']
        else:
            print("Failed to send message:", response_data)
    except Exception as e:
        print(f"An error occurred while sending message via API: {e}")

# Example: Sending the /start message programmatically
send_message_via_api(chat_id, "/start")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
