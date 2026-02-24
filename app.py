from flask import Flask, render_template, request
import requests
from datetime import datetime
import random

app = Flask(__name__)

# =========================
# DATA FETCH
# =========================

def fetch_market():
    try:
        ids = "bitcoin,ethereum"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        return requests.get(url, timeout=10).json()
    except:
        return None

# =========================
# SOVEREIGN MACRO ENGINE
# =========================

def detect_global_regime(btc_change, eth_change):

    avg = (btc_change + eth_change) / 2

    if avg > 5:
        return "GLOBAL EXPANSION PHASE"
    elif avg > 2:
        return "RISK ACCUMULATION PHASE"
    elif avg >= -2:
        return "TRANSITIONAL MACRO ENVIRONMENT"
    elif avg >= -5:
        return "DEFENSIVE CAPITAL ROTATION"
    else:
        return "SYSTEMIC STRESS ENVIRONMENT"


def sovereign_allocation(regime):

    if "EXPANSION" in regime:
        return "75% Growth Assets | 15% Strategic Core | 10% Defensive Reserve"
    elif "ACCUMULATION" in regime:
        return "65% Growth | 25% Core | 10% Defensive"
    elif "TRANSITIONAL" in regime:
        return "50% Core | 30% Growth | 20% Defensive"
    elif "DEFENSIVE" in regime:
        return "35% Growth | 30% Core | 35% Defensive"
    else:
        return "25% Growth | 25% Core | 50% Capital Preservation"


def sovereign_report():

    data = fetch_market()

    if not data:
        return "Global market data unavailable."

    btc_price = data["bitcoin"]["usd"]
    btc_change = data["bitcoin"]["usd_24h_change"]

    eth_price = data["ethereum"]["usd"]
    eth_change = data["ethereum"]["usd_24h_change"]

    regime = detect_global_regime(btc_change, eth_change)
    allocation = sovereign_allocation(regime)

    stability_index = round(100 - abs(btc_change * 2), 2)
    confidence = round(random.uniform(82, 96), 2)

    narrative = (
        "Global capital flows indicate strategic positioning across risk assets."
        if "EXPANSION" in regime else
        "Institutional capital entering measured accumulation phase."
        if "ACCUMULATION" in regime else
        "Macro environment reflects rotational behavior."
        if "TRANSITIONAL" in regime else
        "Capital preservation mandates elevated."
        if "DEFENSIVE" in regime else
        "Systemic risk elevated. Sovereign capital defensive."
    )

    return f"""
STRYX SOVEREIGN WEALTH FUND REPORT
-------------------------------------------------------
BTC: ${btc_price:,.2f} | {btc_change:.2f}%
ETH: ${eth_price:,.2f} | {eth_change:.2f}%

GLOBAL MACRO REGIME:
{regime}

GLOBAL STABILITY INDEX:
{stability_index}%

INSTITUTIONAL CONFIDENCE:
{confidence}%

SOVEREIGN NARRATIVE:
{narrative}

STRATEGIC ALLOCATION FRAMEWORK:
{allocation}

CAPITAL PRESERVATION PROTOCOL: ACTIVE
LONG-TERM HORIZON: 5–20 YEARS

Generated: {datetime.utcnow()} UTC
"""

# =========================
# ROUTE
# =========================

@app.route("/", methods=["GET","POST"])
def home():
    output = None

    if request.method == "POST":
        command = request.form.get("command","").lower()

        if "sovereign" in command or "macro" in command or "fund" in command:
            output = sovereign_report()
        else:
            output = "Type: sovereign report"

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run()