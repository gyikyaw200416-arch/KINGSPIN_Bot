import telebot
import os
from flask import Flask, request
from supabase import create_client

# Credentials (Environment Variables များမှ ခေါ်သုံးပါသည်)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Client Initialization
bot = telebot.TeleBot(BOT_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

# Webhook Route (Telegram မှ မက်ဆေ့ချ်များ လက်ခံရန်)
@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# Command Handler (Bot စတင်သည့်အခါ)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please join our channel: https://t.me/Minings2026")

# Root Route (404 အမှားပြခြင်းကို ရှောင်ရန်)
@app.route('/')
def home():
    return "Bot is running perfectly!", 200

# Server execution
if __name__ == "__main__":
    app.run()
