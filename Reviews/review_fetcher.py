# review_fetcher.py
import os
import requests
from bs4 import BeautifulSoup

# --- API Keys and URLs ---
YELP_KEY = os.getenv("YELP_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Add your Google API Key to secrets

YELP_AUTOCOMPLETE_URL = "https://api.yelp.com/v3/autocomplete"
YELP_REVIEWS_URL = "https://api.yelp.com/v3/businesses/{id}/reviews"

# --- New Google API URL ---
GOOGLE_FIND_PLACE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
GOOGLE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def get_yelp_suggestions(text: str, location: str):
    # (This function remains the same as the previous answer)
    # ...
    pass

# --- New function to find a Google Place ID ---
def get_google_place_id(store_name: str, location: str):
    """Search for a Google Place ID by store name and location."""
    if not GOOGLE_API_KEY:
        return None
    
    # Combine store name and location for a more effective search query
    search_query = f"{store_name} in {location}"
    params = {
        "input": search_query,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_API_KEY,
    }
    try:
        resp = requests.get(GOOGLE_FIND_PLACE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("candidates"):
            return data["candidates"][0]["place_id"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Place ID: {e}")
    return None

def _yelp_reviews(biz_id, limit=3):
    # (This function remains the same)
    # ...
    pass

def _google_reviews(place_id, limit=5):
    """Fetches reviews for a given Google Place ID."""
    if not GOOGLE_API_KEY:
        return []
    params = {"place_id": place_id, "fields": "review", "key": GOOGLE_API_KEY}
    try:
        resp = requests.get(GOOGLE_DETAILS_URL, params=params)
        resp.raise_for_status()
        result = resp.json().get("result", {})
        reviews = result.get("reviews", [])
        return [rv["text"] for rv in reviews[:limit]]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google reviews: {e}")
    return []

def fetch_reviews(source: str, **kwargs):
    """Unified wrapper to fetch reviews from either Yelp or Google."""
    store_name = kwargs.get("store_name")
    location = kwargs.get("location")

    if source == "yelp" and store_name and location:
        biz_id = get_yelp_business_id(store_name, location)
        return _yelp_reviews(biz_id) if biz_id else []
    
    # --- New logic for Google ---
    if source == "google" and store_name and location:
        place_id = get_google_place_id(store_name, location)
        return _google_reviews(place_id) if place_id else []

    return []
