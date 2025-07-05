import telebot
import time
from datetime import datetime

API_TOKEN = '8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g'
GROUP_CHAT_ID = '@Mousa_SmartBot_Group'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ تم تفعيل البوت الذكي بنجاح!")

def generate_signal():
    now = datetime.utcnow().minute
    if now % 2 == 0:
        return "🔔 BUY signal - Confidence: 94%"
    else:
        return "🔻 SELL signal - Confidence: 91%"

def send_signals():
    while True:
        signal = generate_signal()
        bot.send_message(GROUP_CHAT_ID, f"📡 Smart Signal:\n{signal}")
        time.sleep(60)

import threading
threading.Thread(target=send_signals).start()

bot.polling()
