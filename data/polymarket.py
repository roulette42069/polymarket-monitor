import requests

GAMMA = "https://gamma-api.polymarket.com"

def fetch_event(event_id: str) -> dict:
    url = f"{GAMMA}/events/{event_id}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def pick_market(event: dict, contains: str) -> dict:
    """Pick the first market whose question contains a substring."""
    for m in event.get("markets", []):
        if contains.lower() in m.get("question", "").lower():
            return m
    raise ValueError(f"No market matched: {contains}")
