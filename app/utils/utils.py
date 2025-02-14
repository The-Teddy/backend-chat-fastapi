from datetime import datetime

def to_iso_format(data: dict)-> dict:

    date_fields = ['created_at', 'updated_at', 'last_login', 'email_verified']

    for field in date_fields:
        if field in data and isinstance(data[field], datetime):
            data[field] = data[field].isoformat()

    return data