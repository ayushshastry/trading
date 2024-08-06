endpoint = "https://paper-api.alpaca.markets/v2"
api_key = "PKZQX3COP15EEX24MI0E"
api_secret = "vdyenIKqieFAu7JChmcNMTtl8GfxP5qTK2lwQEJA"

import alpaca_trade_api as tradeapi
import numpy as np
import time
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame
import matplotlib.pyplot as plt

SEC_KEY = api_secret 
PUB_KEY = api_key
BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(key_id = PUB_KEY, secret_key = SEC_KEY, base_url = BASE_URL)


symb = "SPY"
pos_held = False 
total_profit = 0
profit_array = []

count = 0

while True:
    print("")
    print("Checking Price")
    market_data = api.get_bars(symb, timeframe = TimeFrame.Minute, limit=5, start=f"2024-03-08T14:{str(30 + count)}:00Z", end=f"2024-03-08T14:{str(35 + count)}:00Z") # Get one bar object for each of the past 5 minutes
    close_list = []   # Stores all the closing prices from the last 5 mintues
    for bar in market_data:
        close_list.append(bar.c) # bar.c is the closing price of the bar's time interval
    
    close_list = np.array(close_list, dtype = np.float64)
    ma = np.mean(close_list)
    last_price = close_list[-1]
    volatility = np.std(close_list)
    
    buy_threshold = ma - volatility
    sell_threshold = ma + volatility

    print(f"Moving Average: {ma}")
    print(f"Last Price: {last_price}")
    print(f"Volatility: {volatility}")
    print(f"Buy Threshold: {buy_threshold}")
    print(f"Sell Threshold: {sell_threshold}")

    if last_price < buy_threshold and not pos_held:
        print("Buy")
        start_price = last_price
        pos_held = True
    elif last_price > sell_threshold and pos_held:
        print("Sell")
        total_profit += (last_price - start_price)
        pos_held = False
    count += 1
    print(f"Total profit: {total_profit}")
    profit_array.append(total_profit)
    if count == 10:
        break

    time.sleep(5)

plt.plot(profit_array, label='Total Profit', color='blue')
plt.title('Total Profit Over Time')
plt.xlabel('Iteration')
plt.ylabel('Total Profit ($)')
plt.ylim(min(profit_array) - 0.5, max(profit_array) + 0.5)
plt.legend()
plt.grid(True)
plt.pause(1) 
plt.show()

from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


client = StockHistoricalDataClient(api_key, api_secret)

params = StockTradesRequest(
    symbol_or_symbols="GOOG",
    start=datetime(2024, 3, 28, 14, 30),
    end = datetime(2024, 3, 28, 14, 45)
)

trades = client.get_stock_trades(params)

for trade in reversed(trades.data["GOOG"]):
    print(trade)


# no keys required for crypto data
client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
    symbol_or_symbols=["BTC/USD", "ETH/USD"],
    timeframe=TimeFrame.Day,
    start="2022-07-01"
)

bars = client.get_crypto_bars(request_params)

print(bars)
