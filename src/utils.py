import re
import json
from typing import Tuple

def sanitize_user_text(text: str, max_len: int) -> str:
    """Basic hardening against prompt injection and abuse.
    - Trim length
    - Strip control chars
    - Remove obvious 'ignore previous instructions' patterns
    - Block attempts to include email creds or URLs
    """
    if not text:
        return ""
    text = text.replace("\x00", " ")
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', ' ', text)
    text = text[:max_len]
    # Remove common attack phrases
    patterns = [
        r'(?i)ignore (the )?previous instructions',
        r'(?i)you are now .*?',
        r'(?i)system prompt:.*',
        r'(?i)please email .*',
        r'(?i)format other than json',
        r'(?i)tool.*?call.*?',
    ]
    for p in patterns:
        text = re.sub(p, '[redacted]', text)
    # Remove URLs and emails to avoid accidental forwarding
    text = re.sub(r'https?://\S+', '[url]', text)
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[email]', text)
    return text.strip()

def assert_only_json(s: str) -> dict:
    """Ensure the model returned only JSON and parse it."""
    # Grab first and last braces
    start = s.find('{')
    end = s.rfind('}')
    if start == -1 or end == -1 or end <= start:
        raise ValueError("LLM did not return valid JSON.")
    payload = s[start:end+1]
    return json.loads(payload)

def clamp_price_currency(car: dict) -> dict:
    """Normalize price / estimated_price currency to 'L.E' and integers for amounts when possible."""
    price_keys = ["price", "estimated_price"]
    for k in price_keys:
        if k in car and isinstance(car[k], dict):
            amt = car[k].get("amount")
            cur = car[k].get("currency") or "L.E"
            if isinstance(amt, str):
                digits = re.sub(r'[^\d]', '', amt)
                if digits:
                    amt = int(digits)
                else:
                    amt = None
            elif isinstance(amt, float):
                amt = int(round(amt))
            car[k]["amount"] = amt
            car[k]["currency"] = "L.E" if cur.upper().startswith("L") else cur
    return car

def safe_merge_body_type(car: dict, body_type_from_image: str) -> dict:
    if "car" in car:
        car["car"]["body_type"] = body_type_from_image
    elif "body_type" in car:
        car["body_type"] = body_type_from_image
    return car
