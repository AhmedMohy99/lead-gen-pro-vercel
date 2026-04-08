from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def extract_contacts(url):
    try:
        r = requests.get(url, timeout=5)
        text = r.text

        phone = re.findall(r'\+?\d[\d\s\-]{8,}', text)
        email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)

        return {
            "phone": phone[0] if phone else None,
            "email": email[0] if email else None
        }
    except:
        return {"phone": None, "email": None}

@app.route("/")
def home():
    return "Lead Gen Pro Running"

@app.route("/api/run")
def run():
    query = request.args.get("q", "restaurant cairo")

    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []

    for a in soup.select("a"):
        href = a.get("href")
        if href and "http" in href and "google" not in href:
            links.append(href)

    leads = []

    for link in links[:10]:
        contacts = extract_contacts(link)

        leads.append({
            "website": link,
            "phone": contacts["phone"],
            "email": contacts["email"]
        })

    return jsonify({
        "count": len(leads),
        "leads": leads
    })
