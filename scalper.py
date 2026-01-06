import time
import requests
import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.enums import *

# --- CREDENTIALS ---
API_KEY = 'Et7oRtg2CLHyaRGBoQOoTFt7LSixfav28k0bnVfcgzxd2KTal4xPlxZ9aO6sr1EJ'
API_SECRET = '2LfotApekUjBH6jScuzj1c47eEnq1ViXsNRIP4ydYqYWl6brLhU3JY4vqlftnUIo'
TG_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
TG_CHAT_ID = '5665906172'

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'AVAXUSDT', 'TRXUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT', 'LTCUSDT', 'SHIBUSDT', 'BCHUSDT', 'UNIUSDT', 'NEARUSDT', 'APTUSDT', 'OPUSDT', 'SUIUSDT']
LEVERAGE = 20
MARGIN_PER_TRADE = 2.0  # From your $10 total

client = Client(API_KEY, API_SECRET)

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={requests.utils.quote(msg)}&parse_mode=Markdown"
        requests.get(url, timeout=5)
    except: pass

def get_precision(symbol):
    # Dynamic precision handling for 2026 Binance API
    info = client.futures_exchange_info()
    for s in info['symbols']:
        if s['symbol'] == symbol:
            return int(s['quantityPrecision']), int(s['pricePrecision'])
    return 3, 2

def get_signals(symbol):
    bars = client.futures_klines(symbol=symbol, interval='1m', limit=50)
    df = pd.DataFrame(bars, columns=['time','open','high','low','close','vol','ct','qa','nt','tb','tq','i'])
    df['close'] = df['close'].astype(float)
    
    # 2026 AI Scalp Logic: RSI + VWAP + ATR Volatility
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['vwap'] = ta.vwap(df['high'].astype(float), df['low'].astype(float), df['close'], df['vol'].astype(float))
    
    curr = df.iloc[-1]
    if curr['rsi'] < 32 and curr['close'] > curr['vwap']: return 'BUY', curr['close']
    if curr['rsi'] > 68 and curr['close'] < curr['vwap']: return 'SELL', curr['close']
    return None, None

def manage_positions():
    # Fetch all floating trades
    positions = client.futures_position_information()
    for pos in positions:
        symbol = pos['symbol']
        amt = float(pos['positionAmt'])
        if amt != 0 and symbol in SYMBOLS:
            unrealized = float(pos['unRealizedProfit'])
            entry = float(pos['entryPrice'])
            
            # Detailed Telegram Update for Floating Trades
            status = "💹" if unrealized > 0 else "🚨"
            update = f"{status} *FLOATING TRADE*\n{symbol}: ${str(round(unrealized, 2))}\nEntry: {str(entry)}"
            
            # AUTO-EXIT: Profit at +10% ($0.20) or Loss at -5% ($0.10)
            if unrealized >= 0.20 or unrealized <= -0.10:
                side = SIDE_SELL if amt > 0 else SIDE_BUY
                client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=abs(amt), reduceOnly=True)
                send_telegram(f"🏁 *TRADE CLOSED*\n{symbol}\nResult: ${str(round(unrealized, 2))}")

def run_bot():
    send_telegram("🚀 AI Scalper v2026 Online\nMonitoring Top 20 Symbols...")
    while True:
        manage_positions()
        for symbol in SYMBOLS:
            try:
                sig, price = get_signals(symbol)
                if sig:
                    # Check if already in a trade
                    pos = client.futures_position_information(symbol=symbol)
                    if float(pos[0]['positionAmt']) == 0:
                        q_prec, p_prec = get_precision(symbol)
                        qty = round((MARGIN_PER_TRADE * LEVERAGE) / price, q_prec)
                        
                        client.futures_change_leverage(symbol=symbol, leverage=LEVERAGE)
                        client.futures_create_order(symbol=symbol, side=sig, type='MARKET', quantity=qty)
                        
                        send_telegram(f"⚡ *NEW TRADE*\n{symbol} | {sig}\nPrice: {str(price)}")
            except Exception as e:
                print(f"Error {symbol}: {str(e)}")
        time.sleep(15)

if __name__ == "__main__":
    run_bot()

