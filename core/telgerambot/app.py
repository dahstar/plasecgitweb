#modifeid ai and chatgpt with my inputs
import os
import sqlite3
import telebot
from telebot.types import ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
from plasec import Plasec
user_id=0
plasec_instance =None
token=""
import time
import requests
from requests.exceptions import ConnectionError

def find_user_id(username):
    try:
        user_info = bot.get_chat(username)
        print("us",user_info,username)
        return user_info.id  # Get the user ID from the chat info
    except Exception as e:
        print(f"Error finding user ID for {username}: {str(e)}")
        return None
def check_user_in_db(user_id):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    
    # Check if the user ID exists in the chat_history table
    cursor.execute('SELECT COUNT(*) FROM chat_history WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] > 0
def send_message_to_user(username, message):
    user_id = find_user_id(username)
    
    if user_id is not None:
        if check_user_in_db(user_id):
            try:
                # Send message to user
                bot.send_message(user_id, message)
                
                # Add 50 credits to the user
                update_user_credits(user_id, 50)
                bot.send_message(user_id, "You've been rewarded with 50 credits.")
                
            except Exception as e:
                print(f"Error sending message to {username}: {str(e)}")
        else:
            # Send a request for the user to login in @plasec
            bot.send_message(user_id, "Please log in at @plasec to access more features.")
    else:
        print("User not found or bot has not had interaction with the user.")

 
def check_user_in_db(user_id):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    
    # Check if the user ID exists in the chat_history table
    cursor.execute('SELECT COUNT(*) FROM chat_history WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] > 0  # Return True if the user exists, False otherwise
def make_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            return response
        except ConnectionError as e:
            print(f"Connection error: {e}, retrying... ({attempt + 1}/{max_retries})")
            time.sleep(2)  # Wait before retrying
    raise ConnectionError("Max retries reached")
#https://www.google.com/search?q=token+generator+python&oq=token+generator+pyth&gs_lcrp=EgZjaHJvbWUqBwgBEAAYgAQyBggAEEUYOTIHCAEQABiABDIICAIQABgWGB4yCAgDEAAYFhgeMggIBBAAGBYYHjIICAUQABgWGB4yCggGEAAYDxgWGB4yDAgHEAAYChgPGBYYHjINCAgQABiGAxiABBiKBTIKCAkQABiABBiiBNIBCTEwNTI2ajBqN6gCCLACAQ&sourceid=chrome&ie=UTF-8
#gemeni
 
user_modes = {}
user_search_results = {}

 
 

# Initialize Telegram bot with your API Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot.set_webhook()
allscore=0
# Function to initialize the SQLite database
def get_last_id():
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()

    # Fetch the last id from the chat_history table
    cursor.execute('SELECT MAX(id) FROM chat_history')
    result = cursor.fetchone()

    conn.close()

    # If no records are found, start from 0
    return result[0] if result[0] is not None else 0
def initialize_db():
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        message TEXT NOT NULL,
                        response TEXT NOT NULL,
                        type TEXT DEFAULT 'default_type',
                        system TEXT DEFAULT 'default_system',
                        user_id INTEGER NOT NULL DEFAULT 0,
                        chat_id TEXT DEFAULT 0,
                        token TEXT DEFAULT '0'
                      )''')
    # Create a table to store user profiles (if it doesn't exist)
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
                        user_id INTEGER PRIMARY KEY,
                        credits INTEGER DEFAULT 0
                      )''')
    conn.commit()
    conn.close()
@bot.message_handler(commands=['register'])
def handle_register(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Print user information to the console
    print(f"User ID: {user_id}")
    print(f"Username: {username}")

    # Send a welcome message to the user
    welcome_message = f"Hello, @{username}! Your User ID is {user_id}."
    bot.reply_to(message, welcome_message)
def get_or_create_user_profile(user_id):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute('SELECT credits FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    # If user does not exist, create a profile with 0 credits
    if result is None:
        cursor.execute('INSERT INTO user_profiles (user_id, credits) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        result = (0,)  # Default credits if the user is new

    conn.close()
    return result[0]  # Return the user's current credits

# Function to update user credits
def update_user_credits(user_id, credits_to_add):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()

    # Update the credits for the user
    cursor.execute('UPDATE user_profiles SET credits = credits + ? WHERE user_id = ?', (credits_to_add, user_id))
    conn.commit()
    conn.close()
def show_message_with_credits_button(chat_id, message_text, user_id, credits_added=None):
    markup = InlineKeyboardMarkup()

    # Custom message with optional credits added text
    if credits_added is not None:
        message_text += f" {credits_added} credits added."

    # Button to show full credits
    credits_button = InlineKeyboardButton(message_text, callback_data='get_credits')
    markup.add(credits_button)

    
# Function to retrieve user credits
def get_user_credits(user_id):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()
    cursor.execute('SELECT credits FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0
# Function to retrieve user credits
def get_message_token(chat_id):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token FROM chat_history WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
# Function to store a message in the database
def store_message(message, response, default_type='default_type', default_system='default_system', user_id=0, chat_id=0, token="0"):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    
    # Fetch the last id and increment it
    last_id = get_last_id()
    new_id = last_id + 1
    
    # Insert the message, response, chat_id, and other fields into the table
    cursor.execute('INSERT INTO chat_history (id, message, response, type, system, user_id, chat_id, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                   (new_id, message, response, default_type, default_system, user_id, chat_id, token))
    
    conn.commit()
    conn.close()

# Function to retrieve the chat history for a user
def get_chat_history(user_id):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, response FROM chat_history WHERE user_id = ?', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

# Function to search history based on a partial input
def search_history(user_id, search_term):
    search_term=search_term.replace("/search","").strip()
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, response,token FROM chat_history WHERE user_id = ? AND message LIKE ?', 
                   (user_id, f'%{search_term}%'))
    results = cursor.fetchall()
    conn.close()
    print(f"Search term: '{search_term}', Found {len(results)} results")
    return results
def show_line_menu(chat_id,message='💲 Credits', callback_data='get_credits'):
 credits_button = InlineKeyboardButton(message, callback_data)
 markup.row(exit_button)
# Function to show a colorful menu

def show_colorful_menu(chat_id,message="Please choose an option:",crmessage="💲 Credits"):
    markup = InlineKeyboardMarkup()

    # Create colorful buttons using emojis
    start_chat_button = InlineKeyboardButton('🌟 /chat message]', callback_data='start_chat')
    search_button = InlineKeyboardButton('🔍 /search [searchterm]', callback_data='search')
    register_button = InlineKeyboardButton('🆘 /register', callback_data='handle_register')
    help_button = InlineKeyboardButton('🆘 Help', callback_data='help')
    credits_button = InlineKeyboardButton(crmessage, callback_data='get_credits')
    exit_button = InlineKeyboardButton('❌ /Exit', callback_data='exit')
    if crmessage=="💲 Credits":
     # Add buttons to the markup
     markup.row(start_chat_button, search_button)
     markup.row(help_button, credits_button)
     markup.row(register_button,exit_button)
    else:
        markup.row( credits_button)
    # Send the message with the colorful menu
    s="dawood"
    if type(s)!=type(message):
     message=message.content_type
    bot.send_message(chat_id, message, reply_markup=markup)
# Handle the button press via callback data
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    if call.data == "start_chat":
        bot.send_message(call.message.chat.id, "Starting chat... How can I assist you today?")
    elif call.data == "search":
        bot.send_message(call.message.chat.id, "Please start typing to search.")
    elif call.data=="get_search":
      
        user_modes[call.from_user.id] = "search"  # Switch to search mode
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "Help Menu: Choose an option to start a chat or search for information.")
    elif call.data == "get_credits":
        user_id = call.from_user.id
        bot.send_message(call.message.chat.id, f"all credits:{get_user_credits(user_id)}")

    elif call.data == "exit":
        bot.send_message(call.message.chat.id, "Goodbye!")
# Function to interact with Cohere for training examples

def chatwithllm(message, topic='default_topic', system='default_system'):
    """
    Run the plasec.py script with the given arguments and system prompt.
    """
    try:
        

        # Run plasec.py with the message, topic, and system prompt
        result = subprocess.run(
            ['python3', 'plasec.py', message, topic, system],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()  # Return the output from the script
    except Exception as e:
        print(f"Error running script: {str(e)}")
        return f"Error running script: {str(e)}"
# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to plasec!")
    show_colorful_menu(message.chat.id,"Hello, welcome to plasec!")

# Function to show search results in a numbered format with truncated messages (up to 100 characters)
def display_search_results(chat_id, results):
    result_text = "Search results:\n"
    t=[""]*20
    count=0
    for idx, (msg, resp,token) in enumerate(results[:10], 1):  # Show only top 10 results
        truncated_msg = msg[:200]  # Truncate to 100 characters
        result_text += f"{idx}. {truncated_msg}... (type {idx} to view full message)\n"
        t[idx]=token
        
        if count==0:
         show_colorful_menu(chat_id, f"{resp}", f"{token}")
        count+=1
    if count>1:
        bot.send_message(chat_id, result_text)
          
    else:
    
          bot.send_message(chat_id, "no other result-type /chat for new result")

    #bot.send_message(chat_id, "Please choose an option:")
    return results,token
def handle_chat(message):
   
    user_message = message.text.replace("/chat ", "").strip()
    user_id = message.from_user.id
    if user_message:
        # Create a Plasec instance
        plasec_instance = Plasec(chat=user_message, topic="general", system="telegram")
        chat_id = message.chat.id  # Retrieve the chat_id

        # Store the message, response, and chat_id in the database
        store_message(user_message, plasec_instance.answer, 'chat', 'plasec', user_id, chat_id, plasec_instance.token)

        # Update user credits
        update_user_credits(user_id, 1)

        # Show response and menu
        show_message_with_credits_button(message.chat.id, f"Plasec Response: {plasec_instance.answer}", user_id, credits_added=10)
        show_colorful_menu(message.chat.id, f"{plasec_instance.answer}", f"{plasec_instance.token}+plasec_instance.count$c")


def real_time_search(message, user_id, task_type='search'):
    search_term = message.text.strip().replace("/chat ", "")  # Extract the search term from the message

    # Perform a search based on the term
    results = search_history(user_id, search_term)

    if results:
        # If search results are found, display them and let the user choose
        user_search_results[user_id] = results
       
        result,token=display_search_results(message.chat.id, results)

        # Auto-select the first result or let the user pick
        
        bot.register_next_step_handler(message, handle_search_selection, user_id)
    else:
        # If no results are found, fall back to chat
        bot.send_message(message.chat.id, "waiting for chat...")
        handle_chat(message, user_id)
def get_message_token(message,response):
  
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    
    # Use both chat_id and user_id to filter the result
    cursor.execute('SELECT token FROM chat_history WHERE message = ? AND response = ?', (message, response))
    result = cursor.fetchone()
    
    conn.close()
    
    return result[0] if result else "0"  # Return 0 if no result is found
def handle_search_selection(message, user_id):
    try:
        selected_idx = int(message.text.strip()) - 1
        chat_id=0
        # Retrieve the corresponding full message from the stored search results
        if user_id in user_search_results and 0 <= selected_idx < len(user_search_results[user_id]):
            full_msg, full_resp,token = user_search_results[user_id][selected_idx]
            
            # Combine message and response
            combined_message = f"Full Message: {full_msg}\nResponse: {full_resp}"
            chat_id = message.chat.id  # Get the chat_id
            # Check if the combined message exceeds 4096 characters
            if len(combined_message) > 4096:
                # If more than 4096 characters, split into chunks
                for chunk in [combined_message[i:i + 4096] for i in range(0, len(combined_message), 4096)]:
                   # bot.send_message(message.chat.id, chunk)
                    token = get_message_token(message,full_resp)
                    print("tcid",chat_id)
                    show_colorful_menu(message.chat.id, f"{chunk}", f"{token}+10$")
            else:
                # If less than 4096 characters, send the whole message
                #bot.send_message(message.chat.id, combined_message)
                
                print("tc",token)
                show_colorful_menu(message.chat.id, f"{combined_message}", f"{token}+10$")

            # Update credits for selecting a search result
            update_user_credits(user_id, 20)

        else:
            bot.send_message(message.chat.id, "Invalid selection. Picking the first result.")
            
            full_msg, full_resp,token = user_search_results[user_id][0]
            combined_message = f"Full Message: {full_msg}\nResponse: {full_resp}"

            if len(combined_message) > 4096:
                # Split if too long
                for chunk in [combined_message[i:i + 4096] for i in range(0, len(combined_message), 4096)]:
                    bot.send_message(message.chat.id, chunk)
            else:
                bot.send_message(message.chat.id, combined_message)
                
            update_user_credits(user_id, 20)
            show_message_with_credits_button(message.chat.id, "First result selected.", user_id, credits_added=20)
 
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input. Picking the first result.")
        
        full_msg, full_resp,token = user_search_results[user_id][0]
        combined_message = f"Full Message: {full_msg}\nResponse: {full_resp}"

        if len(combined_message) > 4096:
            # Split if too long
            for chunk in [combined_message[i:i + 4096] for i in range(0, len(combined_message), 4096)]:
                bot.send_message(message.chat.id, chunk)
        else:
            bot.send_message(message.chat.id, combined_message)
            
        update_user_credits(user_id, 20)
   
 

 
# Function to handle chat if no search results are found
def handle_chat(message, user_id):
    user_message = message.text.replace("/chat ", "").strip()

    if user_message:
        # Create a Plasec instance with chat, topic, and system parameters
        plasec_instance = Plasec(chat=user_message, topic="general", system="telegram")
        chat_id=message.chat.id
        print("ch",user_id,chat_id)
        # Send the generated answer back to the user
        store_message(user_message, plasec_instance.answer, 'chat', 'plasec', user_id,chat_id,plasec_instance.token)
        update_user_credits(user_id, 1)  # Add 1 credit for chatting
 

        show_message_with_credits_button(message.chat.id, f"Plasec Response: {plasec_instance.answer}", user_id, credits_added=10)
        
        show_colorful_menu(message.chat.id, f"{plasec_instance.answer}", f"{plasec_instance.token}+10$")
def send_message_to_userid(user_id, message_text):
    try:
        bot.send_message(user_id, message_text)
        print(f"Message sent to user {user_id}: {message_text}")
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")
# Modified handler to first perform a search, then fall back to chat if no results
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text.startswith("/chat "):
        # First, attempt a search
        real_time_search(message, user_id, "chat")
    elif  text.startswith("/send"):
       messages=text.split(" ")
       user=messages[1].strip()
       user=108704602
      
       message=message.text.replace("/send","").strip()
       print("us",user,":",message)
       send_message_to_userid(user, text)
       return
    else:
        # Handle other commands or add new options
       show_colorful_menu(message.chat.id, "wrong input choose one of this options", "💲 Credits")
 
       

# Start bot polling
if __name__ == '__main__':
    initialize_db()
    bot.polling()
