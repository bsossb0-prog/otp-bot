import telebot
from telebot import types
import os

# আপনার বট টোকেন দিন
API_TOKEN = '8667923566:AAEs1uWDlbF7aQ2tCUPOKdlHLJOI0UJIweo'
bot = telebot.TeleBot(API_TOKEN)

# ইউজার ডেটা সাময়িকভাবে রাখার জন্য ডিকশনারি
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 Generate Command")
    btn2 = types.KeyboardButton("🛠 Termux Setup")
    btn3 = types.KeyboardButton("📖 Help")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "🔥 Nayem ভাই, আপনার Termux Live জেনারেটর রেডি!\n\nকমান্ড তৈরি করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "🚀 Generate Command":
        msg = bot.send_message(message.chat.id, "🎥 প্রথমে আপনার ভিডিওর নাম দিন।\n\nউদাহরণ: `Live.mp4`", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_video_name)
    
    elif message.text == "🛠 Termux Setup":
        setup_text = (
            "🛠 **Step 1: Update & Install Packages**\n"
            "`pkg update && pkg upgrade -y` \n"
            "`pkg install ffmpeg -y` \n"
            "`termux-setup-storage`"
        )
        bot.send_message(message.chat.id, setup_text, parse_mode="Markdown")

# ধাপ ১: ভিডিওর নাম নেওয়া
def get_video_name(message):
    chat_id = message.chat.id
    video_name = message.text
    user_data[chat_id] = {'video': video_name} # ভিডিওর নাম সেভ হলো
    
    msg = bot.send_message(chat_id, f"✅ ভিডিওর নাম: `{video_name}`\n\n🔑 এবার আপনার ইউটিউব **Stream Key** দিন।", parse_mode="Markdown")
    bot.register_next_step_handler(msg, get_stream_key)

# ধাপ ২: স্ট্রিম কি নেওয়া এবং কমান্ড জেনারেট করা
def get_stream_key(message):
    chat_id = message.chat.id
    stream_key = message.text
    video_name = user_data[chat_id]['video'] # আগের ধাপে সেভ করা ভিডিওর নাম
    
    path = "/storage/emulated/0/Download/"
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    response = (
        "✅ **আপনার সব কমান্ড রেডি!**\n\n"
        "📂 **Step 1: Check Video Path**\n"
        f"`ls {path}{video_name}`\n\n"
        "🚀 **Step 2: Start Live (একবার চলবে)**\n"
        f'`ffmpeg -re -i "{path}{video_name}" -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -f flv "{rtmp_url}"` \n\n'
        "🔄 **Step 3: Loop Live (ভিডিও বারবার চলবে)**\n"
        f'`ffmpeg -re -stream_loop -1 -i "{path}{video_name}" -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -f flv "{rtmp_url}"` \n\n'
        "🛑 **Stop Live:** `Ctrl + C`"
    )

    # মেইন মেনু বাটন আবার ফিরিয়ে আনা
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 Generate Command", "🛠 Termux Setup", "📖 Help")
    
    bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)
    
    # ডেটা ক্লিয়ার করা
    del user_data[chat_id]

bot.polling()
