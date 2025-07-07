
import yfinance as yf
from indicators import calculate_indicators

def generate_signal(symbol='EURUSD=X'):
    data = yf.download(tickers=symbol, interval='1m', period='1d')
    if data.empty:
        return None

    data = calculate_indicators(data)
    last = data.iloc[-1]

    rsi_ok = last['rsi'] < 30 or last['rsi'] > 70
    macd_ok = last['macd'] > last['macd_signal']
    fractal_ok = not pd.isna(last['fractal_down']) or not pd.isna(last['fractal_up'])

    if rsi_ok and macd_ok and fractal_ok:
        direction = 'شراء 🔼' if last['macd'] > last['macd_signal'] else 'بيع 🔽'
        confidence = 95 if rsi_ok and macd_ok else 90
        return f"📢 توصية {direction}
الزوج: EUR/USD
الثقة: {confidence}%
المؤشرات: RSI + MACD + Fractal ✅"

    return None
