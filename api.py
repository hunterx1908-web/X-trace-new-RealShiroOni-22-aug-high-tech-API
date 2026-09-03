import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@RealShiroOni"

# Original API details
ORIGINAL_API_URL = "https://rohit-apis-nine.vercel.app/api/leak-v3"
ORIGINAL_KEY = "Bhai"

# 🔥 API Expiry Date (4 din — aaj included)
API_EXPIRY = "2026-09-21"

def is_expired():
    try:
        expiry = datetime.strptime(API_EXPIRY, "%Y-%m-%d")
        return datetime.utcnow() > expiry
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "High-Tech Leak API is working! (X-TRACE Edition)",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "expires_on": API_EXPIRY,
        "status": "Active" if not is_expired() else "Expired",
        "endpoints": {
            "info": "/api/leak-v3?key=YOUR_KEY&query=PHONE_NUMBER"
        },
        "example": "/api/leak-v3?key=@RealShiroOni&query=8518042438"
    })

@app.route('/api/leak-v3')
def leak_v3():
    # 🔥 Check if API is expired
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}! Please contact support.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    # Get parameters
    key = request.args.get('key')
    query = request.args.get('query')
    
    # 🔐 Key verify
    if not key:
        return jsonify({
            "status": False,
            "error": "Missing API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
        
    if key != VALID_KEY:
        return jsonify({
            "status": False,
            "error": "Invalid API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 401
    
    if not query:
        return jsonify({
            "status": False,
            "error": "Missing 'query' parameter!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # 🔥 Clean phone number (remove +91, 91, spaces)
    clean_query = query.strip().replace(" ", "").replace("+", "")
    if clean_query.startswith("91") and len(clean_query) == 12:
        clean_query = clean_query[2:]
    
    # If it's a phone number (10 digits), add 91 for original API
    if clean_query.isdigit() and len(clean_query) == 10:
        query_for_api = "91" + clean_query
    else:
        query_for_api = clean_query
    
    # Forward to original API
    params = {
        'key': ORIGINAL_KEY,
        'query': query_for_api
    }
    
    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            # Check if data exists
            has_data = False
            if 'data' in data and isinstance(data['data'], dict):
                if 'data' in data['data']:
                    for source_key in ['source1', 'source2']:
                        if source_key in data['data']['data']:
                            source = data['data']['data'][source_key]
                            if isinstance(source, dict) and source.get('records'):
                                has_data = True
                                break
            
            if not has_data:
                return jsonify({
                    "status": False,
                    "message": "No data found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
            
            # Remove original developer if exists
            data.pop('developer', None)
            data.pop('channel', None)
            data.pop('credits_remaining', None)
            
            # Add our branding
            data['developer'] = '@x_TRACEOWNER'
            data['credit'] = '@x_TRACEOWNER'
            data['api_expires_on'] = API_EXPIRY
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "message": "Request timeout. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404

@app.route('/api/leak-v3/<path:path>')
def catch_all(path):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))