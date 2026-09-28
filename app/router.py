# Fast, explainable routing heuristic for the MVP.
# Later this can be replaced by a classifier/LLM router.

COMPLEX_MARKERS = [
    "compare", "analyze", "architecture", "debug", "optimize",
    "design", "trade-off", "tradeoff", "code", "algorithm",
    "multiple", "step by step", "deep dive", "why does", "calculate"
]

def route(query: str):
    q = query.lower()
    score = 0
    score += min(len(query) / 120, 2)
    score += sum(1 for x in COMPLEX_MARKERS if x in q)
    return "large" if score >= 2.0 else "small"
