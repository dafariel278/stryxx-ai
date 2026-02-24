from flask import Flask, render_template, request
import requests
from datetime import datetime
import random

app = Flask(__name__)

# ===============================
# DATA FETCH (CRYPTO AS MACRO PROXY)
# ===============================

def fetch_market():
    try:
        ids = "bitcoin,ethereum"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        return requests.get(url, timeout=10).json()
    except:
        return None


# ===============================
# MACRO REGIME ENGINE
# ===============================

def detect_macro_regime(btc_change, eth_change):

    avg = (btc_change + eth_change) / 2

    if avg > 4:
        return "STRONG RISK-ON"
    elif avg > 1.5:
        return "RISK-ON"
    elif avg >= -1.5:
        return "NEUTRAL"
    elif avg >= -4:
        return "RISK-OFF"
    else:
        return "CRISIS MODE"


def volatility_state(btc_change):
    vol = abs(btc_change)

    if vol < 1:
        return "LOW VOLATILITY"
    elif vol < 3:
        return "EXPANDING VOLATILITY"
    else:
        return "HIGH VOLATILITY"


def allocation_model(regime):

    if regime == "STRONG RISK-ON":
        return "70% Growth Assets | 20% Core | 10% Defensive"
    elif regime == "RISK-ON":
        return "60% Growth | 30% Core | 10% Defensive"
    elif regime == "NEUTRAL":
        return "50% Core | 30% Growth | 20% Defensive"
    elif regime == "RISK-OFF":
        return "30% Growth | 40% Core | 30% Defensive"
    else:
        return "20% Growth | 30% Core | 50% Defensive"


def probability_score(btc_change):
    base = 50
    adjustment = btc_change * 3
    score = base + adjustment
    score = max(5, min(95, score))
    return round(score, 2)


# ===============================
# BLACKROCK 10X REPORT
# ===============================

def hedge_fund_report():

    data = fetch_market()

    if not data:
        return "Market data temporarily unavailable."

    btc_price = data["bitcoin"]["usd"]
    btc_change = data["bitcoin"]["usd_24h_change"]

    eth_price = data["ethereum"]["usd"]
    eth_change = data["ethereum"]["usd_24h_change"]

    regime = detect_macro_regime(btc_change, eth_change)
    volatility = volatility_state(btc_change)
    allocation = allocation_model(regime)
    prob = probability_score(btc_change)

    narrative = (
        "Growth assets gaining institutional traction."
        if "RISK-ON" in regime else
        "Capital preservation bias emerging."
        if "RISK-OFF" in regime or "CRISIS" in regime else
        "Market consolidation phase."
    )

    return f"""
STRYX GLOBAL MACRO HEDGE FUND REPORT
------------------------------------------------
BTC: ${btc_price:,.2f} | {btc_change:.2f}%
ETH: ${eth_price:,.2f} | {eth_change:.2f}%

MACRO REGIME: {regime}
VOLATILITY STATE: {volatility}
PROBABILITY SCORE (Momentum Bias): {prob}%

INSTITUTIONAL NARRATIVE:
{narrative}

STRATEGIC CAPITAL ALLOCATION:
{allocation}

RISK CONTROLS:
• Dynamic Position Sizing
• Volatility Monitoring
• Capital Preservation Protocol Active

Generated: {datetime.utcnow()} UTC
"""


# ===============================
# ROUTE
# ===============================

@app.route("/", methods=["GET", "POST"])
def home():
    output = None

    if request.method == "POST":
        command = request.form.get("command", "").lower()

        if "macro" in command or "hedge" in command or "10x" in command:
            output = hedge_fund_report()
        else:
            output = "Type: macro 10x report"

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run()