import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD



def send_email(to_email: str, name: str) -> bool:
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return False

    message = EmailMessage()
    message['Subject'] = 'Grow your business online'
    message['From'] = EMAIL_SENDER
    message['To'] = to_email
    message.set_content(
        f'Hello {name}\n\n'
        'I can help you get more customers by building a professional website and improving your digital presence.\n\n'
        'Let me know if you are interested.'
    )

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
        return True
    except Exception:
        return False
