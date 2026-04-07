import os

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_API_KEY')
LOCATION = os.getenv('LOCATION', 'Cairo Egypt')
BUSINESS_TYPE = os.getenv('BUSINESS_TYPE', 'restaurants')
RADIUS = int(os.getenv('RADIUS', '3000'))

EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
WHATSAPP_MESSAGE = os.getenv(
    'WHATSAPP_MESSAGE',
    'Hello I can help you grow your business with a professional website'
)
