import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# လင့်ခ်များ
APK_DIRECT_URL = "https://t.me/fotmovtv/15"
WEBSITE_URL = "http://bamarthan.vercel.app/"
ADMIN_GROUP_URL = "https://t.me/addlist/uO9JW9MOK-ZlM2M9"
ADMIN_FB_URL = "https://www.facebook.com/share/1GsFpU5pPH/"

# Vercel Webhook အတွက် Route နှစ်ခုစလုံးကို အလုပ်လုပ်အောင် ပြင်ဆင်ထားပါသည်
@app.route('/', methods=['GET', 'POST'])
@app.route('/api/webhook', methods=['GET', 'POST'])
def telegram_webhook():
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'OK', 200
        return 'Invalid JSON', 400
    return "FOTMOV TV Bot Webhook Running!"

# 🌟 1. /start Command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **မင်္ဂလာပါ သယ်ရင်းရေ...**\n"
        "🚀 **FOTMOV TV Official APK Downloader Bot** မှ ကြိုဆိုပါတယ်ဗျာ။\n\n"
        "⚠️ **[အရေးကြီး] အသုံးမပြုမီ အောက်ပါအညွှန်းစာကို သေချာဖတ်ရန် လိုအပ်ပါသည် -**\n"
        "၁။ ဖုန်းထဲတွင် Version အဟောင်းရှိပါက **Uninstall (ဖျက်ပစ်ရန်)** လိုအပ်ပါသည်။\n"
        "၂။ အောက်ပါ ဒေါင်းလုဒ်ခလုတ်ကို နှိပ်၍ APK အသစ်ကို ရယူတပ်ဆင်ပါ။\n"
        "၃။ လိုင်းမငြိမ်ပါက VPN အသုံးပြုပေးပါ။\n\n"
        "👇 အောက်ပါ ခလုတ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါပြီ -"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📥 APK File Direct Download", url=APK_DIRECT_URL))
    markup.add(InlineKeyboardButton("🌐 Visit Official Website", url=WEBSITE_URL))
    markup.add(InlineKeyboardButton("👥 Admin Group/Channel", url=ADMIN_GROUP_URL),
               InlineKeyboardButton("👤 Admin FB Account", url=ADMIN_FB_URL))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# 🆕 2. New Member Join
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        text = f"👋 မင်္ဂလာပါ {new_member.first_name} ရေ!\nFOTMOV TV Group မှ ကြိုဆိုပါတယ်။"
        markup = InlineKeyboardMarkup()
        bot_user = bot.get_me().username
        markup.add(InlineKeyboardButton("🤖 Bot စတင်ရန် (/start)", url=f"https://t.me/{bot_user}?start=start"))
        bot.send_message(message.chat.id, text, reply_markup=markup)

# အခြားစာပို့လျှင် /start ပြန်ပြခြင်း
@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    if message.content_type != 'text': return
    bot.reply_to(message, "💡 FOTMOV TV APK ရယူရန်အတွက် /start ဟု နှိပ်ပေးပါ သယ်ရင်း။")

# Vercel အသိအမှတ်ပြုရန် ၎င်းကို အောက်ဆုံးတွင် ထည့်ပေးပါ
handler = app
