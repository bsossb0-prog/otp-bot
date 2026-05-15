import telebot
from telebot import types
import os

# আপনার বট টোকেন দিন
API_TOKEN = '8667923566:AAEs1uWDlbF7aQ2tCUPOKdlHLJOI0UJIweo'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 Generate Command")
    btn2 = types.KeyboardButton("🛠 Termux Setup")
    btn3 = types.KeyboardButton("📖 Help")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "🔥 Nayem ভাই, আপনার Termux Live জেনারেটর রেডি!\nনিচের বাটনে ক্লিক করে কমান্ড জেনারেট করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "🚀 Generate Command":
        msg = bot.send_message(message.chat.id, "🎥 ভিডিওর নাম এবং স্ট্রিম কি দিন।\n\nউদাহরণ: `Live.mp4 your-key-here`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, generate_all_commands)
    
    elif message.text == "🛠 Termux Setup":
        setup_text = (
            "🛠 **Step 1: Update & Install Packages**\n"
            "`pkg update && pkg upgrade -y` \n"
            "`pkg install ffmpeg -y` \n"
            "`termux-setup-storage`"
        )
        bot.send_message(message.chat.id, setup_text, parse_mode="Markdown")

def generate_all_commands(message):
    try:
        data = message.text.split()
        if len(data) < 2:
            bot.reply_to(message, "❌ ফরম্যাট ভুল! `video.mp4 key` এভাবে দিন।")
            return
        
        video, key = data[0], data[1]
        path = "/storage/emulated/0/Download/"
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{key}"

        # সব কমান্ড সাজানো
        response = (
            "✅ **আপনার সব কমান্ড রেডি!**\n\n"
            "📂 **Step 1: Check Video Path**\n"
            f"`ls {path}{video}`\n\n"
            "🚀 **Step 2: Start Live (একবার চলবে)**\n"
            f'`ffmpeg -re -i "{path}{video}" -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -f flv "{rtmp_url}"` \n\n'
            "🔄 **Step 3: Loop Live (ভিডিও বারবার চলবে)**\n"
            f'`ffmpeg -re -stream_loop -1 -i "{path}{video}" -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -f flv "{rtmp_url}"` \n\n'
            "🛑 **Stop Live:**\n"
            "`Ctrl + C`"
        )

        # ইনলাইন বাটন (YouTube Studio তে যাওয়ার জন্য)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Open YouTube Studio", url="https://studio.youtube.com/video/live/0"))
        
        bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, "Error: কমান্ড জেনারেট করা সম্ভব হয়নি।")

bot.polling()
