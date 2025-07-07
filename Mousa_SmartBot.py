import logging
import yfinance as yf
import pandas as pd
import ta
import time
from telegram import Bot
import os

# إعداد التوكن واسم البوت من المتغيرات البيئية أو بشكل مباشر
TOKEN = "8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g"
bot = Bot(token=TOKEN)

# قائمة الأزواج المطلوبة
symbols = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "NZDUSD=X", "USDCHF=X", "BTC-USD", "ETH-USD"]

# تحليل الذكاء الاصطناعي البسيط: فلترة باستخدام RSI و MACD والدعم والمقاومة
def analyze(symbol):
    try:
        data = yf.download(symbol, period="2d", interval="1m")
        if data.empty or len(data) < 10:
            return None

        df = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
        rsi = df["momentum_rsi"].iloc[-1]
        macd = df["trend_macd"].iloc[-1]
        signal = df["trend_macd_signal"].iloc[-1]
        support = df["Low"].rolling(window=10).min().iloc[-1]
        resistance = df["High"].rolling(window=10).max().iloc[-1]

        confidence = 0
        recommendation = "❕ انتظر"

        if rsi < 30 and macd > signal:
            confidence = 91
            recommendation = "✅ شراء"
        elif rsi > 70 and macd < signal:
            confidence = 92
            recommendation = "❌ بيع"
        elif (rsi > 40 and rsi < 60) and abs(macd - signal) < 0.1:
            confidence = 85
            recommendation = "⚠️ تذبذب"

        if confidence >= 90:
            message = f"🔔 توصية ذكية من البوت:\n"
            message += f"{signal}"
الزوج: {symbol.replace('=X','')}
RSI: {round(rsi,2)} | MACD: {round(macd,2)}
الدعم: {round(support,2)} | المقاومة: {round(resistance,2)}
📊 نسبة الثقة: {confidence}%
📈 {recommendation}"
            return message
        else:
            return None
    except:
        return None

# إرسال التوصيات تلقائيًا
while True:
    for symbol in symbols:
        result = analyze(symbol)
        if result:
            try:
                bot.send_message(chat_id='@Mousa_SmartBot', text=result)
            except Exception as e:
                print(f"Error sending message for {symbol}: {e}")
        time.sleep(2)
    time.sleep(60)
