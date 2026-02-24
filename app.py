from flask import Flask, render_template, request
import requests
import statistics
import datetime
import random

app = Flask(__name__)

# ====== REAL PRICE (CoinGecko Free API) ======
def get_price(asset_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd&include_24hr_change=true"
    r = requests.get(url)
    data = r.json()
    price = data[asset_id]["usd"]
    change = data[asset_id]["usd_24h_change"]
    return price, change

# ====== GET MARKET CHART DATA ======
def get_market_data(asset_id):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=14"
    r = requests.get(url)
    data = r.json()
    prices = [p[1] for p in data["prices"]]
    return prices

# ====== RSI CALCULATION ======
def calculate_rsi(prices, period=14):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff >= 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 1

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

# ====== MA CALCULATION ======
def moving_average(prices, period):
    if len(prices) < period:
        return None
    return round(statistics.mean(prices[-period:]), 2)

# ====== SIGNAL GENERATOR ======
def generate_signal(price, ma9, ma21, rsi):
    if ma9 > ma21 and rsi < 70:
        return "BUY SIGNAL"
    if ma9 < ma21 and rsi > 30:
        return "SELL SIGNAL"
    return "WAIT / NO CLEAR SIGNAL"

# ====== MAIN ENGINE ======
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

    detected = None
    for key in assets:
        if key in cmd:
            detected = assets[key]
            break

    if detected:
        try:
            price, change = get_price(detected)
            prices = get_market_data(detected)

            rsi = calculate_rsi(prices)
            ma9 = moving_average(prices, 9)
            ma21 = moving_average(prices, 21)

            signal = generate_signal(price, ma9, ma21, rsi)

            fear_greed = random.randint(20, 80)

            return f"""
STRYX FULL MARKET REPORT
--------------------------------
Asset: {detected.upper()}
Price: ${price}
24H Change: {round(change,2)}%

RSI(14): {rsi}
MA 9: {ma9}
MA 21: {ma21}

Signal: {signal}

Fear & Greed Index (Simulated): {fear_greed}

Generated: {datetime.datetime.now()}
"""

        except Exception as e:
            return f"Market API Error: {e}"

    if "scan" in cmd:
        return """
Market Scanner:
Try:
Analyze BTC
Analyze ETH
Analyze SOL
Analyze XRP
"""

    if "strategy" in cmd:
        return """
STRYX PRO STRATEGY

1. Follow MA crossover
2. Confirm with RSI
3. Risk max 2%
4. Always use stop loss
"""

    return """
STRYX FULL MODE ACTIVE

Try commands:
- Analyze BTC
- Analyze ETH
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