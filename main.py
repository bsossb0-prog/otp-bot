import telebot
import random
import time
import threading
from telebot.types import *

TOKEN = "8253626154:AAGWBaV4GXs6klQDYAnwn1NdDcD1b02fbAk"
GROUP_ID = -100XXXXXXXXX
ADMIN_ID = 123456789

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

{"name":"Bangladesh","flag":"🇧🇩","code":"#BD","prefix":"+88019","service":"Telegram","speed":2,"active":True},

{"name":"Italy","flag":"🇮🇹","code":"#IT","prefix":"+39347","service":"Facebook","speed":5,"active":False},

{"name":"USA","flag":"🇺🇸","code":"#US","prefix":"+1201","service":"Google","speed":5,"active":False},

{"name":"Pakistan","flag":"🇵🇰","code":"#PK","prefix":"+923","service":"WhatsApp","speed":5,"active":False},

{"name":"Vietnam","flag":"🇻🇳","code":"#VN","prefix":"+849","service":"TikTok","speed":5,"active":False}

]

def is_admin(uid):
    return uid == ADMIN_ID


def mask(prefix):
    return prefix + "***" + str(random.randint(100,999))


def main_menu():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("⚡ Speed","📊 OTP Stats")
    kb.row("🌍 Countries","🔧 Service Edit")
    kb.row("▶ Start Generator","⏹ Stop Generator")

    return kb


def generator():

    global otp_count

    while True:

        if running:

            active = [c for c in countries if c["active"]]

            if len(active) > 0:

                c = random.choice(active)

                number = mask(c["prefix"])

                if c["service"] == "Telegram":
                    otp = random.randint(10000,99999)
                else:
                    otp = random.randint(100000,999999)

                text=f"""
{c['flag']} {c['name']} {c['code']} 📱 {c['service']}

{number}

🔑 {otp}
"""

                keyboard=InlineKeyboardMarkup()

                keyboard.row(
                InlineKeyboardButton("📢 Main Channel",url="https://t.me/YOUR_CHANNEL"),
                InlineKeyboardButton("🤖 Number Bot",url="https://t.me/YOUR_BOT")
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
def start(m):

    if not is_admin(m.from_user.id):
        return

    bot.send_message(m.chat.id,"🤖 OTP BOT READY",reply_markup=main_menu())


@bot.message_handler(func=lambda m:True)
def panel(m):

    global running

    if not is_admin(m.from_user.id):
        return


    if m.text=="📊 OTP Stats":

        bot.send_message(m.chat.id,f"📊 OTP Generated : {otp_count}")


    elif m.text=="▶ Start Generator":

        running=True
        bot.send_message(m.chat.id,"✅ Generator Started")


    elif m.text=="⏹ Stop Generator":

        running=False
        bot.send_message(m.chat.id,"🛑 Generator Stopped")


    elif m.text=="🌍 Countries":

        kb=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            status="✅" if c["active"] else "❌"

            kb.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']} {status}",
            callback_data=f"toggle_{i}"
            )
            )

        bot.send_message(m.chat.id,"🌍 Country Manager",reply_markup=kb)


    elif m.text=="🔧 Service Edit":

        kb=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            kb.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"service_{i}"
            )
            )

        bot.send_message(m.chat.id,"🔧 Select Country",reply_markup=kb)


    elif m.text=="⚡ Speed":

        kb=InlineKeyboardMarkup()

        for i,c in enumerate(countries):

            kb.row(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"speed_{i}"
            )
            )

        bot.send_message(m.chat.id,"⚡ Select Country",reply_markup=kb)


@bot.callback_query_handler(func=lambda call:call.data.startswith("toggle_"))
def toggle(call):

    i=int(call.data.split("_")[1])

    countries[i]["active"]=not countries[i]["active"]

    bot.answer_callback_query(call.id,"Updated")


@bot.callback_query_handler(func=lambda call:call.data.startswith("service_"))
def service_select(call):

    i=int(call.data.split("_")[1])

    kb=InlineKeyboardMarkup()

    for s in services:

        kb.row(
        InlineKeyboardButton(
        s,
        callback_data=f"setservice_{i}_{s}"
        )
        )

    bot.edit_message_text(
    f"📱 Select Service for {countries[i]['name']}",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call:call.data.startswith("setservice_"))
def set_service(call):

    data=call.data.split("_")

    i=int(data[1])
    s=data[2]

    countries[i]["service"]=s

    bot.answer_callback_query(call.id,f"{countries[i]['name']} → {s}")


@bot.callback_query_handler(func=lambda call:call.data.startswith("speed_"))
def speed_select(call):

    i=int(call.data.split("_")[1])

    kb=InlineKeyboardMarkup()

    for name,val in speed_options.items():

        kb.row(
        InlineKeyboardButton(
        name,
        callback_data=f"setspeed_{i}_{val}"
        )
        )

    bot.edit_message_text(
    f"⚡ Set Speed for {countries[i]['name']}",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call:call.data.startswith("setspeed_"))
def set_speed(call):

    data=call.data.split("_")

    i=int(data[1])
    s=int(data[2])

    countries[i]["speed"]=s

    bot.answer_callback_query(call.id,"Speed Updated")


print("BOT RUNNING...")
bot.infinity_polling()
