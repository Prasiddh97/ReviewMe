# review_fetcher.py
import os, requests, re, time
from bs4 import BeautifulSoup

YELP_KEY = os.getenv("YELP_API_KEY")      # add to secrets.toml on Streamlit[89]
YELP_URL = "https://api.yelp.com/v3/businesses/{id}/reviews"

def _yelp_reviews(biz_id, limit=3):
    if not YELP_KEY:
        return []
    headers = {"Authorization": f"Bearer {YELP_KEY}"}
    resp = requests.get(YELP_URL.format(id=biz_id), headers=headers, params={"limit": limit})
    if resp.status_code == 200:
        return [d["text"] for d in resp.json().get("reviews", [])]
    return []

def _google_reviews(place_id, key, limit=5):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "review", "key": key}
    r = requests.get(url, params=params).json()
    revs = r.get("result", {}).get("reviews", [])
    return [rv["text"] for rv in revs[:limit]]

def _scrape_reviews(url, css_selector, limit=20):
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    return [el.get_text(strip=True) for el in soup.select(css_selector)][:limit]

def fetch_reviews(source: str, **kwargs):
    """Unified wrapper—returns list[str] of raw review texts."""
    if source=="yelp":
        return _yelp_reviews(kwargs["biz_id"])
    if source=="google":
        return _google_reviews(kwargs["place_id"], kwargs["api_key"])
    if source=="scrape":
        return _scrape_reviews(kwargs["url"], kwargs["selector"])
    return []
