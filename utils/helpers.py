from pathlib import Path
import csv



def score_lead(details: dict, email: str | None) -> str:
    score = 0
    if not details.get('website'):
        score += 10
    rating = details.get('rating')
    if isinstance(rating, (int, float)) and rating < 4:
        score += 5
    if not email:
        score += 3
    if not details.get('phone'):
        score += 2
    return 'HIGH' if score >= 10 else 'LOW'



def serialize_lead(lead: dict) -> dict:
    return {
        'name': lead.get('name'),
        'phone': lead.get('phone'),
        'website': lead.get('website'),
        'email': lead.get('email'),
        'rating': lead.get('rating'),
        'priority': lead.get('priority'),
        'lat': lead.get('lat'),
        'lng': lead.get('lng'),
        'address': lead.get('address'),
    }



def save_leads_csv(leads: list[dict], path: str) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['name', 'phone', 'website', 'email', 'rating', 'priority', 'lat', 'lng', 'address']
    with destination.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)



def create_map_data(leads: list[dict]) -> list[dict]:
    points = []
    for lead in leads:
        lat = lead.get('lat')
        lng = lead.get('lng')
        if lat is None or lng is None:
            continue
        points.append({
            'name': lead.get('name'),
            'lat': lat,
            'lng': lng,
            'phone': lead.get('phone'),
            'priority': lead.get('priority'),
            'website': lead.get('website'),
            'email': lead.get('email'),
            'address': lead.get('address'),
        })
    return points
