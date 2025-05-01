# GEM Strategy Tracker

This is a simple Python script that implements the **Global Equities Momentum (GEM)** strategy popularized by Gary Antonacci in *Dual Momentum Investing*.

It evaluates 252-trading-day momentum across:
- **SPY** (U.S. stocks)
- **VEU** (International stocks)
- **BND** (Bonds)

If none show positive momentum, the strategy shifts to **cash**.

---

## 🔧 Requirements

- Python 3.x
- [`yfinance`](https://pypi.org/project/yfinance/)

---

## ✅ Setup (Recommended)

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install yfinance
```

---

## ▶️ Run the Strategy

```bash
python gem.py
```

This will:
- Download historical prices
- Calculate 252-trading-day returns
- Output the recommended asset for GEM allocation

---

## 🧠 Strategy Logic

1. Look back 252 trading days.
2. Compare SPY, VEU, BND returns.
3. If the best return is positive, invest in that asset.
4. If not, stay in cash.
5. Rebalance on a fixed day each month (e.g. the 5th).

---

## 🧪 Customize

To switch to a 200-trading-day version, open `gem.py` and change:

```python
past = data[symbol].iloc[-252]
```

to

```python
past = data[symbol].iloc[-200]
```

---

## 📚 References

- [OptimalMomentum.com](https://www.optimalmomentum.com/)
- [Book on Amazon](https://www.amazon.com/Dual-Momentum-Investing-Innovative-Strategy/dp/0071849440)
- [StockCharts GEM-style view](https://stockcharts.com/freecharts/perf.php?BIL,VOO,VEU,BND&n=252&O=011000)

---

## ⚠️ Disclaimer

This is not financial advice. Use at your own risk. Educational purposes only.

---

Built by [Adamo](#).
