import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

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
        "🚀 **MyanmaJav Official Bot** မှ ကြိုဆိုပါတယ်။\n\n"
        "📢 **အရေးကြီး:** Main Group ကို join ရန် သူငယ်ချင်း (သို့) Group (၅) ခုသို့ ရှယ်ပေးဖို့ မေတ္တာရပ်ခံပါတယ်ခင်ဗျာ။\n\n"
        "👇 အောက်ပါ ခလုတ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါပြီ -"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton("ပိုမိုကြည့်ရှု့ရန် Main Group 👈ကိုjoin ပါ", url="https://t.me/+nRpPeCCewcFhYWRl"),
        InlineKeyboardButton("Website မှကြည့်ရန်👈နှိပ်ပါ", url="https://shawdowless-xnxxburmese.static.hf.space/Adults.html"),
        InlineKeyboardButton("TikTok video Downloader", url="https://t.me/tknowatermarkdownloader"),
        InlineKeyboardButton("🇯🇵စာတန်းထိုး(Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/12YBTq"),
InlineKeyboardButton("🇯🇵ဆင်ဆာမပါ-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/BrFapmF"),
InlineKeyboardButton("🇷🇺ရုရှား-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/3UTfd7"),
InlineKeyboardButton("အာရှ-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/kxRZBL"),
InlineKeyboardButton("No ad-Apk Downloader👈နှိပ်ပါ", url="https://t.me/Fotmovdownloader"),
        InlineKeyboardButton("Admin Fb Acc.", url="https://www.facebook.com/share/17cje3nmAV/")
    )
    
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
