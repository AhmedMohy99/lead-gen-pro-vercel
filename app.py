from flask import Flask, jsonify
from scraper.maps_scraper import get_coordinates, search_places
from scraper.details_scraper import get_details
from scraper.email_finder import extract_email
from utils.helpers import score_lead

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({
        "status": "ok",
        "message": "Lead Gen Pro API is running on Vercel",
        "routes": {
            "health": "/",
            "run": "/run"
        }
    })

@app.route("/run")
def run_leads():
    try:
        lat, lng = get_coordinates()
        places = search_places(lat, lng)

        leads = []

        for place in places[:20]:
            details = get_details(place["place_id"])
            email = extract_email(details["website"]) if details.get("website") else None
            priority = score_lead(details, email)

            leads.append({
                "name": details.get("name"),
                "phone": details.get("phone"),
                "website": details.get("website"),
                "email": email,
                "rating": details.get("rating"),
                "priority": priority,
                "lat": details.get("lat"),
                "lng": details.get("lng")
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
        }), 500
