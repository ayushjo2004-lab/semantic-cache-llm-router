import json, sqlite3, os
from .config import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            embedding TEXT NOT NULL,
            answer TEXT NOT NULL,
            model TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            model TEXT NOT NULL,
            cache_hit INTEGER NOT NULL,
            latency_ms REAL NOT NULL,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            estimated_cost REAL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

def add_cache(query, embedding, answer, model):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO cache(query, embedding, answer, model) VALUES(?,?,?,?)",
            (query, json.dumps(embedding), answer, model)
        )

def get_cache():
    with sqlite3.connect(DB_PATH) as con:
        rows = con.execute("SELECT id, query, embedding, answer, model FROM cache").fetchall()
    return [{"id": r[0], "query": r[1], "embedding": json.loads(r[2]), "answer": r[3], "model": r[4]} for r in rows]

def log_request(query, model, cache_hit, latency_ms, input_tokens, output_tokens, cost):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""INSERT INTO requests
        (query, model, cache_hit, latency_ms, input_tokens, output_tokens, estimated_cost)
        VALUES(?,?,?,?,?,?,?)""",
        (query, model, int(cache_hit), latency_ms, input_tokens, output_tokens, cost))

def request_stats():
    with sqlite3.connect(DB_PATH) as con:
        total, hits, latency, cost = con.execute("""
            SELECT COUNT(*), COALESCE(SUM(cache_hit),0),
                   COALESCE(AVG(latency_ms),0), COALESCE(SUM(estimated_cost),0)
            FROM requests
        """).fetchone()
        rows = con.execute("""
            SELECT query, model, cache_hit, latency_ms, estimated_cost, created_at
            FROM requests ORDER BY id DESC LIMIT 100
        """).fetchall()
    return {
        "total": total, "hits": hits, "cache_hit_rate": (hits/total*100 if total else 0),
        "avg_latency_ms": latency, "total_cost": cost,
        "recent": rows
    }
