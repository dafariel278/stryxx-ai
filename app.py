from flask import Flask, render_template, request
import requests
import numpy as np
from datetime import datetime

app = Flask(__name__)

def get_market_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=30"
    data = requests.get(url).json()

    prices = [p[1] for p in data["prices"]]
    current_price = prices[-1]
    change_24h = ((prices[-1] - prices[-2]) / prices[-2]) * 100

    return prices, current_price, change_24h

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = deltas[deltas > 0].sum() / period
    losses = -deltas[deltas < 0].sum() / period

    if losses == 0:
        return 100

    rs = gains / losses
    return 100 - (100 / (1 + rs))

def analyze_coin(symbol):
    coin_map = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "xrp": "ripple"
    }

    symbol = symbol.lower()
    if symbol not in coin_map:
        return "Unsupported asset."

    prices, price, change = get_market_data(coin_map[symbol])

    rsi = calculate_rsi(prices)
    ma9 = np.mean(prices[-9:])
    ma21 = np.mean(prices[-21:])

    score = 0
    if rsi < 30:
        score += 30
    elif rsi > 70:
        score -= 30

    if ma9 > ma21:
        score += 40
    else:
        score -= 40

    if change > 0:
        score += 20
    else:
        score -= 20

    if score > 60:
        recommendation = "STRONG BUY"
    elif score > 20:
        recommendation = "BUY"
    elif score > -20:
        recommendation = "HOLD"
    elif score > -60:
        recommendation = "SELL"
    else:
        recommendation = "STRONG SELL"

    return f"""
INSTITUTIONAL MARKET REPORT
Asset: {symbol.upper()}
Price: ${price:,.2f}
24H Change: {change:.2f}%

Technical Indicators:
RSI (14): {rsi:.2f}
MA 9: {ma9:,.2f}
MA 21: {ma21:,.2f}

Quant Score: {score}
Recommendation: {recommendation}

Generated: {datetime.utcnow()} UTC
"""

@app.route("/", methods=["GET","POST"])
def home():
    output = None

    if request.method == "POST":
        command = request.form.get("command","").lower()

        if "analyze" in command:
            symbol = command.split()[-1]
            output = analyze_coin(symbol)

        elif "scan" in command:
            output = "Supported assets: BTC, ETH, SOL, XRP"

        elif "portfolio" in command:
            output = "Portfolio engine under development."

        else:
            output = "Command not recognized."

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()