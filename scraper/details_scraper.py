import requests
from config import API_KEY

DETAILS_URL = 'https://maps.googleapis.com/maps/api/place/details/json'



def get_details(place_id: str) -> dict:
    response = requests.get(
        DETAILS_URL,
        params={
            'key': API_KEY,
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,website,rating,geometry,formatted_address',
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload.get('result', {})
    geometry = result.get('geometry', {}).get('location', {})

    return {
        'name': result.get('name'),
        'phone': result.get('formatted_phone_number'),
        'website': result.get('website'),
        'rating': result.get('rating'),
        'lat': geometry.get('lat'),
        'lng': geometry.get('lng'),
        'address': result.get('formatted_address'),
    }
