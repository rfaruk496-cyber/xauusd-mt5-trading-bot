import MetaTrader5 as mt5
import pandas as pd

SYMBOL = "XAUUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
CANDLES = 100

# Connect to MetaTrader 5
if not mt5.initialize():
    print("❌ MT5 connection failed")
    print("Error:", mt5.last_error())
    quit()

print("✅ Connected to MetaTrader 5")

# Check account
account = mt5.account_info()

if account is None:
    print("❌ Could not retrieve account information")
    mt5.shutdown()
    quit()

print("Account:", account.login)
print("Balance:", account.balance)
print("Equity:", account.equity)

# Check XAUUSD
symbol_info = mt5.symbol_info(SYMBOL)

if symbol_info is None:
    print("❌ XAUUSD was not found")
    mt5.shutdown()
    quit()

print("✅ XAUUSD found")

# Make sure the symbol is visible
if not symbol_info.visible:
    if not mt5.symbol_select(SYMBOL, True):
        print("❌ Could not select XAUUSD")
        mt5.shutdown()
        quit()

# Get recent candles
rates = mt5.copy_rates_from_pos(
    SYMBOL,
    TIMEFRAME,
    0,
    CANDLES
)

if rates is None:
    print("❌ Could not retrieve XAUUSD data")
    print("Error:", mt5.last_error())
    mt5.shutdown()
    quit()

data = pd.DataFrame(rates)

# Convert timestamp
data["time"] = pd.to_datetime(data["time"], unit="s")

print("\n📊 Latest XAUUSD candles:")
print(data.tail(10))

# Latest price
tick = mt5.symbol_info_tick(SYMBOL)

if tick:
    print("\n💰 XAUUSD")
    print("Bid:", tick.bid)
    print("Ask:", tick.ask)

mt5.shutdown()

print("\n✅ Test completed — NO TRADE WAS PLACED")
