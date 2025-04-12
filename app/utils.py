import re

def sanitize_input(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text) # Remove HTML tags
    text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)', '', text) # Remove links
    return text.strip()
