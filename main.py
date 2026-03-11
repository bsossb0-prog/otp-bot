import telebot
import random
import time
import threading
from telebot.types import *

TOKEN = "8253626154:AAGWBaV4GXs6klQDYAnwn1NdDcD1b02fbAk"
GROUP_ID = -100XXXXXXXXXX
ADMIN_ID = 123456789

bot = telebot.TeleBot(TOKEN)

speed = 3
running = False
otp_count = 0


countries = [

{"name":"Bangladesh","flag":"🇧🇩","code":"#BD","prefix":"+88019","service":"Facebook","active":True},
{"name":"Nepal","flag":"🇳🇵","code":"#NP","prefix":"+97798","service":"WhatsApp","active":True},
{"name":"Germany","flag":"🇩🇪","code":"#DE","prefix":"+4915","service":"Telegram","active":True},
{"name":"USA","flag":"🇺🇸","code":"#US","prefix":"+1201","service":"Telegram","active":True},
{"name":"Italy","flag":"🇮🇹","code":"#IT","prefix":"+39347","service":"Telegram","active":True},
{"name":"Pakistan","flag":"🇵🇰","code":"#PK","prefix":"+923","service":"WhatsApp","active":True}

]


def mask(prefix):

    a=random.randint(100,999)
    b=random.randint(1000,9999)

    return f"{prefix}{a}***{b}"


def generator():

    global otp_count

    while True:

        if running:

            active=[c for c in countries if c["active"]]

            if not active:
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
            InlineKeyboardButton("🤖 Number Bot",url="https://t.me/YOUR_BOT")
            )

            try:
                bot.send_message(GROUP_ID,text,reply_markup=keyboard)
                otp_count+=1
            except:
                pass

        time.sleep(speed)


threading.Thread(target=generator,daemon=True).start()


def admin_panel():

    kb=InlineKeyboardMarkup()

    kb.row(
    InlineKeyboardButton("▶ Start",callback_data="start"),
    InlineKeyboardButton("⏹ Stop",callback_data="stop")
    )

    kb.row(
    InlineKeyboardButton("⚡ Speed",callback_data="speed"),
    InlineKeyboardButton("📊 Dashboard",callback_data="stats")
    )

    return kb


@bot.message_handler(commands=['start'])
def start(msg):

    if msg.from_user.id != ADMIN_ID:
        return

    bot.send_message(msg.chat.id,"🤖 BOT READY",reply_markup=admin_panel())


@bot.message_handler(commands=['admin'])
def admin(msg):

    if msg.from_user.id != ADMIN_ID:
        return

    active=len([c for c in countries if c["active"]])

    text=f"""
🎛 OTP BOT ADMIN PANEL

📊 OTP Generated : {otp_count}
⚡ Speed : {speed}s
🌍 Active Countries : {active}
🟢 Generator : {"Running" if running else "Stopped"}
"""

    bot.send_message(msg.chat.id,text,reply_markup=admin_panel())


@bot.callback_query_handler(func=lambda call:True)
def callback(call):

    global running
    global speed

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id,"Admin Only")
        return


    if call.data=="start":

        running=True
        bot.answer_callback_query(call.id,"Generator Started")


    elif call.data=="stop":

        running=False
        bot.answer_callback_query(call.id,"Generator Stopped")


    elif call.data=="stats":

        active=len([c for c in countries if c["active"]])

        text=f"""
📊 OTP Generated : {otp_count}
⚡ Speed : {speed}s
🌍 Active Countries : {active}
🟢 Generator : {"Running" if running else "Stopped"}
"""

        bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_panel()
        )


    elif call.data=="speed":

        kb=InlineKeyboardMarkup()

        speeds=[1,3,4,5,6,7,8,9,10]

        for s in speeds:
            kb.add(InlineKeyboardButton(f"{s}s",callback_data=f"set_{s}"))

        bot.edit_message_text(
        "⚡ Select Speed",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
        )


    elif call.data.startswith("set_"):

        speed=int(call.data.split("_")[1])

        bot.answer_callback_query(call.id,f"Speed set to {speed}s")

        bot.edit_message_text(
        f"⚡ Speed Updated : {speed}s",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_panel()
        )


bot.infinity_polling()
