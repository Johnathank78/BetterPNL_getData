#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Optional if you want to allow cross-origin

app = Flask(__name__)
CORS(app)  # Enable CORS so you can call it from your local "Live Server" front end

BINANCE_BASE_URL = "https://api.binance.com"

@app.route('/proxySigned', methods=['POST'])
def proxy_signed():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    user_api_key = data.get('apiKey')
    endpoint = data.get('endpoint')
    query_string = data.get('queryString')

    if not user_api_key or not endpoint or not query_string:
        return jsonify({"error": "Missing fields"}), 400

    # Construct the full URL for Binance
    url = f"{BINANCE_BASE_URL}{endpoint}?{query_string}"

    # Forward the request to Binance, injecting the public API key in the header
    headers = {
        'X-MBX-APIKEY': user_api_key
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()  # Raise exception if not 2xx
        return jsonify(resp.json())  # Return the JSON from Binance
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

