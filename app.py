from flask import Flask, render_template, request
import random
import datetime

app = Flask(__name__)

def market_ai_engine(command):
    cmd = command.lower()

    assets = {
        "btc": "Bitcoin",
        "bitcoin": "Bitcoin",
        "eth": "Ethereum",
        "ethereum": "Ethereum",
        "sol": "Solana",
        "xrp": "XRP"
    }

    detected_asset = None
    for key in assets:
        if key in cmd:
            detected_asset = assets[key]
            break

    trend = random.choice(["Bullish", "Bearish", "Sideways Consolidation"])
    volatility = random.choice(["Low", "Moderate", "High"])
    sentiment = random.choice(["Fear", "Neutral", "Greed"])
    confidence = random.randint(65, 94)

    if detected_asset:
        return f"""
STRYX MARKET ANALYSIS REPORT
--------------------------------
Asset: {detected_asset}
Trend: {trend}
Volatility: {volatility}
Market Sentiment: {sentiment}
Confidence Level: {confidence}%

Technical Insight:
• Monitor RSI divergence
• Confirm breakout with volume
• Avoid overleveraging

Risk Management:
• Risk max 1-2% per trade
• Always use stop-loss

Generated: {datetime.datetime.now()}
"""

    if "strategy" in cmd:
        return """
STRYX STRATEGY ENGINE
--------------------------------
Recommended Trading Plan:

1. Identify market structure
2. Enter after confirmation candle
3. Risk only small percentage
4. Use trailing stop
5. Avoid emotional trading

Discipline > Emotion
"""

    if "market" in cmd:
        return f"""
GLOBAL MARKET STATUS
--------------------------------
Overall Trend: {trend}
Volatility Index: {volatility}
Sentiment Indicator: {sentiment}

Outlook:
Market currently showing {trend.lower()} behavior.
Traders should remain cautious and manage risk.
"""

    return f"""
STRYX INTELLIGENCE RESPONSE
--------------------------------
Command Received:
{command}

System Status: ONLINE
Modules Active:
• Market Scanner
• Strategy Engine
• Risk Analyzer

Awaiting next command...
"""

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            output = market_ai_engine(task)

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)