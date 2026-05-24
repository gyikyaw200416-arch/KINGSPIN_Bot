import telebot
import os
from flask import Flask, request

# Hardcoding the token for testing as requested
BOT_TOKEN = "8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def webhook():
    # Receive the update from Telegram
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        # Process the update
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Welcome! Please join our channel: https://t.me/Minings2026")

@app.route('/')
def home():
    return "Bot is running", 200

if __name__ == "__main__":
    app.run()
