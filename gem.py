import yfinance as yf
import pandas as pd
import argparse
from datetime import datetime, timedelta

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate GEM strategy allocation for a specific date')
    parser.add_argument('--date', type=str, help='Date to calculate GEM for (YYYY-MM-DD format)', default=None)
    return parser.parse_args()

# Define tickers for GEM
tickers = {
    "SPY": "SPY",   # US stocks
    "VEU": "VEU",   # International stocks
    "BND": "BND"    # Bonds
}

# Parse command line arguments
args = parse_arguments()

# Set end date based on command line argument or use today
if args.date:
    end_date = datetime.strptime(args.date, "%Y-%m-%d")
else:
    end_date = datetime.today()

# Get about 380 days before the end date to ensure 252 trading days are covered
start_date = end_date - timedelta(days=380)

# Download adjusted close prices (default is now adjusted)
data = yf.download(
    list(tickers.values()),
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d"),
    threads=False  # avoid rate-limiting issues
)

# Keep just the 'Close' prices
data = data['Close'].dropna()

# Print data info for debugging
print(f"\nData shape: {data.shape}")
print(f"Data date range: {data.index[0]} to {data.index[-1]}")
print(f"Trading days in dataset: {len(data)}")
print(f"GEM calculation date: {end_date.strftime('%Y-%m-%d')}")

# Calculate 252-trading-day returns
returns = {}
for label, symbol in tickers.items():
    if symbol in data.columns:
        print(f"\n{label} ({symbol}) data points: {len(data[symbol])}")
        if len(data[symbol]) >= 252:
            # Find the closest date to end_date in the data
            closest_date_idx = data.index.get_indexer([end_date], method='pad')[0]
            current = data[symbol].iloc[closest_date_idx]
            
            # Get the price from exactly 252 trading days before the current date
            if closest_date_idx >= 252:
                past = data[symbol].iloc[closest_date_idx - 252]
                current_date = data.index[closest_date_idx].strftime('%Y-%m-%d')
                past_date = data.index[closest_date_idx - 252].strftime('%Y-%m-%d')
                returns[label] = (current / past) - 1
                print(f"{label} ({symbol}): {returns[label]*100:.2f}% (from {past_date} to {current_date})")
            else:
                print(f"{label} ({symbol}): Not enough data (need 252 trading days before the calculation date)")
                continue
        else:
            print(f"{label} ({symbol}): Not enough data (need 252 days, have {len(data[symbol])})")
    else:
        print(f"{label} ({symbol}): Symbol not found in data")

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
if sorted_returns:
    for k, v in sorted_returns:
        print(f"{k}: {v*100:.2f}%")
else:
    print("No valid returns calculated")
