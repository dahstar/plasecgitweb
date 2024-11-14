import requests

# Your bot token and chat ID
bot_token = '7894875635:AAH7pltCXarg0r2Wib6Sf49QBUBbj0Ky4tc'  # Replace with your bot's token
chat_id = '108704602'  # Replace with the chat ID where the message is sent

# Send the /start message
message = "/start"

# Telegram API URL to send the message
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

# Check if the request was successful
if response_data['ok']:
    # Print the response data (including the message sent by the bot)
    print(f"Message ID: {response_data['result']['message_id']}")
    print(f"Text: {response_data['result']['text']}")
    print(f"Response from Bot: {response_data['result']['text']}")
else:
    print("Failed to send message:", response_data)
