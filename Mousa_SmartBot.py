
import os
import time
import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from signals import generate_signal

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("BOT_USERNAME")

bot = Bot(token=TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ بوت التوصيات شغال بنجاح!")

def send_signal(context):
    signal = generate_signal()
    if signal:
        context.bot.send_message(chat_id=update.job.context, text=signal)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    job_queue = updater.job_queue
    chat_id = os.getenv("USER_CHAT_ID")  # أو عيّنه يدويًا للتجربة
    if chat_id:
        job_queue.run_repeating(send_signal, interval=60, first=5, context=chat_id)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
