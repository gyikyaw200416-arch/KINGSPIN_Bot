import os
import telebot
from flask import Flask, request
from supabase import create_client

# Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws')
ADMIN_BOT_TOKEN = os.environ.get('ADMIN_BOT_TOKEN') 
ADMIN_CHAT_ID = os.environ.get('ADMIN_ID')         
CHANNEL_ID = '@Minings2026'

# Supabase Setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# --- Helper Functions ---
def get_user_display(user):
    if user.username: return f"@{user.username}"
    return f"[{user.first_name}](tg://user?id={user.id})"

def check_user_joined(user_id):
    try: 
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['creator', 'administrator', 'member']
    except: 
        return False

# --- Webhook Endpoint ---
@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return 'OK', 200
    return 'Forbidden', 403

# --- Game & Withdraw Handlers ---
@bot.message_handler(commands=['spin'])
def spin_game(message):
    # Channel check included here for safety
    if not check_user_joined(message.from_user.id):
        bot.reply_to(message, "⚠️ Please join @Minings2026 to play!")
        return

    dice = bot.send_dice(message.chat.id, emoji='🎰')
    val = dice.dice.value
    
    rewards = {1: 0.01, 22: 0.02, 43: 0.05, 64: 0.1}
    reward = rewards.get(val, 0)
    
    if reward > 0:
        user_id = str(message.from_user.id)
        data = supabase.table("users").select("balance").eq("id", user_id).execute()
        current_bal = data.data[0]['balance'] if data.data else 0
        new_bal = round(current_bal + reward, 3)
        supabase.table("users").upsert({"id": user_id, "balance": new_bal}).execute()
        bot.reply_to(message, f"🎰 Congratulations! You won {reward} 💸.\nBalance: {new_bal} 💸")
    else:
        bot.reply_to(message, "🎰 Better luck next time!")

@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    user_id = str(message.from_user.id)
    data = supabase.table("users").select("balance").eq("id", user_id).execute()
    bal = data.data[0]['balance'] if data.data else 0
    
    if bal < 0.1:
        bot.reply_to(message, f"❌ Minimum withdrawal is 0.1 💸.\nYour balance: {bal} 💸")
    else:
        admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)
        text = f"🚨 **New Withdrawal Request**\nUser: {get_user_display(message.from_user)}\nAmount: {bal} 💸"
        admin_bot.send_message(ADMIN_CHAT_ID, text, parse_mode="Markdown")
        bot.reply_to(message, "✅ Withdrawal request sent to admin!")

# --- Unified Handler (Group Join Check & Commands) ---
@bot.message_handler(func=lambda message: True, content_types=['text', 'dice', 'sticker', 'photo', 'video', 'document', 'animation'])
def handle_all_messages(message):
    # 1. Group Join Check (Always active)
    if message.chat.type in ['group', 'supergroup']:
        user_id = message.from_user.id
        
        # Bypass Admins
        is_admin = False
        try:
            status = bot.get_chat_member(message.chat.id, user_id).status
            if status in ['creator', 'administrator']: is_admin = True
        except: pass
        
        if not is_admin and not check_user_joined(user_id):
            bot.delete_message(message.chat.id, message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text="📢 Join Channel Now", url="https://t.me/Minings2026"))
            bot.send_message(message.chat.id, f"⚠️ Hello {get_user_display(message.from_user)}, you must join the channel to interact!", reply_markup=markup, parse_mode="Markdown")
            return

    # 2. Commands Handling
    if message.text and message.text.startswith('/start'):
        bot.reply_to(message, "Welcome to KingSpin! Use /spin to play or /withdraw to cash out.")

if __name__ == "__main__":
    app.run()
