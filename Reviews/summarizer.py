# summarizer.py
from functools import lru_cache
from transformers import pipeline

@lru_cache(maxsize=1)
def _get_pipe():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize(texts, max_tokens=120):
    joined = " ".join(texts)
    pipe = _get_pipe()
    out = pipe(joined, max_length=max_tokens, min_length=30, do_sample=False)
    return out[0]["summary_text"]
