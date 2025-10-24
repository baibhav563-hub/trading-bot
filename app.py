from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

# Load secrets from the .env file
load_dotenv()

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN", "").strip()
USE_SANDBOX = os.getenv("USE_SANDBOX", "true").lower() == "true"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "invalid secret"}), 401

    action = data.get("action")
    qty = data.get("qty", 1)
    instrument = data.get("instrument_token")

    base_url = "https://api-sandbox.upstox.com" if USE_SANDBOX else "https://api.upstox.com"
    url = f"{base_url}/v2/order/place"

    payload = {
    "instrument_token": instrument,
    "quantity": qty,
    "transaction_type": action,
    "order_type": "MARKET",
    "price": 0,
    "trigger_price": 0,
    "product": "I",
    "validity": "DAY"
}



    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    return jsonify({"status": "sent", "response": r.json()}), r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
