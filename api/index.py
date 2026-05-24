import os
import telebot
from flask import Flask, request

# Bot Configuration (Using environment variables is recommended for security)
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8871290779:AAEBWy17HHbYpMuc9D-ZKI7h8x2R5Ky5Cws')
CHANNEL_ID = '@Minings2026'

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# --- Webhook Endpoint ---
@app.route('/api', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# --- Helper Functions ---
def check_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

def get_user_display(user):
    """Returns a clickable mention if username exists, otherwise returns first name."""
    if user.username:
        return f"@{user.username}"
    return f"[{user.first_name}](tg://user?id={user.id})"

# --- Unified Message & Dice Handler ---
@bot.message_handler(func=lambda message: True, content_types=['text', 'dice', 'sticker', 'photo', 'video', 'document', 'animation'])
def handle_all_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # 1. Force Join Protection (Only for Groups/Supergroups)
    if message.chat.type in ['group', 'supergroup']:
        # Admin Bypass
        is_admin = False
        try:
            status = bot.get_chat_member(chat_id, user_id).status
            if status in ['creator', 'administrator']:
                is_admin = True
        except: 
            pass
        
        if not is_admin and not check_user_joined(user_id):
            try:
                # Delete the unauthorized message
                bot.delete_message(chat_id, message.message_id)
                
                # Create the Join button
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text="📢 Join Channel Now", url="https://t.me/Minings2026"))
                
                # Format the message
                user_display = get_user_display(message.from_user)
                alert_text = (f"⚠️ **Access Restricted**\n\n"
                              f"Hello {user_display},\n"
                              f"You must join our official channel to interact with this group. "
                              f"Please join to proceed.")
                
                bot.send_message(chat_id, alert_text, reply_markup=markup, parse_mode="Markdown")
                return
            except Exception as e:
                print(f"Error handling force join: {e}")
                return

    # 2. Logic Execution (Only if Member or Admin)
    if message.text and message.text.startswith('/start'):
        bot.reply_to(message, "Welcome to KingSpin! Use /spin to play.")
    
    # Add your /spin, /balance logic below this line...

if __name__ == "__main__":
    app.run()
