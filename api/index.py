from flask import Flask, jsonify, request, Response
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lead Gen Pro</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: white;
      text-align: center;
      padding: 40px 20px;
      margin: 0;
    }
    .box {
      max-width: 1100px;
      margin: auto;
      background: #111827;
      border-radius: 16px;
      padding: 24px;
    }
    h1 {
      margin-bottom: 8px;
    }
    p {
      opacity: 0.9;
    }
    .controls {
      margin: 20px 0;
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
    }
    input {
      padding: 12px;
      border-radius: 10px;
      border: none;
      min-width: 220px;
    }
    button {
      background: #22c55e;
      color: white;
      border: none;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      opacity: 0.9;
    }
    #status {
      margin: 20px 0;
      font-weight: bold;
    }
    table {
      margin-top: 20px;
      width: 100%;
      border-collapse: collapse;
      background: #1f2937;
      overflow: hidden;
      border-radius: 12px;
    }
    th, td {
      border: 1px solid #374151;
      padding: 10px;
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }
    th {
      background: #0b1220;
    }
    a {
      color: #93c5fd;
    }
  </style>
</head>
<body>
  <div class="box">
    <h1>Lead Gen Pro</h1>
    <p>Free business lead finder using OpenStreetMap</p>

    <div class="controls">
      <input id="query" value="restaurant" placeholder="Business type e.g. cafe" />
      <input id="location" value="Cairo Egypt" placeholder="Location e.g. Cairo Egypt" />
      <button onclick="runScraper()">Run Lead Scraper</button>
    </div>

    <div id="status"></div>
    <div id="results"></div>
  </div>

  <script>
    async function runScraper() {
      const query = document.getElementById("query").value.trim() || "restaurant";
      const location = document.getElementById("location").value.trim() || "Cairo Egypt";
      const status = document.getElementById("status");
      const results = document.getElementById("results");

      status.innerText = "Loading leads...";
      results.innerHTML = "";

      try {
        const url = `/api/run?q=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`;
        const res = await fetch(url);
        const data = await res.json();

        if (data.status !== "success") {
          status.innerText = "Error: " + (data.message || "Unknown error");
          return;
        }

        status.innerText = `Total Leads: ${data.count}`;

        if (!data.leads || data.leads.length === 0) {
          results.innerHTML = "<p>No results found. Try cafe clinic pharmacy restaurant or another city.</p>";
          return;
        }

        let html = `
          <table>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Map</th>
            </tr>
        `;

        data.leads.forEach(l => {
          const mapUrl = `https://www.openstreetmap.org/?mlat=${l.lat}&mlon=${l.lon}#map=18/${l.lat}/${l.lon}`;
          html += `
            <tr>
              <td>${l.name || ""}</td>
              <td>${l.type || ""}</td>
              <td>${l.lat || ""}</td>
              <td>${l.lon || ""}</td>
              <td><a href="${mapUrl}" target="_blank">Open Map</a></td>
            </tr>
          `;
        });

        html += "</table>";
        results.innerHTML = html;
      } catch (err) {
        status.innerText = "Request failed: " + err.message;
      }
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return Response(HTML_PAGE, mimetype="text/html")

@app.route("/api", methods=["GET"])
def api_home():
    return jsonify({
        "status": "ok",
        "message": "Free Lead Gen API running"
    })

@app.route("/api/run", methods=["GET"])
def run():
    try:
        query = request.args.get("q", "restaurant").strip()
        location = request.args.get("location", "Cairo Egypt").strip()

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{query} {location}",
            "format": "jsonv2",
            "limit": 20,
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "lead-gen-pro-vercel"
        }

        res = requests.get(url, params=params, headers=headers, timeout=20)
        res.raise_for_status()
        data = res.json()

        leads = []
        for place in data:
            leads.append({
                "name": place.get("display_name"),
                "lat": place.get("lat"),
                "lon": place.get("lon"),
                "type": place.get("type")
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
