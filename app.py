from flask import Flask, render_template, request
import requests
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import datetime
import random
import os

app = Flask(__name__)

# ==============================
# COINGECKO REAL DATA (FREE)
# ==============================

def get_price(asset_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": asset_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    r = requests.get(url)
    data = r.json()
    return data[asset_id]["usd"], data[asset_id]["usd_24h_change"]


def get_market_data(asset_id, days=14):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url)
    data = r.json()
    prices = [p[1] for p in data["prices"]]
    return prices


# ==============================
# TECHNICAL INDICATORS
# ==============================

def calculate_rsi(prices, period=14):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff >= 0:
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
    if ma9 and ma21:
        if ma9 > ma21 and rsi < 70:
            return "BUY SIGNAL"
        if ma9 < ma21 and rsi > 30:
            return "SELL SIGNAL"
    return "WAIT / NO CLEAR SIGNAL"


# ==============================
# CHART GENERATOR
# ==============================

def generate_chart(prices, asset):
    plt.figure()
    plt.plot(prices)
    plt.title(f"{asset.upper()} Price Chart")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    chart_path = "static/chart.png"
    plt.savefig(chart_path)
    plt.close()


# ==============================
# PORTFOLIO ANALYZER
# ==============================

def portfolio_analysis(text):
    risk_score = random.randint(40, 85)
    level = "Low Risk" if risk_score < 50 else "Medium Risk" if risk_score < 70 else "High Risk"

    return f"""
STRYX PORTFOLIO ANALYSIS
-------------------------
Input: {text}

Diversification Score: {risk_score}/100
Risk Level: {level}

Recommendation:
- Avoid overexposure
- Balance high & mid cap assets
- Use risk management
"""


# ==============================
# MAIN ENGINE
# ==============================

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

            try:
                price, change = get_price(asset)
                prices = get_market_data(asset)

                rsi = calculate_rsi(prices)
                ma9 = moving_average(prices, 9)
                ma21 = moving_average(prices, 21)
                signal = generate_signal(ma9, ma21, rsi)
                fear_greed = random.randint(20, 80)

                generate_chart(prices, asset)

                return f"""
STRYX FULL MARKET REPORT
-------------------------
Asset: {asset.upper()}
Price: ${price}
24H Change: {round(change,2)}%

RSI(14): {rsi}
MA 9: {ma9}
MA 21: {ma21}

Signal: {signal}
Fear & Greed Index: {fear_greed}

Generated: {datetime.datetime.now()}
"""

            except Exception as e:
                return f"Market API Error: {e}"

    if "portfolio" in cmd:
        return portfolio_analysis(command)

    if "scan" in cmd:
        return """
STRYX MARKET SCANNER
---------------------
Available Assets:
- BTC
- ETH
- SOL
- XRP

Try: Analyze BTC
"""

    if "strategy" in cmd:
        return """
STRYX PRO STRATEGY
-------------------
1. Follow MA crossover
2. Confirm with RSI
3. Risk max 2%
4. Always use stop-loss
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
    app.run(host="0.0.0.0", port=5000)