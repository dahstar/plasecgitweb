import os
import sqlite3
import telebot
from telebot.types import ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
from plasec import Plasec
user_id=0
plasec_instance =None
token=""
user_scores = {}
user_name=""
score=100
import time
import requests
from requests.exceptions import ConnectionError
import random
import urllib.request
allm=None
USER_DB_PATH="profile.db"
# Dictionary to track each user's current autopilot step
user_progress = {}

user_modes = {}
user_search_results = {}

username=""
import PlasecImage

# Initialize Telegram bot with your API Token
# Initialize bot with token (set your own token)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

bot.set_webhook()
allscore=0

@bot.message_handler(commands=['autopilot'])
def start_autopilot(message):
    global user_id
   
    set_autopilot_status(user_id, 1,1)

 
    bot.reply_to(message, "با /play برای گرفتن کردیت اضافه بازی کنید 🎮 یا با /exit خارج شوید.")
''''

 
def chat_command(message):
    user_id = message.from_user.id
    # Check if the user is on the "chat" step
    if user_progress.get(user_id) == "chat":
       
        chat_command(message)
        user_progress[user_id] = "score"  # Move to the final step

@bot.message_handler(commands=['score'])
def score_command(message):
    user_id = message.from_user.id
    # Check if the user is on the "score" step
    if user_progress.get(user_id) == "score":
        get_user_score(user_id)
        bot.reply_to(message, "پایان! شما همه مراحل را کامل کردید. 🎉")
        user_progress.pop(user_id)  # Clear progress after completion
'''
@bot.message_handler(commands=['exit'])
def exit_autopilot(message):
    user_id = message.from_user.id
    # End the autopilot session
    if user_id in user_progress:
        bot.reply_to(message, "  بزنید تا  اتوپایلوت خاتمه یابد/exit  ")

def add_user_if_not_exists(user_id, username,score=10):
    """Adds a user to the database if they don't already exist."""
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username,score) VALUES (?, ? ,?)", (user_id, username,score))
    conn.commit()
    conn.close()
def update_user_score(user_id, points=1):
    """Increment the user's score by a given number of points."""
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET score = score + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def deduct_credits(user_id, amount=10):
    """Deduct credits from the user upon each interaction."""
    print(f"deduct from {user_id}")
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    current_credits = cursor.fetchone()
    
    if current_credits and current_credits[0] >= amount:
        cursor.execute("UPDATE users SET credits = credits - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
    conn.close()

def deduct_score(user_id, amount=10):
 try:
    """Deduct credits from the user upon each interaction."""
    print(f"deduct score from {user_id}")
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    current_credits = cursor.fetchone()
    
    if current_credits and current_credits[0] >= amount:
        cursor.execute("UPDATE users SET score = score - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
    conn.close()
 except Exception as e:
       return f"error:{str(e)}"

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
def initialize_db_profile():
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_autopilot (
        user_id INTEGER PRIMARY KEY,
        autopilot INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close() 
def set_autopilot_status(user_id, status,current):
    # Connect to the database
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()

    # Insert or update the autopilot status for the user
    cursor.execute('''
    INSERT INTO user_autopilot (user_id, autopilot,currentrun) 
    VALUES (?, ?, ?)
    ON CONFLICT(user_id) 
    DO UPDATE SET autopilot=excluded.autopilot
    ''', (user_id, status,current))
    
    conn.commit()
    conn.close()
def get_autopilot_status(user_id):

    # Retrieve the autopilot status for a specific user
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT autopilot FROM user_autopilot WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result[0] if result else 0  # Return 0 if no record found


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
def get_user_score(user_id):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute('SELECT score FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    # If user does not exist, create a profile with 0 credits
    if result is None:
        return "you are not playing yet"
    conn.close()
    return result[0]  # Return the user's current score
def get_or_create_user_profile(user_id):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute('SELECT credits FROM user_profiles WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    # If user does not exist, create a profile with 0 credits
    if result is None:
        cursor.execute('INSERT INTO users (user_id, credits,score) VALUES (?, ?, ?)', (user_id, 10, 10))
        conn.commit()
        result = (0,)  # Default credits if the user is new

    conn.close()
    return result[0]  # Return the user's current credits

# Function to update user credits
def update_user_credits(user_id, credits_to_add):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()

    # Update the credits for the user
    cursor.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (credits_to_add, user_id))
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
    
def get_user_id_by_token(token):  
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM chat_history WHERE token = ?', (token,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
def get_message_credits(message=""):
    global score
    if "💲" in message:
      return f"you have {score} plasec now by playing add to them"
    if message=="":
       global plasec_instance
       return plasec_instance.get_price()
    else :
     user_id=get_user_id_by_token(message)
     mcredit=message.split("-")[-1].replace("$","")
     update_user_credits(user_id,float(mcredit)) 
     credit=get_user_credits(user_id)
     username=get_username_userid(user_id)
    
     return str(credit)+"-message credit:"+message.split("-")[-1]+"-"+str(username)
     
# Function to retrieve user credits
def get_message_token(chat_id):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token FROM chat_history WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
def get_username_userid(chat_id):
    conn = sqlite3.connect('profile.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_name FROM user_profiles WHERE user_id = ?', (chat_id,))
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
    start_chat_button = InlineKeyboardButton('💬 /chat [message] use credits in chat', callback_data='start_chat')
    search_button = InlineKeyboardButton('▶️ /play get chat in credits', callback_data='gameplay')
    register_button = InlineKeyboardButton('📝 /share soon', callback_data='handle_register')
    ref_button = InlineKeyboardButton('📝 /ref soon', callback_data='handle_register')
    autopilot_button = InlineKeyboardButton('/autopilot', callback_data='autopilot')
    credits_button = InlineKeyboardButton('💳 ' + crmessage, callback_data=crmessage)
    exit_button = InlineKeyboardButton('❌ /exit', callback_data='exit')
    if crmessage=="💲 Credits":
     # Add buttons to the markup
     markup.row(start_chat_button, search_button)
     markup.row(autopilot_button, credits_button)
     markup.row(exit_button)
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
    
     
    if call.data == "gameplay":
        bot.send_message(call.message.chat.id, " type /play for play or /score for score")
    elif call.data == "autopilot":
          start_autopilot(call.message)
    elif call.data=="get_search":
      
        user_modes[call.from_user.id] = "search"  # Switch to search mode
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "Help Menu: Choose an option to start a chat or search for information.")
    elif "$" in call.data or "💲" in call.data :
        user_id = call.from_user.id
        bot.send_message(call.message.chat.id, f"all credits:{get_message_credits(call.data)}")
    elif call.data == "get_credits_message":
        global plasec_instance
        price=get_credits_message()
       
        bot.send_message(call.message.chat.id, f"message credits:{get_message_credits()}")
    
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
    global user_id
    text=""
    user_id=message.from_user.id
   
    text="به پلاسیک خوش آمدید"
    text+="\\n"
    text+="برای آموزش بازی کردن از اتوپایلوت استفاده کنید" 
    text+="\\n"
    text+="با بازی کردیت بگیرید و با هوش مصنوعی و در آینده دوستان چت کنید و کردیت را سهیم شوید و از امکانات هوش مصنوعی پیشرفته استفاده کنید "
    text+="\\n"
    text+="نسخه دمو تک نفره)"
    text+="\\n"
         
    
    
    show_colorful_menu(message.chat.id,text)

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
   chat_id = message.chat.id   
   try: 
    global plasec_instance,user_id
    user_message = message.text.replace("/chat", "").strip()
    if user_id==0:
     user_id = message.from_user.id
    if user_message:
        # Create a Plasec instance
        plasec_instance = Plasec(chat=user_message, topic="general", system="telegram")
         # Retrieve the chat_id
        #deduct_credits(user_id,10)
        deduct_score(user_id,10)
        # Store the message, response, and chat_id in the database
        store_message(user_message, plasec_instance.answer, 'chat', 'plasec', user_id, chat_id, plasec_instance.token)
        # Show response and menu
        show_message_with_credits_button(message.chat.id, f"Plasec Response: {plasec_instance.answer}", user_id, credits_added=10)
        show_colorful_menu(message.chat.id, f"{plasec_instance.answer}", f"{plasec_instance.token}+plasec_instance.count$c")
       
   except Exception as e:
           bot.send_message(chat_id, f"error{str(e)}")
@bot.message_handler(commands=['chat'])
def real_time_search(message, task_type='search'):
    user_id = message.from_user.id
    search_term = message.text.strip().replace("/chat ", "")  # Extract the search term from the message

    # Perform a search based on the term
    results = search_history(user_id, search_term)
    autostarted=get_autopilot_status(user_id)
    print("auto",autostarted)
    if autostarted==1:
         bot.reply_to(message, "با /score کردیتتان را ببینید 📊 یا با /exit خارج شوید.")
    if search_term=="/chat":
        return
    if results:
        # If search results are found, display them and let the user choose
        user_search_results[user_id] = results
       
        result,token=display_search_results(message.chat.id, results)

        # Auto-select the first result or let the user pick
        if len(result)>1 :
         bot.register_next_step_handler(message, handle_search_selection, user_id)
    else:
        # If no results are found, fall back to chat
        global user_name
        user_name=message.from_user.username
        bot.send_message(message.chat.id, f"waiting for chat by {message.from_user.username}...")
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
                    show_colorful_menu(message.chat.id, f"{chunk}", f"{token}")
            else:
                # If less than 4096 characters, send the whole message
                #bot.send_message(message.chat.id, combined_message)
                
                print("tc",token)
                show_colorful_menu(message.chat.id, f"{combined_message}", f"{token}")

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
    d=get_user_score(user_id)
    if get_user_score(user_id)<10:
        bot.send_message(user_id, f"your :{d} isn't enough for chat")
        return
    if user_message:
        # Create a Plasec instance with chat, topic, and system parameters
        plasec_instance = Plasec(chat=user_message, topic="general", system="telegram")
        chat_id=message.chat.id
        print("ch",user_id,chat_id)
        # Send the generated answer back to the user
        store_message(user_message, plasec_instance.answer, 'chat', 'plasec', user_id,chat_id,plasec_instance.token)
        
        deduct_score(user_id, 10)  # remove credit for chatting
 
            
        show_message_with_credits_button(message.chat.id, f"Plasec Response: {plasec_instance.answer}", user_id, credits_added=10)
        
        show_colorful_menu(message.chat.id, f"{plasec_instance.answer}", f"{plasec_instance.token}")
# Function to handle chat if no search results are found
@bot.message_handler(commands=['image'])
def image_command(message):
    chat_text = message.text.replace("/image", "").strip()
    if chat_text:
        try:
            # Instantiate Plasec with image generation action
            d=PlasecImage.PlasecImage()
            image_url = d.get_image(f"/imagine {chat_text}")
            bot.send_photo(message.chat.id, image_url)  # Send image to user
        except Exception as e:
            bot.reply_to(message, f"Error generating image: {str(e)}")
    else:
               bot.reply_to(message, "Please provide a description for the image, e.g., /image mountain.")

    
def send_message_to_userid(user_id, message_text):
    try:
        bot.send_message(user_id, message_text)
        print(f"Message sent to user {user_id}: {message_text}")
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")
# Modified handler to first perform a search, then fall back to chat if no results
def get_random_credits(message=""):
    import random
    random_float = random.random() 
    random_int = random.randint(1, 10)
    return random_int
# /play command to start the game

@bot.message_handler(commands=['score'])
def show_score(message):
 global user_scores,user_name,score,allm,user_id
 allm=message
 
 markup = InlineKeyboardMarkup()


 score=get_user_score(user_id)
 bot.send_message(user_id, f"user plasec is:{score}")
 autostarted=get_autopilot_status(user_id)
 print("auto",autostarted)
 if autostarted==1:
         bot.send_message(message.chat.id, "با تشکر اتوپایوت به پایان رسید   ", reply_markup=markup)
         set_autopilot_status(user_id,0,1)
def read_link(url):
   data=""
   with urllib.request.urlopen(url) as response:
         data = response.read().decode('utf-8')  # Read and decode the 
   return data
@bot.message_handler(commands=['play'])
def play_game(message):
    markup = InlineKeyboardMarkup()
    try:
        global allm, user_id
        allm = message
        user_ids = message.from_user.id

        # Randomly assign points with weights
        points = random.choices([1, 5, 10], weights=[70, 20, 10], k=1)[0]
        deduct_credits(user_ids, -points)
        update_user_score(user_ids, points)

        # Determine the image URL based on points and description for the card
        image_url = f"https://playandsecure.com/docs/card{points}.png?nocache={random.randint(1, 10000)}"
        caption = f"You've earned {points} points!\n\n🃏 **Mission:** Upgrade your card by viewing ads!**"

        # Create a link to the HTML page with the points as a query parameter
        ads_page_url = f"https://www.playandsecure.com/plasec"
        button = InlineKeyboardButton("Upgrade Card - View Ads", url=ads_page_url)
        markup.add(button)

        # Send the image with caption and button
        bot.send_photo(
            message.chat.id,
            image_url,
            caption=caption,
            parse_mode='Markdown',
            reply_markup=markup
        )
        autostarted=get_autopilot_status(user_id)
        if autostarted:
            bot.send_message(
                message.chat.id,
                "حالا با کردیتان با /chat از هوش مصنوعی جواب بگیرید 🧠 یا با /exit خارج شوید.",
                reply_markup=markup
            )

    except Exception as e:
        bot.send_message(message.chat.id, f"Error 440: {str(e)}", reply_markup=markup)

# Handler for clicking the logo
@bot.callback_query_handler(func=lambda call: call.data == "click_logo")
def handle_click(call):
 
    points = random.choices([1, 5, 10], weights=[70, 20, 10], k=1)[0]
    #update_user_score(user_id, points)
    print("Cards",points)
     
    # Send the card image
    with open('card'+points+'.png', 'rb') as photo:
        bot.send_photo(user_id, photo, caption=f"You've earned {points} points! Keep playing to increase your score.")
  
@bot.message_handler(func=lambda message: True)
def handle_message(message):
   
    user_id = message.from_user.id
    text = message.text.strip()

    if text.startswith("/chat "):
        # First, attempt a search

        real_time_search(message, user_id, "chat")
    #elif text.startswith("/play "):
        # First, attempt a search
        #real_time_search(message, user_id, "chat")
    elif  text.startswith("/send"):
       messages=text.split(" ")
       user=messages[1].strip()
    
       message=message.text.replace("/send","").strip()
       print("us",user,":",message)
       send_message_to_userid(user, text)
       return
    else:
        # Handle other commands or add new options
       show_colorful_menu(message.chat.id, "wrong input choose one of this options", "💲 Credits")
 
       

# Start bot polling
if __name__ == '__main__':
    #initialize_db()
    initialize_db_profile()
    bot.polling()