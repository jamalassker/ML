import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime, time as dtime
import time

# ================= CONFIG =================
SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]
TIMEFRAME = "1m"
CANDLES = 1500

EXCHANGE = ccxt.binance({"enableRateLimit": True})

INITIAL_BALANCE = 1000.0
RISK_PER_TRADE = 0.01   # 1%

# Optimization grids
RSI_BUY = [25, 30, 35]
RSI_SELL = [65, 70, 75]
SL_ATR_GRID = [1.0, 1.2, 1.5]
TP_ATR_GRID = [1.5, 1.8, 2.2]

# Trading sessions (UTC)
SESSIONS = [
    (dtime(7, 0), dtime(11, 0)),   # London
    (dtime(13, 0), dtime(17, 0))   # NY
]

# ================= UTIL =================
def in_session():
    now = datetime.utcnow().time()
    return any(start <= now <= end for start, end in SESSIONS)

def fetch_ohlc(symbol):
    ohlc = EXCHANGE.fetch_ohlcv(symbol, TIMEFRAME, limit=CANDLES)
    df = pd.DataFrame(
        ohlc, columns=["ts","open","high","low","close","volume"]
    )
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df

def indicators(df):
    df["ema20"] = ta.ema(df["close"], 20)
    df["ema50"] = ta.ema(df["close"], 50)
    df["ema200"] = ta.ema(df["close"], 200)
    df["rsi"] = ta.rsi(df["close"], 14)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], 14)

    bb = ta.bbands(df["close"], 20, 2)
    l = [c for c in bb.columns if c.startswith("BBL")][0]
    u = [c for c in bb.columns if c.startswith("BBU")][0]

    df["bb_low"] = bb[l]
    df["bb_up"] = bb[u]

    df["z"] = (
        (df["close"] - df["close"].rolling(20).mean())
        / df["close"].rolling(20).std()
    )
    return df.dropna()

def regime(row):
    if row["ema20"] > row["ema50"] > row["ema200"]:
        return "UP"
    if row["ema20"] < row["ema50"] < row["ema200"]:
        return "DOWN"
    return "RANGE"

# ================= BACKTEST =================
def backtest(df, rsi_b, rsi_s, sl_atr, tp_atr):
    balance = 1.0
    wins = losses = 0

    for i in range(1, len(df)-20):
        r = df.iloc[i]
        reg = regime(r)

        if reg == "UP" and r["rsi"] < rsi_b and r["z"] < -1:
            entry = r["close"]
            sl = entry - r["atr"] * sl_atr
            tp = entry + r["atr"] * tp_atr
            for _, f in df.iloc[i+1:i+20].iterrows():
                if f["low"] <= sl:
                    balance -= 1
                    losses += 1
                    break
                if f["high"] >= tp:
                    balance += tp_atr / sl_atr
                    wins += 1
                    break

        if reg == "DOWN" and r["rsi"] > rsi_s and r["z"] > 1:
            entry = r["close"]
            sl = entry + r["atr"] * sl_atr
            tp = entry - r["atr"] * tp_atr
            for _, f in df.iloc[i+1:i+20].iterrows():
                if f["high"] >= sl:
                    balance -= 1
                    losses += 1
                    break
                if f["low"] <= tp:
                    balance += tp_atr / sl_atr
                    wins += 1
                    break

    trades = wins + losses
    if trades == 0:
        return None

    return {
        "equity": balance,
        "winrate": wins / trades,
        "trades": trades
    }

# ================= OPTIMIZER =================
def optimize(symbol):
    df = indicators(fetch_ohlc(symbol))
    best = None

    for rb in RSI_BUY:
        for rs in RSI_SELL:
            for sl in SL_ATR_GRID:
                for tp in TP_ATR_GRID:
                    res = backtest(df, rb, rs, sl, tp)
                    if not res:
                        continue
                    if not best or res["equity"] > best["equity"]:
                        best = {
                            "symbol": symbol,
                            "rsi_b": rb,
                            "rsi_s": rs,
                            "sl": sl,
                            "tp": tp,
                            **res
                        }
    return best

# ================= LIVE PAPER =================
def live_trade(config):
    balance = INITIAL_BALANCE
    open_trade = None

    print(f"\n▶ LIVE PAPER TRADING {config['symbol']}")

    while True:
        if not in_session():
            time.sleep(30)
            continue

        df = indicators(fetch_ohlc(config["symbol"]))
        r = df.iloc[-1]

        if open_trade:
            if open_trade["side"] == "BUY":
                if r["low"] <= open_trade["sl"]:
                    balance -= balance * RISK_PER_TRADE
                    open_trade = None
                elif r["high"] >= open_trade["tp"]:
                    balance += balance * RISK_PER_TRADE * (config["tp"]/config["sl"])
                    open_trade = None

        else:
            reg = regime(r)
            if reg == "UP" and r["rsi"] < config["rsi_b"] and r["z"] < -1:
                open_trade = {
                    "side": "BUY",
                    "sl": r["close"] - r["atr"] * config["sl"],
                    "tp": r["close"] + r["atr"] * config["tp"]
                }

        print(f"{datetime.utcnow()} | Balance: {round(balance,2)}")
        time.sleep(60)

# ================= MAIN =================
if __name__ == "__main__":
    print("🔬 Optimizing...")
    configs = []

    for s in SYMBOLS:
        best = optimize(s)
        if best and best["equity"] > 1.02:
            configs.append(best)
            print("✔", best)

    if not configs:
        print("No profitable symbols found")
        exit()

    # Trade best symbol
    configs.sort(key=lambda x: x["equity"], reverse=True)
    live_trade(configs[0])
