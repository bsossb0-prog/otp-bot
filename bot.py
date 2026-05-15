import telebot
from telebot import types

# ---------------------------------------------------------
# নিচে আপনার বট টোকেনটি বসান (যেমন: '123456:ABC-DEF...')
API_TOKEN = '8667923566:AAEs1uWDlbF7aQ2tCUPOKdlHLJOI0UJIweo' 
# ---------------------------------------------------------

bot = telebot.TeleBot(API_TOKEN)

# স্টার্ট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 Generate Command")
    btn2 = types.KeyboardButton("🛠 Termux Setup")
    btn3 = types.KeyboardButton("📖 Help")
    markup.add(btn1, btn2, btn3)
    
    welcome_msg = (
        "👋 স্বাগতম নায়েম ভাই!\n\n"
        "এই বট আপনাকে YouTube Live করার জন্য সঠিক FFmpeg কমান্ড তৈরি করে দেবে।"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🚀 Generate Command":
        msg = bot.send_message(message.chat.id, "আপনার ভিডিওর নাম এবং স্ট্রিম কি (Stream Key) দিন।\n\nউদাহরণ: `live.mp4 your-key-here`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_ffmpeg)
    
    elif message.text == "🛠 Termux Setup":
        setup_text = (
            "টার্মাক্স সেটআপ কমান্ড:\n\n"
            "`pkg update && pkg upgrade -y` \n"
            "`termux-setup-storage` \n"
            "`pkg install ffmpeg -y`"
        )
        bot.send_message(message.chat.id, setup_text, parse_mode="Markdown")
        
    elif message.text == "📖 Help":
        help_text = (
            "১. আপনার ভিডিওর নাম `live.mp4` রাখুন।\n"
            "২. ভিডিওটি ফোনের Download ফোল্ডারে থাকতে হবে।\n"
            "৩. এই বট থেকে জেনারেট করা কমান্ডটি Termux-এ পেস্ট করুন।"
        )
        bot.send_message(message.chat.id, help_text)

# কমান্ড তৈরির লজিক
def process_ffmpeg(message):
    try:
        user_input = message.text.split()
        if len(user_input) < 2:
            bot.reply_to(message, "❌ ভুল হয়েছে! ভিডিওর নাম এবং স্ট্রিম কি-এর মাঝে একটি স্পেস (Space) দিন।")
            return
        
        v_name = user_input[0]
        s_key = user_input[1]
        
        # FFmpeg কমান্ড ফরম্যাট
        final_cmd = f'ffmpeg -re -i {v_name} -c:v libx264 -preset veryfast -b:v 2500k -c:a aac -f flv "rtmp://a.rtmp.youtube.com/live2/{s_key}"'
        
        # ইনলাইন কপি বাটন
        markup = types.InlineKeyboardMarkup()
        btn_studio = types.InlineKeyboardButton("🌐 Go to YouTube Studio", url="https://studio.youtube.com")
        markup.add(btn_studio)
        
        bot.send_message(message.chat.id, f"✅ আপনার কমান্ড তৈরি:\n\n`{final_cmd}`", parse_mode="Markdown", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, "দুঃখিত, কমান্ড তৈরি করতে সমস্যা হয়েছে।")

# বট পোলিং শুরু
print("বটটি এখন সচল...")
bot.polling()
