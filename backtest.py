import pandas as pd
from strategy import generate_signal


def run_backtest(data, starting_balance=1000, risk_per_trade=0.01):
    balance = starting_balance
    trades = []

    position = None

    for i in range(50, len(data)):
        current = data.iloc[i]

        # Use candles up to the current candle
        history = data.iloc[:i + 1]

        signal = generate_signal(history)

        # Only one position at a time
        if position is None:

            if signal == "BUY":
                entry = current["close"]

                position = {
                    "type": "BUY",
                    "entry": entry,
                    "entry_index": i
                }

            elif signal == "SELL":
                entry = current["close"]

                position = {
                    "type": "SELL",
                    "entry": entry,
                    "entry_index": i
                }

        else:
            entry = position["entry"]

            if position["type"] == "BUY":
                price_change = current["close"] - entry

            else:
                price_change = entry - current["close"]

            # Simple 1:1 risk/reward exit
            atr = history.iloc[-1]["atr"]

            if pd.isna(atr) or atr <= 0:
                continue

            take_profit = atr
            stop_loss = -atr

            if price_change >= take_profit:
                profit = balance * risk_per_trade
                balance += profit

                trades.append({
                    "type": position["type"],
                    "entry": entry,
                    "exit": current["close"],
                    "result": "WIN",
                    "profit": profit
                })

                position = None

            elif price_change <= stop_loss:
                loss = balance * risk_per_trade
                balance -= loss

                trades.append({
                    "type": position["type"],
                    "entry": entry,
                    "exit": current["close"],
                    "result": "LOSS",
                    "profit": -loss
                })

                position = None

    results = pd.DataFrame(trades)

    if len(results) == 0:
        print("No trades were generated.")
        return

    wins = len(results[results["result"] == "WIN"])
    losses = len(results[results["result"] == "LOSS"])

    win_rate = (wins / len(results)) * 100

    total_profit = results["profit"].sum()

    print("\n========== BACKTEST RESULTS ==========")
    print(f"Starting balance: ${starting_balance:.2f}")
    print(f"Final balance:    ${balance:.2f}")
    print(f"Total trades:     {len(results)}")
    print(f"Wins:             {wins}")
    print(f"Losses:           {losses}")
    print(f"Win rate:         {win_rate:.2f}%")
    print(f"Net profit:       ${total_profit:.2f}")
    print("======================================\n")

    return results


if __name__ == "__main__":
    print("Backtesting engine ready.")
