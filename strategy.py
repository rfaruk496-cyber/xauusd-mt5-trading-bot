import pandas as pd
import numpy as np


def calculate_indicators(df):
    df = df.copy()

    # EMA trend indicators
    df["ema_fast"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=50, adjust=False).mean()

    # RSI
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))

    # ATR
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())

    true_range = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    df["atr"] = true_range.rolling(14).mean()

    return df


def generate_signal(df):
    df = calculate_indicators(df)

    if len(df) < 50:
        return "WAIT"

    current = df.iloc[-1]

    # BUY conditions
    buy_condition = (
        current["ema_fast"] > current["ema_slow"]
        and current["rsi"] > 50
        and current["rsi"] < 70
    )

    # SELL conditions
    sell_condition = (
        current["ema_fast"] < current["ema_slow"]
        and current["rsi"] < 50
        and current["rsi"] > 30
    )

    if buy_condition:
        return "BUY"

    if sell_condition:
        return "SELL"

    return "WAIT"
