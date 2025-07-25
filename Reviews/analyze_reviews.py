# analyze_reviews.py
from review_fetcher import fetch_reviews
from summarizer   import summarize

def analyze(query: str) -> dict:
    """
    Very naive mapping: you should replace with
    real entity resolution (Google Places search, etc.).
    For demo we accept: 'yelp:<bizid>' or HTML URL.
    """
    if query.startswith("yelp:"):
        reviews = fetch_reviews("yelp", biz_id=query.split(":",1)[1])
    elif query.startswith("http"):
        reviews = fetch_reviews("scrape", url=query, selector=".review, .text")
    else:
        return {"error": "Unrecognized query"}
    if not reviews:
        return {"error": "No reviews found"}
    summary = summarize(reviews)
    return {"summary": summary, "samples": reviews[:5]}
