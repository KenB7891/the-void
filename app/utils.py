import re
from datetime import datetime, timezone, timedelta
from fastapi import Request
from app.models import Message
from sqlalchemy.orm import Session

MESSAGE_COOLDOWN_HOURS = 12

def sanitize_input(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text) # Remove HTML tags
    text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)', '', text) # Remove links
    return text.strip()

def get_client_ip(request: Request) -> str:
    return request.client.host

def is_ip_allowed(ip: str, db: Session) -> bool:
    cooldown_cutoff_time = datetime.now(timezone.utc) - timedelta(hours=MESSAGE_COOLDOWN_HOURS)
    cooldown_message = db.query(Message).filter(Message.ip == ip, Message.created_at > cooldown_cutoff_time).first()
    return cooldown_message is None