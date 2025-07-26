# analyze_reviews.py
from review_fetcher import fetch_reviews
from summarizer import summarize

def analyze(query_params: dict):
    """
    Analyzes reviews based on a source (Yelp/Google), store name, and location.
    """
    source = query_params.get("source")
    store_name = query_params.get("store_name")
    location = query_params.get("location")

    if not all([source, store_name, location]):
        return {"error": "Missing source, store name, or location."}

    # Fetch reviews from the selected source
    reviews = fetch_reviews(source, store_name=store_name, location=location)

    if not reviews:
        return {"error": f"No {source.title()} reviews found for '{store_name.title()}' in '{location.title()}'."}

    summary = summarize(reviews)
    return {"summary": summary, "samples": reviews[:5]}
