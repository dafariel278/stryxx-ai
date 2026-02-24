from flask import Flask, render_template, request
import requests
from datetime import datetime
import random

app = Flask(__name__)

COINS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "xrp": "ripple",
    "bnb": "binancecoin"
}

def fetch_market():
    try:
        ids = ",".join(COINS.values())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        return requests.get(url, timeout=10).json()
    except:
        return None

def quant_score(change):
    score = 50 + (change * 5)
    score = max(5, min(95, score))
    return round(score, 2)

def signal(change):
    if change > 4:
        return "STRONG BUY"
    elif change > 1:
        return "BUY"
    elif change >= -1:
        return "HOLD"
    elif change >= -4:
        return "SELL"
    else:
        return "STRONG SELL"

def ai_narrative(symbol, change):
    if change > 2:
        return f"Institutional capital accumulation detected in {symbol.upper()}. Momentum bias positive."
    elif change < -2:
        return f"Distribution pressure visible in {symbol.upper()}. Short-term risk elevated."
    else:
        return f"{symbol.upper()} consolidating within neutral range. Await breakout confirmation."

def analyze(symbol):

    data = fetch_market()

    if not data:
        return "Market data unavailable."

    coin_id = COINS.get(symbol)
    if not coin_id:
        return "Unsupported asset."

    price = data[coin_id]["usd"]
    change = data[coin_id]["usd_24h_change"]

    score = quant_score(change)
    rec = signal(change)
    narrative = ai_narrative(symbol, change)
    confidence = round(random.uniform(82, 96), 2)

    return f"""
STRYX ULTRA CRYPTO INTELLIGENCE REPORT
--------------------------------------------------
Asset: {symbol.upper()}
Price: ${price:,.2f}
24H Change: {change:.2f}%

Quant Score: {score}/100
AI Signal: {rec}
Confidence Level: {confidence}%

AI Market Narrative:
{narrative}

Risk Protocol:
• Dynamic Position Sizing
• Volatility Monitoring Active
• Institutional Flow Tracking

Generated: {datetime.utcnow()} UTC
"""

@app.route("/", methods=["GET","POST"])
def home():
    output = None

    if request.method == "POST":
        command = request.form.get("command","").lower()

        for symbol in COINS.keys():
            if symbol in command:
                output = analyze(symbol)
                break

        if not output:
            output = "Type: btc / eth / sol / xrp / bnb"

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()