import ccxt
import ccxt.pro as ccxtpro
import pandas as pd
import pandas_ta as ta
import numpy as np
import requests
import asyncio
import math
import os
import joblib
from datetime import datetime, time as dtime

# ================= CONFIG =================
SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
TIMEFRAME = "1m"
CANDLES = 600

INITIAL_BALANCE = 1000.0
RISK_PER_TRADE = 0.01
MAX_OPEN_TRADES = 5
MAX_TRADE_MINUTES = 15
MAX_DRAWDOWN = 0.15

TAKER_FEE = 0.0004
SLIPPAGE = 0.0002

AI_PROB_THRESHOLD = 0.62
IMBALANCE_THRESHOLD = 0.15

SESSIONS = [
    (dtime(7, 0), dtime(11, 0)),   # London
    (dtime(13, 0), dtime(17, 0))  # NY
]

# Telegram
TG_TOKEN = os.getenv("TELEGRAM_TOKEN","8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA")
TG_CHAT = os.getenv("TELEGRAM_CHAT_ID","5665906172")


# ML Models (pretrained)
ML_FILTER_MODEL_PATH = "ml_filter_model.pkl"      # Logistic/XGBoost trained offline
LSTM_MODEL_PATH = "lstm_predictor.pkl"           # Pretrained LSTM model

ml_filter_model = joblib.load(ML_FILTER_MODEL_PATH)
lstm_model = joblib.load(LSTM_MODEL_PATH)

# ================= TELEGRAM =================
def tg(msg):
    if TG_TOKEN and TG_CHAT:
        requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT, "text": msg}
        )

# ================= EXCHANGE =================
exchange = ccxtpro.binanceusdm({"enableRateLimit": True})

# ================= UTIL =================
def in_session():
    now = datetime.utcnow().time()
    return any(s <= now <= e for s, e in SESSIONS)

def indicators(df):
    df["ema20"] = ta.ema(df["close"], 20)
    df["ema50"] = ta.ema(df["close"], 50)
    df["ema200"] = ta.ema(df["close"], 200)
    df["rsi"] = ta.rsi(df["close"], 14)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], 14)
    df["z"] = (df["close"] - df["close"].rolling(20).mean()) / df["close"].rolling(20).std()
    return df.dropna()

def regime(r):
    if r["ema20"] > r["ema50"] > r["ema200"]:
        return "UP"
    if r["ema20"] < r["ema50"] < r["ema200"]:
        return "DOWN"
    return "RANGE"

# ================= ORDERBOOK =================
async def orderbook_imbalance(symbol):
    ob = await exchange.watch_order_book(symbol)
    bid = sum(b[1] for b in ob["bids"][:10])
    ask = sum(a[1] for a in ob["asks"][:10])
    return (bid - ask) / (bid + ask)

# ================= AI PROBABILITY =================
def ai_probability(r, bias):
    base = (
        1.5 * min(abs(r["z"]) / 3, 1) +
        1.2 * abs(50 - r["rsi"]) / 50 +
        abs(r["ema20"] - r["ema200"]) / r["close"]
    )
    return 1 / (1 + math.exp(-(base + bias)))

# ================= ML FILTER =================
def ml_filter(df):
    features = df[["open","high","low","close","rsi","atr","z"]].values[-20:].flatten()
    prob = ml_filter_model.predict_proba([features])[0][1]
    return prob

# ================= LSTM PREDICTOR =================
def lstm_predict(df):
    seq = df[["open","high","low","close","rsi","atr","z"]].values[-30:]
    prob = lstm_model.predict(seq.reshape(1,30,7))[0][0]
    return prob

# ================= OPTIMIZER =================
def optimize(df):
    best = {"score": -999}
    for rsi in [28, 30, 32]:
        for sl in [1.1, 1.2, 1.3]:
            for tp in [1.8, 2.0, 2.2]:
                pnl = 0
                for _, r in df.iterrows():
                    if r["rsi"] < rsi and r["z"] < -1:
                        pnl += tp - sl
                if pnl > best["score"]:
                    best = {"rsi": rsi, "sl": sl, "tp": tp, "score": pnl}
    return best

# ================= MAIN =================
async def run():
    balance = INITIAL_BALANCE
    peak = balance
    open_trades = []
    bias = 0.0
    params = {}

    tg("🤖 AI 1m Scalper v2 Started")

    # Optimize per coin
    for s in SYMBOLS:
        ohlc = await exchange.fetch_ohlcv(s, TIMEFRAME, limit=500)
        df = indicators(pd.DataFrame(ohlc, columns=["ts","open","high","low","close","volume"]))
        params[s] = optimize(df)
        tg(f"⚙ {s} params {params[s]}")

    while True:
        if not in_session():
            await asyncio.sleep(10)
            continue

        for s in SYMBOLS:
            candles = await exchange.watch_ohlcv(s, TIMEFRAME, limit=CANDLES)
            df = indicators(pd.DataFrame(candles, columns=["ts","open","high","low","close","volume"]))
            r = df.iloc[-1]

            # Drawdown guard
            peak = max(peak, balance)
            if (peak - balance) / peak > MAX_DRAWDOWN:
                tg("🛑 Max drawdown reached. Trading halted.")
                return

            imbalance = await orderbook_imbalance(s)
            prob_ai = ai_probability(r, bias)
            prob_ml = ml_filter(df)
            prob_lstm = lstm_predict(df)
            combined_prob = (prob_ai + prob_ml + prob_lstm) / 3

            p = params[s]

            # Manage trades
            for t in open_trades[:]:
                age = (datetime.utcnow() - t["time"]).seconds / 60
                if r["low"] <= t["sl"]:
                    loss = balance * RISK_PER_TRADE
                    loss += loss * TAKER_FEE
                    balance -= loss
                    bias -= 0.1
                    open_trades.remove(t)
                    tg(f"❌ SL {t['symbol']} | Bal {round(balance,2)}")

                elif r["high"] >= t["tp"]:
                    gain = balance * RISK_PER_TRADE * 2
                    gain -= gain * TAKER_FEE
                    balance += gain
                    bias += 0.1
                    open_trades.remove(t)
                    tg(f"✅ TP {t['symbol']} | Bal {round(balance,2)}")

                elif age > MAX_TRADE_MINUTES:
                    open_trades.remove(t)
                    tg(f"⏱ Exit timeout {t['symbol']}")

            # ENTRY
            if (
                len(open_trades) < MAX_OPEN_TRADES
                and regime(r) == "UP"
                and combined_prob > AI_PROB_THRESHOLD
                and imbalance > IMBALANCE_THRESHOLD
                and r["rsi"] < p["rsi"]
                and r["z"] < -1
                and r["atr"] > df["atr"].mean()
            ):
                entry = r["close"] * (1 + SLIPPAGE)
                open_trades.append({
                    "symbol": s,
                    "sl": entry - r["atr"] * p["sl"],
                    "tp": entry + r["atr"] * p["tp"],
                    "time": datetime.utcnow()
                })
                tg(f"📈 BUY {s} | CombinedProb {round(combined_prob,2)}")

        await asyncio.sleep(1)

# ================= START =================
asyncio.run(run())
