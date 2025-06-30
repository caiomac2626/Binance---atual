from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

BINANCE_KEY = os.environ.get("BINANCE_KEY")
BINANCE_SECRET = os.environ.get("BINANCE_SECRET")

client = Client(BINANCE_KEY, BINANCE_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data is None or "symbol" not in data or "side" not in data or "quantity" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    symbol = data["symbol"]
    side = data["side"].upper()
    quantity = float(data["quantity"])

    try:
        if side == "BUY":
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quoteOrderQty=quantity  # valor em USDT
            )
            return jsonify({"message": "Ordem de compra enviada", "order": order}), 200
        else:
            return jsonify({"message": "Tipo de ordem não suportado"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Bot da Binance operando com sucesso!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
