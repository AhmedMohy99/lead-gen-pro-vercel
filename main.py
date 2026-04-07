from scraper.maps_scraper import get_coordinates, search_places
from scraper.details_scraper import get_details
from scraper.email_finder import extract_email
from utils.helpers import score_lead, serialize_lead, save_leads_csv, create_map_data
from utils.logger import log


def run_pipeline(limit: int | None = None) -> dict:
    """Run the lead generation pipeline and return structured results."""
    log('Start lead generation pipeline')

    lat, lng = get_coordinates()
    places = search_places(lat, lng)
    if limit:
        places = places[:limit]

    leads: list[dict] = []
    for place in places:
        place_id = place.get('place_id')
        if not place_id:
            continue

        try:
            details = get_details(place_id)
            website = details.get('website')
            email = extract_email(website) if website else None
            priority = score_lead(details, email)

            lead = {
                'name': details.get('name'),
                'phone': details.get('phone'),
                'website': website,
                'email': email,
                'rating': details.get('rating'),
                'priority': priority,
                'lat': details.get('lat'),
                'lng': details.get('lng'),
                'address': details.get('address'),
            }
            leads.append(serialize_lead(lead))
        except Exception as exc:
            log(f'Error processing place {place_id}: {exc}')

    save_leads_csv(leads, 'data/leads.csv')
    map_points = create_map_data(leads)

    result = {
        'status': 'success',
        'location': {'lat': lat, 'lng': lng},
        'count': len(leads),
        'map_points': map_points,
        'leads': leads,
    }
    log(f'Finished pipeline with {len(leads)} leads')
    return result


if __name__ == '__main__':
    output = run_pipeline()
    print(f"Completed successfully. Leads found: {output['count']}")
