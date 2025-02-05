#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Optional if you want to allow cross-origin

app = Flask(__name__)
CORS(app)  # Enable CORS so you can call it from your frontend

BINANCE_BASE_URL = "https://api.binance.us"

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
    headers = {'X-MBX-APIKEY': user_api_key}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        
        # Capture the response from Binance, even in case of an error
        binance_response = resp.json()

        if resp.status_code != 200:
            return jsonify({
                "error": "Binance API error",
                "status_code": resp.status_code,
                "binance_code": binance_response.get("code", "Unknown"),
                "binance_message": binance_response.get("msg", "No message provided")
            }), resp.status_code

        return jsonify(binance_response)  # Return Binance's JSON response

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Binance timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request error", "details": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
