import os
import random
import telebot
from flask import Flask, request
import requests

# Bot Configuration
BOT_TOKEN = '8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws'
CHANNEL_ID = '@Minings2026'

# Initialize Bot and App
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = "https://bysgzzqyubtgvdghldec.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5c2d6enF5dWJ0Z3ZkZ2hsZGVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MzM4ODQsImV4cCI6MjA5MzUwOTg4NH0.-4JDl5X--fNYrRyuaOzyUXz0FaJpIxNSLLzcjGrlavQ"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- Webhook Endpoint ---
@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@app.route('/')
def home():
    return "KingSpin Bot is running!", 200

# --- Helper Functions ---
def check_user_joined(user_id):
    try:
        # Note: Bot must be an administrator in the CHANNEL to check membership
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# --- Message Handler ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # 1. Force Join Protection (Only for Groups)
    if message.chat.type in ['group', 'supergroup']:
        # Bypass for Channel accounts (Anonymous Admins)
        if message.sender_chat and message.sender_chat.type == 'channel':
            pass 
        # Bypass for Group Admins
        elif bot.get_chat_member(chat_id, user_id).status in ['creator', 'administrator']:
            pass
        else:
            # Enforce Join Check
            if not check_user_joined(user_id):
                try:
                    bot.delete_message(chat_id, message.message_id)
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text="📢 Join Channel Now", url="https://t.me/Minings2026"))
                    bot.send_message(chat_id, f"⚠️ Access Denied! {message.from_user.first_name}, please join our channel first.", reply_markup=markup)
                    return
                except Exception as e:
                    print(f"Error enforcing channel link: {e}")
                    return

    # 2. Command Handling
    if message.text and message.text.startswith('/start'):
        bot.reply_to(message, "Welcome to KingSpin! Use /spin to play.")
    
    # Add your /spin, /balance, /withdraw logic here...

if __name__ == "__main__":
    app.run()
