import logging
import yfinance as yf
import pandas as pd
import ta
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("BOT_USERNAME")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Function to analyze and generate real signals
def analyze_pair(symbol):
    data = yf.download(symbol, period='2d', interval='5m')
    if data.empty:
        return f"لا توجد بيانات حالياً لـ {symbol}"
    df = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
    rsi = df["momentum_rsi"].iloc[-1]
    macd = df["trend_macd"].iloc[-1]
    support = df["Low"].rolling(window=5).min().iloc[-1]
    resistance = df["High"].rolling(window=5).max().iloc[-1]

    signal = f"""🔎 تحليل:
رمز الزوج: {symbol}
RSI: {round(rsi,2)}
MACD: {round(macd,2)}
الدعم: {round(support,2)} / المقاومة: {round(resistance,2)}
"""

    if rsi < 30 and macd < 0:
        signal += "✅ التوصية: شراء 🔼"
    elif rsi > 70 and macd > 0:
        signal += "❌ التوصية: بيع 🔽"
    else:
        signal += "⚠️ التوصية: انتظر إشارة أوضح"

    return signal

async def start(update, context):
    await update.message.reply_text("أهلاً بك في بوت التوصيات الذكية 🔍")
await update.message.reply_text("اكتب /signal EURUSD للحصول على توصية.")

async def signal(update, context):
    if context.args:
        symbol = context.args[0].upper()
        response = analyze_pair(symbol)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❗ يرجى كتابة اسم الزوج بعد الأمر، مثال: /signal EURUSD")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()
