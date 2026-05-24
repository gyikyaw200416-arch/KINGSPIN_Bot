import telebot
from flask import Flask, request

# Token ကို ဒီအတိုင်း တိုက်ရိုက်သုံးပါ
BOT_TOKEN = "8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def webhook():
    # Telegram မှ လာသော request ကို လက်ခံခြင်း
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is now working! Join our channel: https://t.me/Minings2026")

@app.route('/')
def home():
    return "Bot is alive", 200

if __name__ == "__main__":
    app.run()
