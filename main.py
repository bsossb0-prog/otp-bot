import telebot
import random
import time
import threading
from telebot.types import *

TOKEN = "8253626154:AAGWBaV4GXs6klQDYAnwn1NdDcD1b02fbAk"

GROUP_ID = -1003549378995
ADMIN_ID = 8626918981

CHANNEL_LINK = "https://t.me/YOUR_CHANNEL"
BOT_LINK = "https://t.me/numberfast12_bot"

bot = telebot.TeleBot(TOKEN)

running = False
speed = 3
otp_count = 0


services = [
"Facebook",
"Telegram",
"Google",
"WhatsApp",
"TikTok",
"Apple",
"1xBet"
]


countries = [

{"name":"Bangladesh","flag":"🇧🇩","code":"#BD","prefix":"+88019","active":True,"service":"Telegram"},
{"name":"Italy","flag":"🇮🇹","code":"#IT","prefix":"+39347","active":True,"service":"Telegram"},
{"name":"USA","flag":"🇺🇸","code":"#US","prefix":"+1201","active":True,"service":"Google"},
{"name":"Pakistan","flag":"🇵🇰","code":"#PK","prefix":"+923","active":True,"service":"WhatsApp"},
{"name":"Vietnam","flag":"🇻🇳","code":"#VN","prefix":"+849","active":True,"service":"TikTok"}

]


def is_admin(user_id):
    return user_id == ADMIN_ID


def main_menu():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("⚡ Speed","📊 OTP Stats")
    kb.row("🌍 Countries","🔧 Service Edit")
    kb.row("▶ Start Generator","⏹ Stop Generator")

    return kb


def mask_number(prefix):

    last = random.randint(100,999)

    return f"{prefix}***{last}"


def generate_otp(service):

    if service == "Telegram":
        return random.randint(10000,99999)

    return random.randint(100000,999999)


def generator():

    global otp_count

    while True:

        if running:

            active = [c for c in countries if c["active"]]

            if not active:
                time.sleep(2)
                continue

            c = random.choice(active)

            number = mask_number(c["prefix"])

            otp = generate_otp(c["service"])

            text = f"""
{c['flag']} {c['name']} {c['code']} 📱 {c['service']}

{number}

🔑 {otp}
"""

            kb = InlineKeyboardMarkup()

            kb.row(
            InlineKeyboardButton("📢 Main Channel",url=CHANNEL_LINK),
            InlineKeyboardButton("🤖 Number Bot",url=BOT_LINK)
            )

            try:

                bot.send_message(GROUP_ID,text,reply_markup=kb)

                otp_count += 1

            except:
                pass

        time.sleep(speed)


threading.Thread(target=generator).start()


@bot.message_handler(commands=['start'])
def start(msg):

    if not is_admin(msg.from_user.id):
        return

    bot.send_message(msg.chat.id,"🤖 OTP BOT READY",reply_markup=main_menu())


@bot.message_handler(func=lambda m:True)
def panel(msg):

    global running

    if not is_admin(msg.from_user.id):
        return


    if msg.text == "⚡ Speed":

        kb = ReplyKeyboardMarkup(resize_keyboard=True)

        kb.row("1s","2s","3s")
        kb.row("5s","10s","50s")
        kb.row("1m","2m")
        kb.row("⬅ Back")

        bot.send_message(msg.chat.id,"⚡ Select Speed",reply_markup=kb)


    elif msg.text.endswith("s"):

        global speed

        speed = int(msg.text.replace("s",""))

        bot.send_message(msg.chat.id,f"⚡ Speed Set : {speed} sec",reply_markup=main_menu())


    elif msg.text.endswith("m"):

        speed = int(msg.text.replace("m",""))*60

        bot.send_message(msg.chat.id,f"⚡ Speed Set : {speed} sec",reply_markup=main_menu())


    elif msg.text == "🌍 Countries":

        kb = InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            status = "✅" if c["active"] else "❌"

            kb.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']} {status}",
            callback_data=f"country_{i}"
            )
            )

        kb.row(InlineKeyboardButton("⬅ Back",callback_data="back"))

        bot.send_message(msg.chat.id,"🌍 Country Manager",reply_markup=kb)


    elif msg.text == "🔧 Service Edit":

        kb = InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            kb.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"servicecountry_{i}"
            )
            )

        kb.row(InlineKeyboardButton("⬅ Back",callback_data="back"))

        bot.send_message(msg.chat.id,"🔧 Select Country",reply_markup=kb)


    elif msg.text == "📊 OTP Stats":

        bot.send_message(msg.chat.id,f"📊 OTP Generated : {otp_count}")


    elif msg.text == "▶ Start Generator":

        running = True

        bot.send_message(msg.chat.id,"✅ Generator Started")


    elif msg.text == "⏹ Stop Generator":

        running = False

        bot.send_message(msg.chat.id,"🛑 Generator Stopped")


    elif msg.text == "⬅ Back":

        bot.send_message(msg.chat.id,"🔙 Back",reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call:True)
def callbacks(call):

    if call.from_user.id != ADMIN_ID:
        return


    if call.data.startswith("country_"):

        i = int(call.data.split("_")[1])

        countries[i]["active"] = not countries[i]["active"]

        status = "ON" if countries[i]["active"] else "OFF"

        bot.answer_callback_query(call.id,f"{countries[i]['name']} {status}")


    elif call.data.startswith("servicecountry_"):

        i = int(call.data.split("_")[1])

        kb = InlineKeyboardMarkup()

        for s in services:

            kb.row(
            InlineKeyboardButton(
            s,
            callback_data=f"setservice_{i}_{s}"
            )
            )

        kb.row(InlineKeyboardButton("⬅ Back",callback_data="back"))

        bot.edit_message_text("Select Service",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb)


    elif call.data.startswith("setservice_"):

        data = call.data.split("_")

        i = int(data[1])

        service = data[2]

        countries[i]["service"] = service

        bot.answer_callback_query(call.id,f"{countries[i]['name']} → {service}")


    elif call.data == "back":

        bot.delete_message(call.message.chat.id,call.message.message_id)



print("BOT RUNNING...")

bot.infinity_polling()
