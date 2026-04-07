from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Free Lead Gen API running (no Google API)"
    })

@app.route("/run")
def run():
    try:
        query = request.args.get("q", "restaurant")
        location = request.args.get("location", "Cairo")

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": f"{query} in {location}",
            "format": "json",
            "limit": 20
        }

        headers = {
            "User-Agent": "lead-gen-app"
        }

        res = requests.get(url, params=params, headers=headers)
        data = res.json()

        leads = []

        for place in data:
            leads.append({
                "name": place.get("display_name"),
                "lat": place.get("lat"),
                "lon": place.get("lon"),
                "type": place.get("type"),
                "priority": "HIGH"
            })

        return jsonify({
            "status": "success",
            "count": len(leads),
            "leads": leads
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
