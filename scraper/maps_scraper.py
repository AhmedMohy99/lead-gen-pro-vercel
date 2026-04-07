import time
import requests
from config import API_KEY, LOCATION, BUSINESS_TYPE, RADIUS

GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
NEARBY_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


class MapsScraperError(RuntimeError):
    pass



def get_coordinates() -> tuple[float, float]:
    if not API_KEY or API_KEY == 'YOUR_GOOGLE_API_KEY':
        raise MapsScraperError('GOOGLE_MAPS_API_KEY is missing. Add it in Vercel Environment Variables.')

    response = requests.get(
        GEOCODE_URL,
        params={'address': LOCATION, 'key': API_KEY},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()

    results = payload.get('results', [])
    if not results:
        raise MapsScraperError(f'Could not find coordinates for location: {LOCATION}')

    location = results[0]['geometry']['location']
    return float(location['lat']), float(location['lng'])



def search_places(lat: float, lng: float, max_pages: int = 3) -> list[dict]:
    all_results: list[dict] = []
    next_page_token: str | None = None

    for page_index in range(max_pages):
        params = {
            'key': API_KEY,
            'location': f'{lat},{lng}',
            'radius': RADIUS,
            'keyword': BUSINESS_TYPE,
        }
        if next_page_token:
            params['pagetoken'] = next_page_token
            # Google Places needs a short delay before pagetoken is active
            time.sleep(2)

        response = requests.get(NEARBY_URL, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()

        status = payload.get('status', 'UNKNOWN')
        if status not in {'OK', 'ZERO_RESULTS'}:
            if page_index == 0:
                raise MapsScraperError(f'Places API error: {status}')
            break

        all_results.extend(payload.get('results', []))
        next_page_token = payload.get('next_page_token')
        if not next_page_token:
            break

    return all_results
