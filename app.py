from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API = "https://api-inference.huggingface.co/models/google/gemma-2b-it"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

class CryptoEngine:
    def get_market_data(self, coin="bitcoin"):
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
        params = {"vs_currency": "usd", "days": "14"}
        response = requests.get(url, params=params)
        data = response.json()
        prices = [p[1] for p in data["prices"]]
        return prices

    def calculate_rsi(self, prices, period=14):
        gains = []
        losses = []

        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))

        avg_gain = sum(gains[-period:]) / period if gains else 0.001
        avg_loss = sum(losses[-period:]) / period if losses else 0.001

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)

    def analyze(self, coin="bitcoin"):
        prices = self.get_market_data(coin)
        rsi = self.calculate_rsi(prices)
        current_price = prices[-1]

        trend = "Bullish" if prices[-1] > prices[0] else "Bearish"

        return {
            "price": current_price,
            "rsi": rsi,
            "trend": trend
        }

crypto = CryptoEngine()

class StryxAI:  
    def ask_ai(self, prompt):

        if not HF_TOKEN:
            return "ERROR: HF_TOKEN not found in Vercel environment."

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7
            }
        }

        try:
            response = requests.post(
                HF_API,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                return "HF API ERROR: " + str(response.status_code)

            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]

            return str(result)

        except Exception as e:
            return "REQUEST ERROR: " + str(e)

ai = StryxAI()

@app.route("/", methods=["GET", "POST"])
def home():
    response = None

    if request.method == "POST":
        task = request.form.get("task").lower()

        if "btc" in task:
            coin = "bitcoin"
        elif "eth" in task:
            coin = "ethereum"
        else:
            coin = "bitcoin"

        analysis = crypto.analyze(coin)

        prompt = f"""
        You are STRYX, professional crypto AI.
        Current Price: {analysis['price']}
        RSI: {analysis['rsi']}
        Trend: {analysis['trend']}
        Give short professional trading insight.
        """

        response = ai.ask_ai(prompt)

    return render_template("index.html", response=response)