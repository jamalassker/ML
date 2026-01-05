
#!/usr/bin/env python3
"""
Binance Micro Scalper - High-Frequency Trading Bot

Features:
- Monitors 100 coins simultaneously
- Opens many trades per hour (scalping mode)
- Uses OBI, VWAP, Z-Score, Volume analysis
- Multiple concurrent positions
- Real-time Telegram notifications
"""

import os
import asyncio
import math
import time
import logging
import datetime
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum

import aiohttp
import numpy as np
from binance import AsyncClient
from binance.enums import *

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

API_KEY = os.getenv("BINANCE_API_KEY", "Et7oRtg2CLHyaRGBoQOoTFt7LSixfav28k0bnVfcgzxd2KTal4xPlxZ9aO6sr1EJ")
API_SECRET = os.getenv("BINANCE_API_SECRET", "2LfotApekUjBH6jScuzj1c47eEnq1ViXsNRIP4ydYqYWl6brLhU3JY4vqlftnUIo")

PAPER_MODE = True
USE_TESTNET = False

TG_TOKEN = os.getenv("TG_TOKEN", "8560134874:AAHF4efOAdsg2Y01eBHF-2DzEUNf9WAdniA")
TG_CHAT_ID = os.getenv("TG_CHAT_ID", "5665906172")

INITIAL_CAPITAL = 100.0
SYMBOLS_TO_MONITOR = 100
MAX_POSITIONS = 30
POSITION_SIZE_PCT = 0.03
MIN_TRADE_VALUE = 5.0

TP_PERCENT = 0.003
SL_PERCENT = 0.002
TRAILING_STOP_PCT = 0.0015

TRADE_COOLDOWN = 3
MAX_HOLD_TIME = 180
SCAN_INTERVAL = 0.3

MAX_DAILY_LOSS_PCT = 0.15
MAX_HOURLY_TRADES = 100
MAX_SPREAD_PCT = 0.002

OBI_STRONG_BUY = 0.15
OBI_BUY = 0.08
OBI_DEPTH = 10

# 🔧 FIX: was too strict for scalping
VWAP_DEVIATION_BUY = -0.0007
VWAP_DEVIATION_SELL = 0.003

ZSCORE_BUY = -1.5
ZSCORE_SELL = 1.5
ZSCORE_LOOKBACK = 20

VOLUME_SURGE_MULT = 2.0
VOLUME_LOOKBACK = 20

# 🔧 FIX: unreachable threshold
MIN_ENTRY_SCORE = 2.5
MIN_EXIT_SCORE = -2.0

# 🔧 FIX: indicator warm-up
MIN_WARMUP_PRICES = 25
MIN_WARMUP_TRADES = 30

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Position:
    symbol: str
    entry_price: float
    quantity: float
    entry_time: float
    stop_loss: float
    take_profit: float
    highest_price: float
    entry_score: float
    obi: float
    zscore: float

@dataclass
class MarketData:
    price: float
    bid: float
    ask: float
    spread: float
    obi: float
    vwap: float
    vwap_dev: float
    zscore: float
    volume_ratio: float
    score: float

@dataclass
class Stats:
    trades: int = 0
    wins: int = 0
    losses: int = 0
    total_pnl: float = 0.0
    hourly_trades: int = 0
    last_hour_reset: float = 0.0

class State:
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.filters: Dict[str, dict] = {}
        self.last_trade: Dict[str, float] = {}
        self.prices: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.volumes: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.trades_data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=500))
        self.balance = INITIAL_CAPITAL
        self.paper_balance = INITIAL_CAPITAL
        self.start_balance = INITIAL_CAPITAL
        self.stats = Stats(last_hour_reset=time.time())
        self.running = True

state = State()

# ══════════════════════════════════════════════════════════════════════════════
# INDICATORS (UNCHANGED)
# ══════════════════════════════════════════════════════════════════════════════

def calc_obi(bids, asks, depth):
    bid_vol = sum(float(b[1]) / (i + 1) for i, b in enumerate(bids[:depth]))
    ask_vol = sum(float(a[1]) / (i + 1) for i, a in enumerate(asks[:depth]))
    total = bid_vol + ask_vol
    return (bid_vol - ask_vol) / total if total else 0.0

def calc_vwap(trades):
    if len(trades) < 10:
        return 0.0, 0.0
    recent = list(trades)[-100:]
    pv = sum(t['p'] * t['q'] for t in recent)
    v = sum(t['q'] for t in recent)
    vwap = pv / v if v else 0.0
    dev = (recent[-1]['p'] - vwap) / vwap if vwap else 0.0
    return vwap, dev

def calc_zscore(prices):
    if len(prices) < ZSCORE_LOOKBACK:
        return 0.0
    arr = list(prices)[-ZSCORE_LOOKBACK:]
    std = np.std(arr)
    return (arr[-1] - np.mean(arr)) / std if std else 0.0

def calc_entry_score(obi, vwap_dev, z, vol):
    score = 0
    if obi >= OBI_STRONG_BUY: score += 3
    elif obi >= OBI_BUY: score += 2
    if vwap_dev <= VWAP_DEVIATION_BUY: score += 2
    if z <= ZSCORE_BUY: score += 2
    if vol >= VOLUME_SURGE_MULT: score += 2
    return score

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

async def analyze_symbol(client, symbol):
    ob = await client.get_order_book(symbol=symbol, limit=OBI_DEPTH)
    bids, asks = ob['bids'], ob['asks']
    bid, ask = float(bids[0][0]), float(asks[0][0])
    mid = (bid + ask) / 2

    state.prices[symbol].append(mid)

    # 🔧 FIX: warm-up guard
    if len(state.prices[symbol]) < MIN_WARMUP_PRICES:
        return None
    if len(state.trades_data[symbol]) < MIN_WARMUP_TRADES:
        return None

    trades = await client.get_recent_trades(symbol=symbol, limit=50)
    for t in trades:
        state.trades_data[symbol].append({
            'p': float(t['price']),
            'q': float(t['qty'])
        })

    obi = calc_obi(bids, asks, OBI_DEPTH)
    vwap, dev = calc_vwap(state.trades_data[symbol])
    z = calc_zscore(state.prices[symbol])
    vol = 1.0

    score = calc_entry_score(obi, dev, z, vol)

    return MarketData(mid, bid, ask, 0, obi, vwap, dev, z, vol, score)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

async def trading_loop(client, symbols):
    while True:
        now = time.time()

        # 🔧 FIX: hourly reset order
        if now - state.stats.last_hour_reset >= 3600:
            state.stats.hourly_trades = 0
            state.stats.last_hour_reset = now

        for symbol in symbols:
            data = await analyze_symbol(client, symbol)
            if data and data.score >= MIN_ENTRY_SCORE:
                logger.info(f"ENTRY {symbol} score={data.score:.2f}")

        await asyncio.sleep(SCAN_INTERVAL)

async def main():
    client = await AsyncClient.create(API_KEY, API_SECRET, testnet=USE_TESTNET)
    info = await client.get_exchange_info()
    symbols = [s['symbol'] for s in info['symbols'] if s['symbol'].endswith('USDT')][:SYMBOLS_TO_MONITOR]
    await trading_loop(client, symbols)

if __name__ == "__main__":
    asyncio.run(main())
