import telebot
import os
from flask import Flask, request
from supabase import create_client

# Configuration Constants
# သင်ပေးထားတဲ့ Keys တွေကို ဒီမှာ တိုက်ရိုက်ထည့်ထားပါတယ်
BOT_TOKEN = "8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws"
SUPABASE_URL = "https://bysgzzqyubtgvdghldec.supabase.co"
SUPABASE_KEY = "sb_publishable_vDgpBMStthWM8aG1fPLqZw_Q2wqwsNG"
CHANNEL_LINK = "https://t.me/Minings2026"

# Initialize Bot and Supabase
bot = telebot.TeleBot(BOT_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

# Telegram Webhook Route
@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Forbidden', 403

# Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = f"Welcome! Please join our channel: {CHANNEL_LINK}"
    bot.reply_to(message, welcome_text)

# Default Route
@app.route('/')
def home():
    return "Bot is running perfectly!", 200

if __name__ == "__main__":
    app.run()
