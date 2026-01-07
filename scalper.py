

import pandas as pd
import pandas_ta as ta
import requests
import time

# --- CONFIGURATION ---
COIN_ID = 'solana'  # CoinGecko uses IDs, not symbols (e.g., 'bitcoin', 'ethereum')
VS_CURRENCY = 'usd'
TELEGRAM_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
CHAT_ID = '5665906172'

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except:
        pass

def fetch_coingecko_ohlc(coin_id):
    # Fetch OHLC data (1-minute equivalent is not available via free REST, 
    # so we use the 30-minute/1-hour window for trend and 'simple/price' for scalp entry)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency={VS_CURRENCY}&days=1"
    response = requests.get(url)
    if response.status_code == 200:
        # Data format: [timestamp, open, high, low, close]
        df = pd.DataFrame(response.json(), columns=['ts', 'o', 'h', 'l', 'c'])
        return df
    elif response.status_code == 429:
        print("Rate limit hit! Sleeping...")
        time.sleep(60)
    return None

def analyze_strategy():
    df = fetch_coingecko_ohlc(COIN_ID)
    if df is None: return None
    
    # Technical Indicators
    df['rsi'] = ta.rsi(df['c'], length=14)
    bbands = ta.bbands(df['c'], length=20, std=2)
    
    # Explicitly map BBands to avoid KeyErrors
    df['lower_band'] = bbands['BBL_20_2.0']
    df['upper_band'] = bbands['BBU_20_2.0']
    
    last = df.iloc[-1]
    
    # Strategy Logic: Mean Reversion
    if last['c'] <= last['lower_band'] and last['rsi'] < 35:
        return f"🟢 GECKO BUY: {COIN_ID.upper()} at ${last['c']} (Oversold)"
    elif last['c'] >= last['upper_band'] or last['rsi'] > 65:
        return f"🔴 GECKO EXIT: {COIN_ID.upper()} at ${last['c']} (Overbought)"
    return None

print("Bot shifted to CoinGecko. Starting...")

while True:
    try:
        signal = analyze_strategy()
        if signal:
            print(signal)
            send_telegram(signal)
        
        # CoinGecko free tier updates every 60s for price data
        time.sleep(60) 
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(30)
