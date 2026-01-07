import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime, timedelta

# ================= CONFIG =================
SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "BNB/USDT",
    "XRP/USDT"
]

TIMEFRAME = "1m"
CANDLES = 1500
EXCHANGE = ccxt.binance({"enableRateLimit": True})

RISK_PER_TRADE = 0.01     # 1%
SL_ATR = 1.2              # stop-loss = 1.2 ATR
TP_ATR = 1.8              # take-profit = 1.8 ATR

# ================= DATA =================
def fetch_ohlc(symbol):
    ohlc = EXCHANGE.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=CANDLES)
    df = pd.DataFrame(
        ohlc,
        columns=["ts","open","high","low","close","volume"]
    )
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df

# ================= FEATURES =================
def compute_features(df):
    df["ema20"] = ta.ema(df["close"], 20)
    df["ema50"] = ta.ema(df["close"], 50)
    df["ema200"] = ta.ema(df["close"], 200)
    df["rsi"] = ta.rsi(df["close"], 14)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], 14)

    bb = ta.bbands(df["close"], length=20, std=2)
    l = [c for c in bb.columns if c.startswith("BBL")][0]
    u = [c for c in bb.columns if c.startswith("BBU")][0]

    df["bb_low"] = bb[l]
    df["bb_up"] = bb[u]

    # Z-score (AI/statistical technique)
    df["zscore"] = (df["close"] - df["close"].rolling(20).mean()) / df["close"].rolling(20).std()

    return df.dropna()

# ================= AI REGIME FILTER =================
def market_regime(row):
    if row["ema20"] > row["ema50"] > row["ema200"]:
        return "UP"
    if row["ema20"] < row["ema50"] < row["ema200"]:
        return "DOWN"
    return "RANGE"

# ================= SIGNAL LOGIC =================
def generate_signal(row):
    regime = market_regime(row)

    # AI rule: mean reversion ONLY in micro-trend
    if regime == "UP":
        if row["rsi"] < 35 and row["zscore"] < -1:
            return "BUY"

    if regime == "DOWN":
        if row["rsi"] > 65 and row["zscore"] > 1:
            return "SELL"

    return None

# ================= BACKTEST =================
def backtest(df):
    balance = 1.0
    wins = losses = 0

    for i in range(1, len(df)):
        row = df.iloc[i]
        signal = generate_signal(row)
        if not signal:
            continue

        atr = row["atr"]
        entry = row["close"]

        if signal == "BUY":
            sl = entry - atr * SL_ATR
            tp = entry + atr * TP_ATR

            future = df.iloc[i+1:i+20]
            for _, f in future.iterrows():
                if f["low"] <= sl:
                    balance -= RISK_PER_TRADE
                    losses += 1
                    break
                if f["high"] >= tp:
                    balance += RISK_PER_TRADE * (TP_ATR / SL_ATR)
                    wins += 1
                    break

        if signal == "SELL":
            sl = entry + atr * SL_ATR
            tp = entry - atr * TP_ATR

            future = df.iloc[i+1:i+20]
            for _, f in future.iterrows():
                if f["high"] >= sl:
                    balance -= RISK_PER_TRADE
                    losses += 1
                    break
                if f["low"] <= tp:
                    balance += RISK_PER_TRADE * (TP_ATR / SL_ATR)
                    wins += 1
                    break

    return {
        "trades": wins + losses,
        "wins": wins,
        "losses": losses,
        "winrate": round(wins / max(1, wins + losses) * 100, 2),
        "equity": round(balance, 3)
    }

# ================= RUN =================
if __name__ == "__main__":
    print("AI 1m Scalper | Backtest + Multi-Coin\n")

    for symbol in SYMBOLS:
        print(f"Testing {symbol}")
        df = fetch_ohlc(symbol)
        df = compute_features(df)
        stats = backtest(df)
        print(stats)
        print("-" * 40)
