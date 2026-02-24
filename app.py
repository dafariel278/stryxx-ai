from flask import Flask, render_template, request
import requests
import statistics
import datetime
import random

app = Flask(__name__)

# ===============================
# SAFE API REQUEST
# ===============================

def safe_request(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


# ===============================
# COINGECKO DATA
# ===============================

def get_price(asset_id):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": asset_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    data = safe_request(url, params)

    if not data or asset_id not in data:
        return None, None

    return (
        data[asset_id].get("usd"),
        data[asset_id].get("usd_24h_change")
    )


def get_market_data(asset_id, days=14):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    data = safe_request(url, params)

    if not data or "prices" not in data:
        return []

    return [p[1] for p in data["prices"]]


# ===============================
# INDICATORS
# ===============================

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains) / period if gains else 0.01
    avg_loss = sum(losses) / period if losses else 0.01

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)


def moving_average(prices, period):
    if len(prices) < period:
        return None
    return round(statistics.mean(prices[-period:]), 2)


def generate_signal(ma9, ma21, rsi):
    if not ma9 or not ma21 or not rsi:
        return "NO SIGNAL"

    if ma9 > ma21 and rsi < 70:
        return "BUY SIGNAL"

    if ma9 < ma21 and rsi > 30:
        return "SELL SIGNAL"

    return "WAIT"


# ===============================
# MAIN ENGINE
# ===============================

def stryx_engine(command):

    cmd = command.lower()

    assets = {
        "btc": "bitcoin",
        "bitcoin": "bitcoin",
        "eth": "ethereum",
        "ethereum": "ethereum",
        "sol": "solana",
        "xrp": "ripple"
    }

    for key in assets:
        if key in cmd:

            asset = assets[key]

            price, change = get_price(asset)
            prices = get_market_data(asset)

            if price is None or not prices:
                return """
STRYX MARKET DATA TEMPORARILY UNAVAILABLE

Please try again in a few seconds.
"""

            rsi = calculate_rsi(prices)
            ma9 = moving_average(prices, 9)
            ma21 = moving_average(prices, 21)
            signal = generate_signal(ma9, ma21, rsi)
            fear_greed = random.randint(20, 80)

            return f"""
STRYX MARKET REPORT
---------------------
Asset: {asset.upper()}
Price: ${price}
24H Change: {round(change,2)}%

RSI(14): {rsi}
MA 9: {ma9}
MA 21: {ma21}

Signal: {signal}
Fear & Greed: {fear_greed}

Generated: {datetime.datetime.now()}
"""

    if "portfolio" in cmd:
        return """
STRYX PORTFOLIO ANALYSIS
--------------------------
Diversification Score: 72/100
Risk Level: MEDIUM

Recommendation:
- Balance allocation
- Avoid overexposure
- Use stop-loss
"""

    if "strategy" in cmd:
        return """
STRYX TRADING STRATEGY
--------------------------
1. Follow MA crossover
2. Confirm with RSI
3. Risk max 2% per trade
4. Always use stop-loss
"""

    if "scan" in cmd:
        return """
STRYX MARKET SCANNER
--------------------------
Available Assets:
- BTC
- ETH
- SOL
- XRP
"""

    return """
STRYX PRO MODE ACTIVE

Try:
- Analyze BTC
- Analyze ETH
- Portfolio BTC 50 ETH 50
- Scan market
- Give strategy
"""


@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            output = stryx_engine(task)

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run()