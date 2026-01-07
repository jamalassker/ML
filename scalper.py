
import pandas as pd
import pandas_ta as ta
import requests
import time

# --- CONFIGURATION ---
COIN_ID = 'solana'   # CoinGecko coin ID
VS_CURRENCY = 'usd'

TELEGRAM_TOKEN = '8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA'
CHAT_ID = '5665906172'


def send_telegram(message):
    try:
        url = (
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
            f"/sendMessage?chat_id={CHAT_ID}&text={message}"
        )
        requests.get(url, timeout=5)
    except:
        pass


def fetch_coingecko_ohlc(coin_id):
    """
    Fetch OHLC data from CoinGecko
    Format returned: [timestamp, open, high, low, close]
    """
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        f"/ohlc?vs_currency={VS_CURRENCY}&days=1"
    )

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        df = pd.DataFrame(
            response.json(),
            columns=['ts', 'o', 'h', 'l', 'c']
        )
        return df

    elif response.status_code == 429:
        print("Rate limit hit! Sleeping...")
        time.sleep(60)

    return None


def analyze_strategy():
    df = fetch_coingecko_ohlc(COIN_ID)
    if df is None or df.empty:
        return None

    # --- INDICATORS ---
    df['rsi'] = ta.rsi(df['c'], length=14)

    bbands = ta.bbands(df['c'], length=20, std=2)

    if bbands is None or bbands.empty:
        return None

    # 🔥 FIX: auto-detect BB column names (version-safe)
    lower_col = [c for c in bbands.columns if c.startswith("BBL")][0]
    upper_col = [c for c in bbands.columns if c.startswith("BBU")][0]

    df['lower_band'] = bbands[lower_col]
    df['upper_band'] = bbands[upper_col]

    last = df.iloc[-1]

    # --- STRATEGY LOGIC (UNCHANGED) ---
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

        # CoinGecko free tier ~60s refresh
        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(30)
