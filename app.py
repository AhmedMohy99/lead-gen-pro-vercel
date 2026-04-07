from flask import Flask, jsonify, request
from main import run_pipeline
from config import LOCATION, BUSINESS_TYPE, RADIUS

app = Flask(__name__)


@app.get('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'Lead Gen Pro API is running on Vercel',
        'defaults': {
            'location': LOCATION,
            'business_type': BUSINESS_TYPE,
            'radius': RADIUS,
        },
        'routes': {
            'health': '/',
            'run': '/run',
        }
    })


@app.get('/run')
def run():
    limit_value = request.args.get('limit', default='20')
    try:
        limit = max(1, min(int(limit_value), 60))
    except ValueError:
        return jsonify({'status': 'error', 'message': 'limit must be a number'}), 400

    try:
        result = run_pipeline(limit=limit)
        # Vercel file system is temporary, so return the data directly.
        return jsonify(result)
    except Exception as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 500


# Vercel looks for `app`
