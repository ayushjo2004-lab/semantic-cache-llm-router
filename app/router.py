# Cost-aware, explainable routing heuristic.
# The router prefers the cheaper model unless the query
# shows strong signals of complexity.

COMPLEX_MARKERS = [
    "compare", "analyze", "architecture", "debug", "optimize",
    "design", "trade-off", "tradeoff", "code", "algorithm",
    "multiple", "step by step", "deep dive", "why does", "calculate"
]

# Queries with a score below this use the cheaper model.
SMALL_MODEL_THRESHOLD = 2.0

# Queries with a stronger complexity signal can use the
# larger model when additional reasoning is likely needed.
LARGE_MODEL_THRESHOLD = 3.0

MODEL_COSTS = {
    "small": 0.0001,
    "large": 0.0003,
}


def calculate_complexity(query: str) -> float:
    """Calculate an explainable complexity score."""
    q = query.lower()

    score = 0

    # Longer queries generally contain more requirements.
    score += min(len(query) / 120, 2)

    # Add one point for every detected complexity marker.
    score += sum(1 for marker in COMPLEX_MARKERS if marker in q)

    return score


def route(query: str, max_cost: float = 0.0003):
    """Route using complexity and a configurable model budget."""

    score = calculate_complexity(query)

    # Simple queries always use the cheaper model.
    if score < LARGE_MODEL_THRESHOLD:
        return "small"

    # Complex queries can use the larger model when its
    # configured reference rate is within the allowed budget.
    if MODEL_COSTS["large"] <= max_cost:
        return "large"

    # Otherwise fall back to the cheaper model.
    return "small"