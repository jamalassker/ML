
import ccxt
import pandas as pd
import pandas_ta as ta
import requests
import time

# --- CONFIGURATION ---
# Using the standard exchange class but with optimized timing
exchange = ccxt.binance({
    'enableRateLimit': True, 
})
symbol = 'SOL/USDT'
TELEGRAM_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
CHAT_ID = '5665906172'

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except:
        pass

def fetch_and_analyze():
    # Increase limit to ensure BBands have enough data to calculate
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
    df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
    
    # FIX: Calculate Bollinger Bands
    # Explicitly naming the columns to avoid the 'BBU_20_2.0' Key Error
    bb = ta.bbands(df['c'], length=20, std=2)
    df['lower_band'] = bb['BBL_20_2.0']
    df['upper_band'] = bb['BBU_20_2.0']
    df['rsi'] = ta.rsi(df['c'], length=14)
    
    last = df.iloc[-1]
    
    # LOGIC
    if last['rsi'] < 30 and last['c'] < last['lower_band']:
        return f"🟢 BUY {symbol} @ {last['c']}"
    elif last['rsi'] > 70 or last['c'] > last['upper_band']:
        return f"🔴 SELL {symbol} @ {last['c']}"
    return None

print("Bot is live and rate-limit optimized...")

while True:
    try:
        signal = fetch_and_analyze()
        if signal:
            send_telegram(signal)
        
        # FIX: Sleep for 60 seconds to match the 1m candle and avoid IP ban
        time.sleep(60) 
    except Exception as e:
        print(f"Error: {e}")
        # If banned, sleep longer to let the IP clear
        time.sleep(30)
