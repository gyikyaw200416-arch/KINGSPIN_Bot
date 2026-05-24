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

# --- Helper Functions (Keep your original logic) ---
def check_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

# --- Message Handler ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = str(message.from_user.id)
    
    # 1. Force Join Protection
    if not check_user_joined(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="📢 Join Channel Now", url="https://t.me/Minings2026"))
        bot.reply_to(message, "⚠️ Access Denied! Please join our channel first.", reply_markup=markup)
        return

    # 2. Add your game logic and commands here...
    if message.text.startswith('/start'):
        bot.reply_to(message, "Welcome to KingSpin! Use /spin to play.")
    
    # Continue with your original /spin, /balance, /withdraw logic...

if __name__ == "__main__":
    app.run()
