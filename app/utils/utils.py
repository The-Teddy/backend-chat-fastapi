from datetime import datetime
from email.message import EmailMessage

def to_iso_format(data: dict)-> dict:

    date_fields = ['created_at', 'updated_at', 'last_login', 'email_verified']

    for field in date_fields:
        if field in data and isinstance(data[field], datetime):
            data[field] = data[field].isoformat()

    return data

def set_message_to_email(from_email: str, to_email: str, subject: str, html_content, verification_url: str):
    message = EmailMessage()
    message.set_content(f"Este é um email em HTML, mas seu cliente de email não suporta esse formato. link para verificação: {verification_url}")
    message["From"] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.add_alternative(html_content, subtype="html")

    return message