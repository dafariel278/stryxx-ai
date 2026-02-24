from flask import Flask, render_template, request
import random
import datetime

app = Flask(__name__)

def stryx_engine(command):
    cmd = command.lower()

    # Crypto Analysis Mode
    if "btc" in cmd or "bitcoin" in cmd:
        price = random.randint(40000, 70000)
        trend = random.choice(["Bullish Momentum", "Bearish Pressure", "Sideways Consolidation"])
        confidence = random.randint(60, 95)

        return f"""
STRYX CRYPTO ANALYSIS REPORT

Asset: Bitcoin (BTC)
Estimated Price Zone: ${price}
Market Structure: {trend}
Confidence Level: {confidence}%

Technical Insight:
- Monitor RSI divergence
- Confirm with volume breakout
- Risk management required

Generated: {datetime.datetime.now()}
"""

    # Strategy Mode
    if "strategy" in cmd:
        return """
STRYX STRATEGY ENGINE

Recommended Plan:

1. Identify trend direction
2. Enter on pullback
3. Risk 1% per trade
4. Use trailing stop
5. Avoid overtrading

Discipline > Emotion
"""

    # General Intelligence Mode
    return f"""
STRYX INTELLIGENCE RESPONSE

Command Received:
{command}

System Analysis:
- Core system online
- Modules active
- Awaiting advanced AI expansion

Status: Stable
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