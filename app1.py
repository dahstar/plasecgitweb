# Code with added /chat command for interaction-based credit deduction

import os
import sqlite3
import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import time

# Initialize bot with token (set your own token)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_BETA")
bot = telebot.TeleBot(TOKEN)

# Database setup and initialization
DB_PATH = 'profile.db'

def initialize_database():
    """Initialize or update the database schema for user scores and credits."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        score INTEGER DEFAULT 0,
        credits INTEGER DEFAULT 100
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
initialize_database()

# Helper functions
def add_user_if_not_exists(user_id, username):
    """Adds a user to the database if they don't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def update_user_score(user_id, points=10):
    """Increment the user's score by a given number of points."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET score = score + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def deduct_credits(user_id, amount=10):
    """Deduct credits from the user upon each interaction."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    current_credits = cursor.fetchone()
    
    if current_credits and current_credits[0] >= amount:
        cursor.execute("UPDATE users SET credits = credits - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
    conn.close()

# Bot command handlers
@bot.message_handler(commands=['start'])
def handle_start(message):
    """Welcome message and user registration."""
    user_id = message.from_user.id
    username = message.from_user.username
    add_user_if_not_exists(user_id, username)
    
    bot.reply_to(message, "Welcome to the bot! You have been registered. Use /play to gain points, /status to check your balance, /search to look for info, or /help for assistance.")

@bot.message_handler(commands=['play'])
def handle_play(message):
    """Add points to user's score when they play."""
    user_id = message.from_user.id
    update_user_score(user_id)
    
    bot.reply_to(message, "You've earned 10 points! Keep playing to increase your score.")

@bot.message_handler(commands=['status'])
def handle_status(message):
    """Display user's score and credit status."""
    user_id = message.from_user.id
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT score, credits FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        bot.reply_to(message, f"Your score: {result[0]}\nYour credits: {result[1]}")
    else:
        bot.reply_to(message, "User not found. Please start with /start command.")

@bot.message_handler(commands=['search'])
def handle_search(message):
    """Placeholder for search functionality."""
    query = message.text[8:].strip()
    if query:
        bot.reply_to(message, f"Searching for '{query}'... (This is a placeholder function)")
    else:
        bot.reply_to(message, "Please provide search terms after the /search command.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Provide information on bot commands and usage."""
    help_text = (
        "Here are the available commands:\n"
        "/start - Register and start using the bot\n"
        "/play - Play a game and earn points\n"
        "/status - Check your current score and credits\n"
        "/search <query> - Perform a search (placeholder)\n"
        "/chat - Start a chat interaction (10 credits deducted per chat)\n"
        "/help - Show this help message\n\n"
        "Each chat interaction or message deducts 10 credits. Play more to keep earning points and credits!"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    """Simulate a chat interaction and deduct credits."""
    user_id = message.from_user.id
    deduct_credits(user_id)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    credits = cursor.fetchone()[0]
    conn.close()
    
    if credits <= 0:
        bot.reply_to(message, "You are out of credits! Please use /play to earn more credits.")
    else:
        bot.reply_to(message, "You're in chat mode! 10 credits have been deducted. Use /status to check your balance.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Deduct credits for each message sent."""
    user_id = message.from_user.id
    deduct_credits(user_id)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    credits = cursor.fetchone()[0]
    conn.close()
    
    if credits <= 0:
        bot.reply_to(message, "You are out of credits! Please use /play to earn more credits.")
    else:
        bot.reply_to(message, "Message received! 10 credits deducted. Use /status to check your balance.")

# Start polling
if __name__ == "__main__":
    bot.polling(none_stop=True)
