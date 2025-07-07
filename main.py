
# Telegram Bot Script - For Real Trading Recommendations

import telegram
from telegram.ext import Updater, CommandHandler
import logging

# Bot token (replace with actual token securely)
TOKEN = "8061215565:AAGpobcJor03wow2SmoVYN48RnF9UBet62g"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("✅ تم تفعيل البوت الذكي بنجاح!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# الأزواج المدعومة (تحويل أسماء Yahoo Finance)
pairs = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X",
    "NZDUSD": "NZDUSD=X"
}

# تحليل كل زوج
def analyze_pair(pair_name, yf_symbol):
    try:
        df = yf.download(tickers=yf_symbol, interval="1m", period="1d")
        df.dropna(inplace=True)

        df["rsi"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
        macd = ta.trend.MACD(df["Close"])
        df["macd_diff"] = macd.macd_diff()
        df["ema_fast"] = ta.trend.EMAIndicator(df["Close"], window=5).ema_indicator()
        df["ema_slow"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
        df["fractal_up"] = df["High"][(df["High"].shift(1) < df["High"]) & (df["High"].shift(-1) < df["High"])]
        df["fractal_down"] = df["Low"][(df["Low"].shift(1) > df["Low"]) & (df["Low"].shift(-1) > df["Low"])]

        last = df.iloc[-1]
        score = 0
        analysis = []

        if last["rsi"] < 30:
            score += 1
            analysis.append("RSI تشبع بيعي")
        elif last["rsi"] > 70:
            score += 1
            analysis.append("RSI تشبع شرائي")

        if last["macd_diff"] > 0:
            score += 1
            analysis.append("MACD إيجابي")
        elif last["macd_diff"] < 0:
            score += 1
            analysis.append("MACD سلبي")

        if last["ema_fast"] > last["ema_slow"]:
            score += 1
            analysis.append("تقاطع EMA صاعد")
        else:
            score += 0

        confidence = int((score / 3) * 100)
        if confidence >= 90:
            direction = "شراء (CALL)" if last["ema_fast"] > last["ema_slow"] else "بيع (PUT)"
            signal = f"📡 توصية حقيقية ✅\nزوج: {pair_name}\nنوع: {direction}\nالفترة: 1m\nنسبة الثقة: {confidence}%\nالتحليل: {' + '.join(analysis)}\nالوقت: {time.strftime('%H:%M')}"
            for user in chat_usernames:
                bot.send_message(chat_id=user, text=signal)

    except Exception as e:
        print(f"خطأ في {pair_name}: {e}")

# حلقة التوصيات المستمرة
while True:
    for pair, symbol in pairs.items():
        analyze_pair(pair, symbol)
        time.sleep(5)  # راحة بسيطة بين الأزواج
    time.sleep(60)  # التكرار كل دقيقة
