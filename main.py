import telebot
import random
import time
import threading
from telebot.types import *

TOKEN = "8253626154:AAGWBaV4GXs6klQDYAnwn1NdDcD1b02fbAk"
GROUP_ID = -1003549378995
ADMIN_ID = 8626918981

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

speed = 3
running = True
otp_count = 0

services = [
"Facebook","Telegram","WhatsApp","TikTok","Google",
"Instagram","Twitter","Snapchat","Messenger","Gmail",
"Amazon","Discord","LinkedIn","YouTube","ChatGPT"
]

countries = [

{"name":"Bangladesh","flag":"🇧🇩","code":"#BD","prefix":"+88019","active":True},
{"name":"Nepal","flag":"🇳🇵","code":"#NP","prefix":"+97798","active":True},
{"name":"Germany","flag":"🇩🇪","code":"#DE","prefix":"+4915","active":True},
{"name":"USA","flag":"🇺🇸","code":"#US","prefix":"+1201","active":True},
{"name":"Afghanistan","flag":"🇦🇫","code":"#AF","prefix":"+937","active":True},
{"name":"Italy","flag":"🇮🇹","code":"#IT","prefix":"+39347","active":True},
{"name":"Saudi Arabia","flag":"🇸🇦","code":"#SA","prefix":"+9665","active":True},
{"name":"Vietnam","flag":"🇻🇳","code":"#VN","prefix":"+849","active":True},
{"name":"Pakistan","flag":"🇵🇰","code":"#PK","prefix":"+923","active":True},
{"name":"Kuwait","flag":"🇰🇼","code":"#KW","prefix":"+965","active":True}

]

def is_admin(user_id):
    return user_id == ADMIN_ID


def main_keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("⚡ Speed","📊 OTP Stats")
    kb.row("🌍 Countries","🛠 Service Edit")
    kb.row("▶ Start Generator","⏹ Stop Generator")

    return kb


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

            service=random.choice(services)

            if service=="Telegram":
                otp=random.randint(10000,99999)
            else:
                otp=random.randint(100000,999999)

            text=f"""
{c['flag']} {c['name']} {c['code']} 📱 {service}

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

        time.sleep(speed)


threading.Thread(target=generator, daemon=True).start()


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

    if message.text=="⚡ Speed":

        bot.send_message(message.chat.id,f"⚡ Current Speed : {speed} sec")


    elif message.text=="📊 OTP Stats":

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


    elif message.text=="🛠 Service Edit":

        keyboard=InlineKeyboardMarkup(row_width=2)

        for i,c in enumerate(countries):

            keyboard.add(
            InlineKeyboardButton(
            f"{c['flag']} {c['name']}",
            callback_data=f"service_{i}"
            )
            )

        bot.send_message(message.chat.id,"🛠 Select Country",reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def toggle(call):

    if call.from_user.id != ADMIN_ID:
        return

    i=int(call.data.split("_")[1])

    countries[i]["active"]=not countries[i]["active"]

    status="ON" if countries[i]["active"] else "OFF"

    bot.answer_callback_query(call.id,f"{countries[i]['name']} {status}")



@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def service_country(call):

    i=int(call.data.split("_")[1])

    keyboard=InlineKeyboardMarkup(row_width=2)

    for s in services:

        keyboard.add(
        InlineKeyboardButton(
        s,
        callback_data=f"setservice_{i}_{s}"
        )
        )

    bot.edit_message_text(
    f"{countries[i]['flag']} {countries[i]['name']} Select Service",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=keyboard
    )



@bot.callback_query_handler(func=lambda call: call.data.startswith("setservice_"))
def set_service(call):

    data=call.data.split("_")

    i=int(data[1])
    service=data[2]

    bot.answer_callback_query(call.id,f"{countries[i]['name']} → {service}")


print("BOT RUNNING...")
bot.infinity_polling()
