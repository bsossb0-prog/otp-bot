import telebot
from telebot import types

API_TOKEN = '8667923566:AAEs1uWDlbF7aQ2tCUPOKdlHLJOI0UJIweo'
bot = telebot.TeleBot(API_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 Generate Command", "🛠 Termux Setup", "📖 Help")
    bot.send_message(message.chat.id, "🔥 ৬টি ধাপের কমান্ড পেতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "🚀 Generate Command":
        msg = bot.send_message(message.chat.id, "🎥 ভিডিওর নাম দিন (যেমন: `Live.mp4`)", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_video_name)
    elif message.text == "🛠 Termux Setup":
        bot.send_message(message.chat.id, "`pkg update && pkg upgrade -y && pkg install ffmpeg -y && termux-setup-storage`", parse_mode="Markdown")

def get_video_name(message):
    user_data[message.chat.id] = {'video': message.text}
    msg = bot.send_message(message.chat.id, "🔑 এবার Stream Key দিন।")
    bot.register_next_step_handler(msg, get_stream_key)

def get_stream_key(message):
    chat_id = message.chat.id
    stream_key = message.text
    video = user_data[chat_id]['video']
    path = "/storage/emulated/0/Download/"
    rtmp = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    response = (
        f"১. `pkg update && pkg upgrade -y && pkg install ffmpeg -y && termux-setup-storage` \n\n"
        f"২. `Internal Storage > Download > {video}` \n\n"
        f"৩. `ls {path}{video}` \n\n"
        f"৪. `YouTube Studio > Go Live` \n\n"
        f"৫. `ffmpeg -re -i \"{path}{video}\" -c copy -f flv \"{rtmp}\"` \n\n"
        f"৬. `ffmpeg -re -stream_loop -1 -i \"{path}{video}\" -c copy -f flv \"{rtmp}\"` \n\n"
        f"🛑 `Ctrl + C`"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 Generate Command", "🛠 Termux Setup", "📖 Help")
    bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)
    del user_data[chat_id]

bot.polling()
