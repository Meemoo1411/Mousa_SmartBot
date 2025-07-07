
import pandas as pd
import ta

def calculate_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['fractal_up'] = df['high'][(df['high'].shift(2) < df['high'].shift(1)) & (df['high'].shift(1) > df['high'])]
    df['fractal_down'] = df['low'][(df['low'].shift(2) > df['low'].shift(1)) & (df['low'].shift(1) < df['low'])]
    return df
