from urllib.parse import quote
from config import WHATSAPP_MESSAGE



def build_whatsapp_link(phone: str) -> str:
    cleaned_phone = ''.join(ch for ch in phone if ch.isdigit() or ch == '+').lstrip('+')
    return f'https://wa.me/{cleaned_phone}?text={quote(WHATSAPP_MESSAGE)}'
