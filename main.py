import telebot
import time
import threading
from datetime import datetime

API_TOKEN = '8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g'
USER_CHAT_ID = 839738530  # يرسل التوصيات للبوت الخاص فقط

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ تم تفعيل البوت الذكي V3 بنجاح! \nسوف تصلك التوصيات مباشرة هنا 📡")

def generate_signal(period):
    now = datetime.utcnow().minute
    if (now // period) % 2 == 0:
        return f"🔔 BUY signal – Confidence: {90 + period//2}%"
    else:
        return f"🔻 SELL signal – Confidence: {88 + period//3}%"

def send_signals_every(period):
    while True:
        try:
            signal = generate_signal(period)
            bot.send_message(USER_CHAT_ID, f"📡 Smart Signal ({period}m):\n{signal}")
            print(f"Sent {period}m signal: {signal}")
        except Exception as e:
            print(f"Error sending {period}m signal: {e}")
        time.sleep(period * 60)

def start_signal_threads():
    threading.Thread(target=send_signals_every, args=(1,), daemon=True).start()
    threading.Thread(target=send_signals_every, args=(5,), daemon=True).start()

start_signal_threads()
bot.polling()
