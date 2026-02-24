from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        data = response.json()

        price = data[coin_id]["usd"]
        change = data[coin_id]["usd_24h_change"]

        return price, change
    except Exception as e:
        return None, None

def analyze(symbol):
    coins = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "xrp": "ripple"
    }

    symbol = symbol.lower()

    if symbol not in coins:
        return "Unsupported asset. Try BTC, ETH, SOL, XRP."

    price, change = get_price(coins[symbol])

    if price is None:
        return "Market API temporarily unavailable."

    sentiment = "BULLISH" if change > 0 else "BEARISH"

    recommendation = "BUY" if change > 2 else \
                     "HOLD" if -2 <= change <= 2 else \
                     "SELL"

    return f"""
STRYX QUANT MARKET REPORT
----------------------------------------
Asset: {symbol.upper()}
Price: ${price:,.2f}
24H Change: {change:.2f}%

Market Sentiment: {sentiment}
Quant Recommendation: {recommendation}

Generated: {datetime.utcnow()} UTC
"""

@app.route("/", methods=["GET", "POST"])
def home():
    output = None

    if request.method == "POST":
        command = request.form.get("command", "").lower()

        if "btc" in command:
            output = analyze("btc")
        elif "eth" in command:
            output = analyze("eth")
        elif "sol" in command:
            output = analyze("sol")
        elif "xrp" in command:
            output = analyze("xrp")
        else:
            output = "Type: Analyze BTC or Analyze ETH"

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()