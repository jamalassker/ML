import ccxt
import ccxt.pro as ccxtpro
import pandas as pd
import pandas_ta as ta
import numpy as np
import requests
import math
import os
import asyncio
from datetime import datetime, time as dtime

# ================= CONFIG =================
SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
TIMEFRAME = "1m"
CANDLES = 500

USE_TESTNET = False   # change to True later if needed

INITIAL_BALANCE = 1000.0
RISK_PER_TRADE = 0.01
MAX_OPEN_TRADES = 5
MAX_TRADE_MINUTES = 15

AI_PROB_THRESHOLD = 0.62
IMBALANCE_THRESHOLD = 0.15

SESSIONS = [
    (dtime(7, 0), dtime(11, 0)),
    (dtime(13, 0), dtime(17, 0))
]

# Telegram
TG_TOKEN = os.getenv("TELEGRAM_TOKEN","8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA")
TG_CHAT = os.getenv("TELEGRAM_CHAT_ID","5665906172")

# ================= TELEGRAM =================
def tg(msg):
    if not TG_TOKEN or not TG_CHAT:
        return
    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHAT, "text": msg}
    )

# ================= EXCHANGE =================
exchange = (
    ccxtpro.binanceusdm({"enableRateLimit": True})
    if not USE_TESTNET else
    ccxtpro.binanceusdm({
        "enableRateLimit": True,
        "urls": {"api": {"public": "https://testnet.binancefuture.com"}}
    })
)

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
    bid_vol = sum([b[1] for b in ob["bids"][:10]])
    ask_vol = sum([a[1] for a in ob["asks"][:10]])
    return (bid_vol - ask_vol) / (bid_vol + ask_vol)

# ================= AI PROBABILITY =================
def ai_probability(r, bias):
    base = (
        1.5 * min(abs(r["z"]) / 3, 1) +
        1.2 * abs(50 - r["rsi"]) / 50 +
        1.0 * abs(r["ema20"] - r["ema200"]) / r["close"]
    )
    return 1 / (1 + math.exp(-(base + bias)))

# ================= MAIN LOOP =================
async def run():
    balance = INITIAL_BALANCE
    open_trades = []
    reward_bias = 0.0

    tg("🤖 AI 1m Scalper Started")

    while True:
        if not in_session():
            await asyncio.sleep(10)
            continue

        for symbol in SYMBOLS:
            candles = await exchange.watch_ohlcv(symbol, TIMEFRAME, limit=CANDLES)
            df = pd.DataFrame(candles, columns=["ts","open","high","low","close","volume"])
            r = indicators(df).iloc[-1]

            imbalance = await orderbook_imbalance(symbol)
            prob = ai_probability(r, reward_bias)
            reg = regime(r)

            # MANAGE TRADES
            for t in open_trades[:]:
                age = (datetime.utcnow() - t["time"]).seconds / 60
                if age > MAX_TRADE_MINUTES:
                    open_trades.remove(t)
                    tg(f"⏱ Exit timeout {t['symbol']}")
                    reward_bias -= 0.05
                    continue

                if r["low"] <= t["sl"]:
                    balance -= balance * RISK_PER_TRADE
                    open_trades.remove(t)
                    reward_bias -= 0.1
                    tg(f"❌ SL {t['symbol']} | Bal {round(balance,2)}")

                elif r["high"] >= t["tp"]:
                    balance += balance * RISK_PER_TRADE * 2
                    open_trades.remove(t)
                    reward_bias += 0.1
                    tg(f"✅ TP {t['symbol']} | Bal {round(balance,2)}")

            # ENTRY
            if len(open_trades) >= MAX_OPEN_TRADES:
                continue

            if (
                reg == "UP"
                and prob >= AI_PROB_THRESHOLD
                and imbalance > IMBALANCE_THRESHOLD
                and r["rsi"] < 30
                and r["z"] < -1
            ):
                open_trades.append({
                    "symbol": symbol,
                    "sl": r["close"] - r["atr"] * 1.2,
                    "tp": r["close"] + r["atr"] * 2.0,
                    "time": datetime.utcnow()
                })
                tg(f"📈 BUY {symbol} | Prob {round(prob,2)} | Imb {round(imbalance,2)}")

        await asyncio.sleep(1)

# ================= START =================
asyncio.run(run())
