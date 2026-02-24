from flask import Flask, render_template, request
import random

app = Flask(__name__)

def stryx_brain(command):
    cmd = command.lower()

    # Crypto Mode
    if "btc" in cmd or "bitcoin" in cmd:
        price = random.randint(40000, 70000)
        trend = random.choice(["Bullish", "Bearish", "Sideways"])
        return f"""
STRYX CRYPTO ANALYSIS

Asset: Bitcoin (BTC)
Estimated Price: ${price}
Market Trend: {trend}

Recommendation:
- Monitor RSI
- Watch volume confirmation
- Use risk management
"""

    # AI Strategy Mode
    if "strategy" in cmd:
        return """
STRYX STRATEGY ENGINE

Suggested Trading Plan:
1. Identify market structure
2. Wait for breakout confirmation
3. Risk only 1-2% per trade
4. Always use stop-loss
"""

    # General AI Mode
    return f"""
STRYX INTELLIGENCE RESPONSE

Command Received:
{command}

Analysis:
- Task logged
- System running stable
- Awaiting advanced AI integration
"""

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            output = stryx_brain(task)
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)