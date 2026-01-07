

import ccxt
import pandas as pd
import pandas_ta as ta
import requests
import time

# --- CONFIGURATION ---
exchange = ccxt.binance()
symbol = 'SOL/USDT'
TELEGRAM_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
CHAT_ID = '5665906172'

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def fetch_and_analyze():
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=50)
    df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
    
    # Strategy: RSI + Bollinger Bands (Best for $10 accounts)
    df['rsi'] = ta.rsi(df['c'], length=14)
    bbands = ta.bbands(df['c'], length=20, std=2)
    df = pd.concat([df, bbands], axis=1)
    
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Signal Logic
    if last['rsi'] < 30 and last['c'] < last['BBL_20_2.0']:
        return f"🟢 BUY SIGNAL: {symbol} at {last['c']}. RSI: {round(last['rsi'], 2)}"
    elif last['rsi'] > 70 or last['c'] > last['BBU_20_2.0']:
        return f"🔴 SELL/EXIT: {symbol} at {last['c']}. RSI: {round(last['rsi'], 2)}"
    return None

print("Bot is live...")
send_telegram("🚀 Scalper Bot Started on $10 Account")

while True:
    try:
        signal = fetch_and_analyze()
        if signal:
            print(signal)
            send_telegram(signal)
        time.sleep(60) # Wait for new 1m candle
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
