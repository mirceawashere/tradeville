import asyncio
import websockets
import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Fetch environment variables
user = os.environ.get("TRADEVILLE_USER")
password = os.environ.get("TRADEVILLE_PASSWORD")

# Function to connect to the API using WebSocket
async def connect_to_api():
    url = "wss://api.tradeville.ro:443"
    subprotocols = ["apitv"]
    async with websockets.connect(url, subprotocols=subprotocols) as websocket:
        # Send login request
        await websocket.send(f'{{"cmd":"login","prm":{{"coduser":"{user}", "parola":"{password}","demo": false }}}}')
        await websocket.recv()  # Receive login response

        # Send portfolio request
        await websocket.send('{ "cmd": "Portfolio", "prm": { "data": "null" } }')
        return await websocket.recv()

# Flask route
@app.route('/get_market_value', methods=['GET'])
def get_market_value():
    try:
        # Run the async WebSocket connection
        response = asyncio.run(connect_to_api())
        data = json.loads(response)

        # Extract and calculate market value
        quantity = data["data"]["Quantity"][0]
        market_price = data["data"]["MarketPrice"][0]
        total_value = quantity * market_price

        # Return JSON response
        return jsonify({"total_value": total_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
