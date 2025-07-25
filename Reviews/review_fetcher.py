import os
import requests
from bs4 import BeautifulSoup

YELP_KEY = os.getenv("YELP_API_KEY")  # Make sure this is set in your env or Streamlit secrets
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
YELP_REVIEWS_URL = "https://api.yelp.com/v3/businesses/{id}/reviews"


def get_yelp_business_id(store_name: str, location: str):
    """Search for a Yelp business ID by store name and location."""
    if not YELP_KEY:
        return None
    headers = {"Authorization": f"Bearer {YELP_KEY}"}
    params = {
        "term": store_name,
        "location": location,
        "limit": 1,
    }
    resp = requests.get(YELP_SEARCH_URL, headers=headers, params=params)
    if resp.status_code == 200:
        businesses = resp.json().get("businesses", [])
        if businesses:
            return businesses[0]["id"]
    return None


def _yelp_reviews(biz_id, limit=3):
    if not YELP_KEY:
        return []
    headers = {"Authorization": f"Bearer {YELP_KEY}"}
    resp = requests.get(YELP_REVIEWS_URL.format(id=biz_id), headers=headers, params={"limit": limit})
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
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    return [el.get_text(strip=True) for el in soup.select(css_selector)][:limit]


def fetch_reviews(source: str, **kwargs):
    """
    Unified wrapper.

    For Yelp:
        - If 'store_name' and 'location' are provided, first search for business ID.
        - Otherwise, use provided 'biz_id' directly.

    For Google and scrape, behavior unchanged.
    """
    if source == "yelp":
        if "store_name" in kwargs and "location" in kwargs:
            biz_id = get_yelp_business_id(kwargs["store_name"], kwargs["location"])
            if not biz_id:
                return []
            return _yelp_reviews(biz_id)
        elif "biz_id" in kwargs:
            return _yelp_reviews(kwargs["biz_id"])
        else:
            return []

    if source == "google":
        return _google_reviews(kwargs["place_id"], kwargs["api_key"])

    if source == "scrape":
        return _scrape_reviews(kwargs["url"], kwargs["selector"])

    return []
