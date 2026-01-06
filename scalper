import os
import time
import requests
import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.enums import *

# --- CONFIGURATION ---
API_KEY = 'Et7oRtg2CLHyaRGBoQOoTFt7LSixfav28k0bnVfcgzxd2KTal4xPlxZ9aO6sr1EJ'
API_SECRET = '2LfotApekUjBH6jScuzj1c47eEnq1ViXsNRIP4ydYqYWl6brLhU3JY4vqlftnUIo'
TG_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
TG_CHAT_ID = '5665906172'
# Top 20 Symbols from your list
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT'] # Add all 20 here
LEVERAGE = 20
QUANTITY_USD = 2.0  # $2 per trade to allow multiple open trades from $10

client = Client(API_KEY, API_SECRET)

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    requests.get(url)

def get_signals(symbol):
    # Fetch 1m candles
    bars = client.futures_klines(symbol=symbol, interval=KLINE_INTERVAL_1MINUTE, limit=100)
    df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'])
    df['close'] = df['close'].astype(float)
    
    # 2026 AI-Hybrid Indicators
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['vwap'] = ta.vwap(df['high'], df['low'], df['close'], df['vol'])
    ema_fast = ta.ema(df['close'], length=9)
    
    last_price = df['close'].iloc[-1]
    last_rsi = df['rsi'].iloc[-1]
    
    # Logic: Scalp when RSI is oversold + Price near VWAP (No-Deadlock)
    if last_rsi < 30 and last_price > df['vwap'].iloc[-1]:
        return 'BUY'
    elif last_rsi > 70 and last_price < df['vwap'].iloc[-1]:
        return 'SELL'
    return None

def monitor_trades():
    print("AI Scalper Active... Scanning Top 20 Symbols.")
    while True:
        for symbol in SYMBOLS:
            try:
                signal = get_signals(symbol)
                if signal:
                    # Logic to check if position already exists
                    pos = client.futures_position_information(symbol=symbol)
                    if float(pos[0]['positionAmt']) == 0:
                        print(f"Signal found for {symbol}: {signal}")
                        
                        # Execute Trade (Market Order)
                        # Note: In a real bot, calculate precise 'quantity' based on symbol decimals
                        # client.futures_create_order(symbol=symbol, side=signal, type='MARKET', quantity=...)
                        
                        msg = f"🚀 *AI TRADE OPENED*\nSymbol: {symbol}\nSide: {signal}\nLeverage: {LEVERAGE}x\nEst. PnL: Floating..."
                        send_telegram_msg(msg)
                        
            except Exception as e:
                print(f"Error on {symbol}: {e}")
        
        time.sleep(10) # Scan every 10 seconds for 1m high-frequency

if __name__ == "__main__":
    monitor_trades()
