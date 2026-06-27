import os
import time
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN required")

bot = telebot.TeleBot(BOT_TOKEN, threaded=True, num_threads=4)

# 🔄 Bot Username ကို တစ်ခါတည်း ရယူသိမ်းဆည်းထားမည်
BOT_USERNAME = None
try:
    BOT_USERNAME = bot.get_me().username
    logger.info(f"Bot initialized successfully as @{BOT_USERNAME}")
except Exception as e:
    logger.error(f"Failed to fetch bot username: {e}")

# 🌟 1. /start Command (HTML Parse Mode သို့ ပြောင်းလဲထားသည်)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 <b>မင်္ဂလာပါ သယ်ရင်းရေ...</b>\n"
        "🚀 <b>MyanmaJav Official Bot</b> မှ ကြိုဆိုပါတယ်။\n\n"
        "📢 <b>အရေးကြီး:</b> Main Group ကို join ရန် သူငယ်ချင်း (သို့) Group (၅) ခုသို့ ရှယ်ပေးဖို့ မေတ္တာရပ်ခံပါတယ်ခင်ဗျာ။\n\n"
        "👇 အောက်ပါ ခလုတ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါပြီ -"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("ပိုမိုကြည့်ရှု့ရန် Main Group 👈ကိုjoin ပါ", url="https://t.me/+nRpPeCCewcFhYWRl"),
        InlineKeyboardButton("nRpPeCCewcFhYWRlhYWRl BFA ADULTS 👈ကိုjoin ပါ", url="https://bfa-adults-tv.vercel.app/"),
        InlineKeyboardButton("Website မှကြည့်ရန်👈နှိပ်ပါ", url="https://shawdowless-xnxxburmese.static.hf.space/Adults.html"),
        InlineKeyboardButton("TikTok video Downloader", url="https://t.me/tknowatermarkdownloader"),
        InlineKeyboardButton("🇯🇵စာတန်းထိုး(Browser တခုဖြင့်ကြည့်ပါ)", url="https://ouo.io/12YBTq"),
        InlineKeyboardButton("🇯🇵ဆင်ဆာမပါ-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/BrFapmF"),
        InlineKeyboardButton("🇷🇺ရုရှား-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/3UTfd7"),
        InlineKeyboardButton("အာရှ-Browser တခုဖြင့်ကြည့်ပါ", url="https://ouo.io/kxRZBL"),
        InlineKeyboardButton("No ad-Apk Downloader👈နှိပ်ပါ", url="https://t.me/Fotmovdownloader"),
        InlineKeyboardButton("Admin Fb Acc.", url="https://www.facebook.com/share/17cje3nmAV/")
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=markup)

# 🆕 2. New Member Join
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.is_bot: 
            continue
        text = f"👋 မင်္ဂလာပါ {new_member.first_name} ရေ!\nFOTMOV TV Group မှ ကြိုဆိုပါတယ်။"
        markup = InlineKeyboardMarkup()
        
        # သတ်မှတ်ထားသော Username ကို သုံးရန်၊ မရှိပါက bot.get_me() ခေါ်ရန်
        username = BOT_USERNAME if BOT_USERNAME else bot.get_me().username
        markup.add(InlineKeyboardButton("🤖 Bot စတင်ရန် (/start)", url=f"https://t.me/{username}?start=start"))
        bot.send_message(message.chat.id, text, reply_markup=markup)

# 🛑 3. Catch-all Handler (Private Chat တွင်သာ အလုပ်လုပ်ရန် ကန့်သတ်ထားသည်)
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_all_other_messages(message):
    if message.content_type != 'text': 
        return
    bot.reply_to(message, "💡 Bot အသုံးပြုရန် /start ဟု နှိပ်ပေးပါ သယ်ရင်း။")

if __name__ == "__main__":
    logger.info("Starting MyanmaJav Bot with polling...")
    try:
        bot.remove_webhook()
    except Exception as e:
        logger.warning(f"Webhook removal skipped: {e}")
        
    time.sleep(1)
    
    while True:
        try:
            # infinity_polling သည် သူ့အလိုလို Reconnect လုပ်သော်လည်း Error အကြီးအကျယ်တက်ပါက loop က ကာကွယ်ပေးမည်
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Polling crashed: {e}")
            logger.info("Restarting in 15 seconds...")
            time.sleep(15)
            
