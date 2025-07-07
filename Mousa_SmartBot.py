import logging
import yfinance as yf
import pandas as pd
import ta
import time
from telegram import Bot
from datetime import datetime

# التوكن واسم البوت
TOKEN = "8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g"
CHAT_ID = "@Mousa_SmartBot"

# إعداد البوت والتسجيل
bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)

# دالة التحليل الفني الكامل
def analyze_pair(symbol):
    try:
        pair_name = symbol.replace('=X', '')

        # جلب البيانات
        df = yf.download(symbol, period='1d', interval='1m')
        if df is None or df.empty:
            return None

        # حساب المؤشرات
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        df['RSI'] = rsi

        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2

        recent = df.iloc[-1]
        support = df['Low'].rolling(window=20).min().iloc[-1]
        resistance = df['High'].rolling(window=20).max().iloc[-1]

        recommendation = "شراء" if (recent['MACD'] > 0 and recent['RSI'] < 70) else "بيع"
        confidence = 90 if recommendation == "شراء" else 85

        message = (
            f"تحليل زوج: {pair_name}\n"
            f"RSI: {round(recent['RSI'], 2)} | MACD: {round(recent['MACD'], 2)}\n"
            f"الدعم: {round(support, 2)} | المقاومة: {round(resistance, 2)}\n"
            f"التوصية: {recommendation} | نسبة الثقة: {confidence}%"
        )
        return message

    except Exception as e:
        print(f"❌ خطأ في التحليل للزوج {symbol}: {e}")
        return None

# قائمة الأزواج + OTC
symbols = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", "USDCAD=X", "AUDUSD=X", "NZDUSD=X",
    "EURGBP=X", "EURJPY=X", "GBPJPY=X", "EURCHF=X", "EURCAD=X", "GBPCAD=X", "AUDJPY=X",
    "NZDJPY=X", "USDHKD=X", "USDSEK=X", "USDNOK=X", "USDSGD=X"
]

# بدء إرسال التوصيات التلقائية
while True:
    for symbol in symbols:
        analysis = analyze_pair(symbol)
        if analysis:
            bot.send_message(chat_id=CHAT_ID, text=analysis)
            time.sleep(2)  # انتظار بسيط بين كل توصية

    time.sleep(60)  # إرسال كل دقيقة
