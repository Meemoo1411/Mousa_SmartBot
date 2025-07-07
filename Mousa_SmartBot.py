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
        data = yf.download(symbol, period='2d', interval='5m')
        if data.empty:
            return None

        df = data.copy()
        df = ta.add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume")

        rsi = df["momentum_rsi"].iloc[-1]
        macd = df["trend_macd"].iloc[-1]
        support = df["Low"].rolling(window=5).min().iloc[-1]
        resistance = df["High"].rolling(window=5).max().iloc[-1]

        pair_name = symbol.replace('=X', '')

        recommendation = ""
        if rsi < 30 and macd < 0:
            recommendation = "شراء"
        elif rsi > 70 and macd > 0:
            recommendation = "بيع"
        else:
            recommendation = "انتظار"

        confidence = 90
        message = f"📉 توصية ذكية\nزوج: {pair_name}\nRSI: {round(rsi,2)} | MACD: {round(macd,2)}\nالدعم: {round(support,2)} | المقاومة: {round(resistance,2)}\nنسبة الثقة: {confidence}%\nالتوصية: {recommendation}"
زوج: {pair_name}
نسبة الثقة: {confidence}%
RSI: {round(rsi, 2)} | MACD: {round(macd, 2)}
الدعم: {round(support, 2)} | المقاومة: {round(resistance, 2)}
message = f"التوصية: {recommendation}"

        return message

    except Exception as e:
        logging.error(f"خطأ في التحليل لزوج {symbol}: {e}")
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
