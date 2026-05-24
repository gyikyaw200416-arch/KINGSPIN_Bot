import telebot
from flask import Flask, request
from supabase import create_client

# Credentials
BOT_TOKEN = "8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws"
SUPABASE_URL = "https://bysgzzqyubtgvdghldec.supabase.co"
SUPABASE_KEY = "sb_publishable_vDgpBMStthWM8aG1fPLqZw_Q2wqwsNG"
CHANNEL_ID = "@Minings2026"

# Initialization
bot = telebot.TeleBot(BOT_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please join our channel: https://t.me/Minings2026")

@app.route('/')
def home():
    return "Bot is running perfectly!", 200
