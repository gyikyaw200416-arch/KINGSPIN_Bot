import os
import telebot
from flask import Flask, request
from supabase import create_client

# Environment Variables မှ ခေါ်ယူပါ (Vercel Settings တွင် ထည့်ထားပြီးဖြစ်ရမည်)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def webhook():
    # Telegram မှ ပေးပို့သော JSON ကို လက်ခံခြင်း
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Forbidden', 403

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please join our channel: https://t.me/Minings2026")

@app.route('/')
def home():
    return "Bot is active", 200

# Vercel အတွက် အရေးကြီးသည်
if __name__ == "__main__":
    app.run()
