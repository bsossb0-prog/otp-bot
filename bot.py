import telebot
from telebot import types

# আপনার বট টোকেনটি এখানে বসান
API_TOKEN = '8667923566:AAEs1uWDlbF7aQ2tCUPOKdlHLJOI0UJIweo'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 Generate Command")
    btn2 = types.KeyboardButton("🛠 Termux Setup")
    btn3 = types.KeyboardButton("📖 Help")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "🔥 Nayem ভাই, আপনার প্রফেশনাল জেনারেটর রেডি!\n\n৬টি ধাপের কমান্ড পেতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "🚀 Generate Command":
        msg = bot.send_message(message.chat.id, "🎥 প্রথমে আপনার ভিডিওর নাম দিন।\n\nউদাহরণ: `Live.mp4`", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_video_name)
    
    elif message.text == "🛠 Termux Setup":
        setup_text = (
            "🛠 **Termux Setup Commands**\n\n"
            "`pkg update && pkg upgrade -y && pkg install ffmpeg -y && termux-setup-storage`"
        )
        bot.send_message(message.chat.id, setup_text, parse_mode="Markdown")

def get_video_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'video': message.text}
    msg = bot.send_message(chat_id, f"✅ ভিডিও: `{message.text}`\n\n🔑 এবার আপনার **Stream Key** দিন।", parse_mode="Markdown")
    bot.register_next_step_handler(msg, get_stream_key)

def get_stream_key(message):
    chat_id = message.chat.id
    stream_key = message.text
    video_name = user_data[chat_id]['video']
    path = "/storage/emulated/0/Download/"
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    # ভিডিওর মতো হুবহু ৬টি ধাপে সাজানো রেসপন্স
    response = (
        "✅ **আপনার সব কমান্ড ৬টি ধাপে রেডি!**\n\n"
        "🛠 **Step 1: Update & Install Packages**\n"
        "`pkg update && pkg upgrade -y && pkg install ffmpeg -y && termux-setup-storage` \n\n"
        "📂 **Step 2: Video File Path**\n"
        f"Internal Storage > Download > `{video_name}`\n\n"
        "🔍 **Step 3: Check Video File**\n"
        f"`ls {path}{video_name}`\n\n"
        "🌐 **Step 4: Open YouTube Studio**\n"
        "Desktop বা YouTube Studio খুলুন, Go Live করুন।\n\n"
        "🚀 **Step 5: Start Live (একবার চলবে)**\n"
        f'`ffmpeg -re -i "{path}{video_name}" -c copy -f flv "{rtmp_url}"` \n\n'
        "🔄 **Step 6: Loop Live (ভিডিও বারবার চলবে)**\n"
        f'`ffmpeg -re -stream_loop -1 -i "{path}{video_name}" -c copy -f flv "{rtmp_url}"` \n\n'
        "🛑 **Stop Live:** `Ctrl + C` চাপুন।"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 Generate Command", "🛠 Termux Setup", "📖 Help")
    
    bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)
    del user_data[chat_id]

bot.polling()
