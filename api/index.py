from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Lead Gen Pro Running"

@app.route("/api/run")
def run():
    query = request.args.get("q", "restaurant")
    location = request.args.get("location", "cairo")

    return jsonify({
        "status": "success",
        "message": "API working",
        "query": query,
        "location": location,
        "leads": [
            {"name": "Test Business 1", "phone": "+201000000000"},
            {"name": "Test Business 2", "phone": "+201111111111"}
        ]
    })
