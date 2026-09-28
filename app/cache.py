import math
from .db import get_cache

def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0

def find_similar(query_embedding, threshold):
    best = None
    for item in get_cache():
        score = cosine(query_embedding, item["embedding"])
        if best is None or score > best["score"]:
            best = {"score": score, **item}
    if best and best["score"] >= threshold:
        return best
    return None
