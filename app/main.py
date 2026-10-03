import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .db import init_db, add_cache, log_request, request_stats
from .embeddings import embed
from .cache import find_similar
from .router import route
from .llm import ask
from .config import CACHE_THRESHOLD, MAX_ROUTE_COST

init_db()
app = FastAPI(title="Semantic Cache + Cost-Aware LLM Router", version="1.0")

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(body: Query):
    if not body.query.strip():
        raise HTTPException(400, "Query cannot be empty")

    start = time.perf_counter()
    embedding = embed(body.query)
    cached = find_similar(embedding, CACHE_THRESHOLD)

    if cached:
        answer = cached["answer"]
        model = cached["model"]
        latency = (time.perf_counter() - start) * 1000
        log_request(body.query, model, True, latency, 0, 0, 0)
        return {
            "answer": answer, "model": model, "cache_hit": True,
            "route": "cached",
            "similarity": round(cached["score"], 4),
            "latency_ms": round(latency, 2),
            "input_tokens": 0,
            "output_tokens": 0,
            "estimated_cost": 0,
        }

    route_name = route(body.query, MAX_ROUTE_COST) 
    answer, model, inp, out, cost = ask(body.query, route_name)
    add_cache(body.query, embedding, answer, model)

    latency = (time.perf_counter() - start) * 1000
    log_request(body.query, model, False, latency, inp, out, cost)

    return {
        "answer": answer,
        "model": model,
        "cache_hit": False,
        "route": route_name,
        "similarity": None,
        "latency_ms": round(latency, 2),
        "input_tokens": inp,
        "output_tokens": out,
        "estimated_cost": round(cost, 8),
    }

@app.get("/metrics")
def metrics():
    s = request_stats()
    return {
        "total_requests": s["total"],
        "cache_hit_rate_percent": round(s["cache_hit_rate"], 2),
        "average_latency_ms": round(s["avg_latency_ms"], 2),
        "estimated_total_cost_usd": round(s["total_cost"], 8),
        "cache_hits": s["hits"],
        "cache_misses": s["total"] - s["hits"],
        "model_usage": s["model_usage"],
        "recent_requests": [
            {
                "query": row[0],
                "model": row[1],
                "cache_hit": bool(row[2]),
                "latency_ms": round(row[3], 2),
                "estimated_cost_usd": round(row[4], 8),
                "created_at": row[5],
            }
            for row in s["recent"]
        ],
    }
