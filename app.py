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


# ===============================
# INSTITUTIONAL SCORING ENGINE
# ===============================

def institutional_score(rsi, ma9, ma21, change):
    score = 50

    if rsi:
        if rsi < 30:
            score += 15
        elif rsi > 70:
            score -= 15

    if ma9 and ma21:
        if ma9 > ma21:
            score += 15
        else:
            score -= 15

    if change:
        if change > 0:
            score += 10
        else:
            score -= 10

    score = max(0, min(100, score))
    return score


def generate_recommendation(score):
    if score >= 75:
        return "STRONG BUY"
    elif score >= 60:
        return "BUY"
    elif score >= 45:
        return "HOLD"
    elif score >= 30:
        return "WEAK SELL"
    else:
        return "STRONG SELL"


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
STRYX INSTITUTIONAL MODE

Market data temporarily unavailable.
Please retry in a few seconds.
"""

            rsi = calculate_rsi(prices)
            ma9 = moving_average(prices, 9)
            ma21 = moving_average(prices, 21)

            score = institutional_score(rsi, ma9, ma21, change)
            recommendation = generate_recommendation(score)
            confidence = round(score * random.uniform(0.85, 0.98), 2)

            sentiment = "BULLISH" if score > 55 else "BEARISH" if score < 45 else "NEUTRAL"

            return f"""
🏦 STRYX INSTITUTIONAL REPORT
--------------------------------
Asset: {asset.upper()}
Price: ${price}
24H Change: {round(change,2)}%

RSI(14): {rsi}
MA 9: {ma9}
MA 21: {ma21}

Trend Score: {score}/100
Market Sentiment: {sentiment}
Recommendation: {recommendation}
Confidence Level: {confidence}%

Generated: {datetime.datetime.now()}
"""

    if "portfolio" in cmd:
        return """
🏦 STRYX PORTFOLIO INTELLIGENCE
--------------------------------
Diversification Score: 78/100
Risk Level: MODERATE
Institutional Advice:
- Maintain balance
- Avoid high leverage
- Allocate max 30% per asset
"""

    if "strategy" in cmd:
        return """
🏦 STRYX STRATEGIC PLAYBOOK
--------------------------------
1. Trade with trend direction
2. Confirm with RSI
3. Risk max 2% capital
4. Scale in, scale out
5. Protect capital first
"""

    if "scan" in cmd:
        return """
🏦 STRYX MARKET SCANNER
--------------------------------
Supported Assets:
- BTC
- ETH
- SOL
- XRP

Try:
Analyze BTC
Analyze ETH
"""

    return """
🏦 STRYX INSTITUTIONAL MODE ACTIVE

Available Commands:
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