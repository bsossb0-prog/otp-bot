import telebot
import random
import time
import threading
from telebot.types import *

TOKEN = "8253626154:AAGWBaV4GXs6klQDYAnwn1NdDcD1b02fbAk"
GROUP_ID = -1003549378995
ADMIN_ID = 8626918981

bot = telebot.TeleBot(TOKEN)

running = True
otp_count = 0

services = ["Facebook","Telegram","Google","WhatsApp","TikTok","Apple","1xBet"]

speed_options = {
"1s":1,
"2s":2,
"3s":3,
"5s":5,
"10s":10,
"50s":50,
"1m":60,
"2m":120
}

countries = [

{"name":"Bangladesh","flag":"🇧🇩","code":"#BD","prefix":"+88019","service":"Facebook","speed":1,"active":True},
{"name":"Italy","flag":"🇮🇹","code":"#IT","prefix":"+39347","service":"Telegram","speed":5,"active":False},
{"name":"USA","flag":"🇺🇸","code":"#US","prefix":"+1201","service":"Google","speed":10,"active":False},
{"name":"Pakistan","flag":"🇵🇰","code":"#PK","prefix":"+923","service":"WhatsApp","speed":5,"active":False},
{"name":"Vietnam","flag":"🇻🇳","code":"#VN","prefix":"+849","service":"TikTok","speed":5,"active":False}

]


def is_admin(user_id):
    return user_id == ADMIN_ID


def main_keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("⚡ Speed","📊 OTP Stats")
    kb.row("🌍 Countries","🔧 Service Edit")
    kb.row("▶ Start Generator","⏹ Stop Generator")

    return kb


def mask(prefix):
    return prefix + "***" + str(random.randint(100,999))


def generator():

    global otp_count

    while True:

        if running:

            active = [c for c in countries if c["active"]]

            if len(active)==0:
                time.sleep(2)
                continue

            c=random.choice(active)

            number=mask(c["prefix"])
            otp=random.randint(100000,999999)

            text=f"""
{c['flag']} {c['name']} {c['code']} 📱 {c['service']}

{number}

🔑 {otp}
"""

            keyboard=InlineKeyboardMarkup()

            keyboard.row(
            InlineKeyboardButton("📢 Main Channel",url="https://t.me/YOUR_CHANNEL"),
            InlineKeyboardButton("🤖 Number Bot",url="https://t.me/numberfast12_bot")
            )

            try:
                bot.send_message(GROUP_ID,text,reply_markup=keyboard)
                otp_count+=1
            except:
                pass

            time.sleep(c["speed"])

        else:
            time.sleep(2)


threading.Thread(target=generator,daemon=True).start()


@bot.message_handler(commands=['start'])
def start(msg):

    if not is_admin(msg.from_user.id):
        return

    bot.send_message(msg.chat.id,"🤖 OTP BOT READY",reply_markup=main_keyboard())


@bot.message_handler(func=lambda m: True)
def panel(message):

    global running

    if not is_admin(message.from_user.id):
        return


    if message.text=="📊 OTP Stats":
        bot.send_message(message.chat.id,f"📊 OTP Generated : {otp_count}")


    elif message.text=="▶ Start Generator":
        running=True
        bot.send_message(message.chat.id,"✅ Generator Started")


    elif message.text=="⏹ Stop Generator":
        running=False
        bot.send_message(message.chat.id,"🛑 Generator Stopped")


    elif message.text=="🌍 Countries":

        keyboard=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            status="✅" if c["active"] else "❌"

            keyboard.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']} {status}",
            callback_data=f"toggle_{i}"
            )
            )

        bot.send_message(message.chat.id,"🌍 Country Manager",reply_markup=keyboard)


    elif message.text=="🔧 Service Edit":

        keyboard=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            keyboard.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"servicecountry_{i}"
            )
            )

        bot.send_message(message.chat.id,"🔧 Select Country",reply_markup=keyboard)


    elif message.text=="⚡ Speed":

        keyboard=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            keyboard.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"speedcountry_{i}"
            )
            )

        bot.send_message(message.chat.id,"⚡ Select Country",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def toggle(call):

    i=int(call.data.split("_")[1])

    countries[i]["active"]=not countries[i]["active"]

    bot.answer_callback_query(call.id,f"{countries[i]['name']} toggled")


@bot.callback_query_handler(func=lambda call: call.data.startswith("servicecountry_"))
def service_country(call):

    i=int(call.data.split("_")[1])

    keyboard=InlineKeyboardMarkup()

    for s in services:

        keyboard.row(
        InlineKeyboardButton(
        s,
        callback_data=f"setservice_{i}_{s}"
        )
        )

    bot.edit_message_text(
    f"📱 Select Service for {countries[i]['name']}",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("setservice_"))
def set_service(call):

    data=call.data.split("_")

    i=int(data[1])
    s=data[2]

    countries[i]["service"]=s

    bot.answer_callback_query(call.id,f"{countries[i]['name']} → {s}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("speedcountry_"))
def speed_country(call):

    i=int(call.data.split("_")[1])

    keyboard=InlineKeyboardMarkup()

    for name,val in speed_options.items():

        keyboard.row(
        InlineKeyboardButton(
        name,
        callback_data=f"setspeed_{i}_{val}"
        )
        )

    bot.edit_message_text(
    f"⚡ Set Speed for {countries[i]['name']}",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("setspeed_"))
def set_speed(call):

    data=call.data.split("_")

    i=int(data[1])
    s=int(data[2])

    countries[i]["speed"]=s

    bot.answer_callback_query(call.id,f"{countries[i]['name']} speed set to {s}s")


print("BOT RUNNING...")
bot.infinity_polling()
