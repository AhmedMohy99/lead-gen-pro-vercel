from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Free Lead Gen API running"
    })

@app.route("/run")
def run():
    query = request.args.get("q", "restaurant")
    location = request.args.get("location", "Cairo Egypt")

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{query} {location}",
        "format": "json",
        "limit": 20
    }

    headers = {
        "User-Agent": "lead-gen"
    }

    res = requests.get(url, params=params, headers=headers)
    data = res.json()

    leads = []

    for place in data:
        leads.append({
            "name": place.get("display_name"),
            "lat": place.get("lat"),
            "lon": place.get("lon")
        })

    return jsonify({
        "count": len(leads),
        "leads": leads
    })

# IMPORTANT FOR VERCEL
def handler(request):
    return app(request.environ, start_response=None)
