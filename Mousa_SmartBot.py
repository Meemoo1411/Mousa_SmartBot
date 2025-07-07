import logging
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timedelta
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio

TOKEN = "8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g"
GROUP_ID = "@Mousa_SmartBot_Group"
PRIVATE_USERNAME = "@Mousa_SmartBot"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

bot = Bot(token=TOKEN)

symbol_list = [
    "EURUSD=X", "USDJPY=X", "GBPUSD=X", "USDCHF=X", "AUDUSD=X", "NZDUSD=X",
    "USDCAD=X", "EURJPY=X", "GBPJPY=X", "EURGBP=X", "EURCHF=X", "AUDJPY=X",
    "BTC-USD", "ETH-USD"
]

def analyze_pair(symbol):
    try:
        data = yf.download(symbol, period="2d", interval="1m")
        if data.empty or len(data) < 10:
            return None

        df = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")

        rsi = df["momentum_rsi"].iloc[-1]
        macd = df["trend_macd"].iloc[-1]
        support = df["Low"].rolling(window=5).min().iloc[-1]
        resistance = df["High"].rolling(window=5).max().iloc[-1]

        recommendation = ""
        confidence = 50

        if rsi < 30 and macd < 0:
            recommendation = "شراء"
            confidence = 92
        elif rsi > 70 and macd > 0:
            recommendation = "بيع"
            confidence = 93
        else:
            recommendation = "انتظار"
            confidence = 85

        if confidence < 90:
            return None

        now = datetime.utcnow() + timedelta(minutes=1)
        time_str = now.strftime("%H:%M")

        symbol_clean = symbol.replace("=X", "").replace("-USD", "/USD")
        msg = f"""📡 توصية تلقائية
زوج: {symbol_clean}
الوقت المناسب للدخول: {time_str}
RSI: {round(rsi, 2)} | MACD: {round(macd, 2)}
الدعم: {round(support, 4)} | المقاومة: {round(resistance, 4)}
القرار: {recommendation}
نسبة الثقة: {confidence}% ✅"""

        return msg
    except Exception as e:
        print(f"خطأ في {symbol}: {e}")
        return None

async def send_signals():
    while True:
        for symbol in symbol_list:
            signal = analyze_pair(symbol)
            if signal:
                try:
                    await bot.send_message(chat_id=GROUP_ID, text=signal)
                    await bot.send_message(chat_id=PRIVATE_USERNAME, text=signal)
                    await asyncio.sleep(1)
                except Exception as e:
                    print("خطأ في الإرسال:", e)
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    asyncio.create_task(send_signals())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
