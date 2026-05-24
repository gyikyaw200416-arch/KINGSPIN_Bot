import telebot
from flask import Flask, request

# Token ကို ဒီမှာ တိုက်ရိုက်ထည့်လိုက်ပါ
BOT_TOKEN = "8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws"
bot = telebot.TeleBot(BOT_TOKEN)
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
    bot.reply_to(message, "Welcome! Bot is working.")

if __name__ == "__main__":
    app.run()
