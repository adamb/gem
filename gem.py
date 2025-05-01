import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define tickers for GEM
tickers = {
    "SPY": "SPY",   # US stocks
    "VEU": "VEU",   # International stocks
    "BND": "BND"    # Bonds
}

# Get about 300 days to ensure 252 trading days are covered
end_date = datetime.today()
start_date = end_date - timedelta(days=300)

# Download adjusted close prices (default is now adjusted)
data = yf.download(
    list(tickers.values()),
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d"),
    threads=False  # avoid rate-limiting issues
)

# Keep just the 'Close' prices
data = data['Close'].dropna()

# Calculate 252-trading-day returns
returns = {}
for label, symbol in tickers.items():
    if symbol in data.columns and len(data[symbol]) >= 252:
        current = data[symbol].iloc[-1]
        past = data[symbol].iloc[-252]
        returns[label] = (current / past) - 1

# Sort and choose best performer with positive return
sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)
if sorted_returns and sorted_returns[0][1] > 0:
    pick = sorted_returns[0][0]
    print(f"GEM would invest in: {pick} ({sorted_returns[0][1]*100:.2f}% 252-day return)")
else:
    pick = "CASH"
    print("GEM would stay in CASH")

# Print all returns
print("\nAll 252-trading-day returns:")
for k, v in sorted_returns:
    print(f"{k}: {v*100:.2f}%")
