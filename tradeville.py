import asyncio
import websockets
import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

user = os.environ.get("TRADEVILLE_USER")
password = os.environ.get("TRADEVILLE_PASSWORD")


async def connect_to_api():
    url = "wss://api.tradeville.ro:443"
    subprotocols = ["apitv"]
    async with websockets.connect(url, subprotocols=subprotocols) as websocket:
        
        await websocket.send(f'{{"cmd":"login","prm":{{"coduser":"{user}", "parola":"{password}","demo": false }}}}')
        await websocket.recv()  

        
        await websocket.send('{ "cmd": "Portfolio", "prm": { "data": "null" } }')
        return await websocket.recv()

# Flask 
@app.route('/get_market_value', methods=['GET'])
def get_market_value():
    try:
        
        response = asyncio.run(connect_to_api())
        data = json.loads(response)

        
        quantity = data["data"]["Quantity"][0]
        market_price = data["data"]["MarketPrice"][0]
        total_value = quantity * market_price

        
        return str(total_value)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
