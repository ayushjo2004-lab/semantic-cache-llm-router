# Semantic Cache + Cost-Aware LLM Router

A fast portfolio project demonstrating three production-oriented ideas:

1. **Semantic caching** — reuse an answer when a new query is semantically similar to a cached query.
2. **Cost-aware routing** — send simple requests to a cheaper/smaller model and complex requests to a larger model.
3. **Observability** — record cache hits, model choice, latency, token usage and estimated cost.

## Architecture

User → Embedding → Semantic Cache → Router → Small/Large LLM → Metrics

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Put your API key in .env

uvicorn app.main:app --reload
```

In another terminal:

```bash
streamlit run dashboard/app.py
```

API docs:
`http://localhost:8000/docs`

## Test

```bash
pytest
```

Run the evaluation after starting the API:

```bash
cd evaluation
python evaluate.py
```

## Interview explanation

"The system first embeds each incoming query and compares it with cached embeddings. If similarity crosses a configurable threshold, it returns the cached response and avoids an LLM generation call. Otherwise a lightweight routing layer estimates query complexity and chooses either a cheaper model or a more capable model. Every request records latency, cache status, model, tokens and estimated cost, which feeds the dashboard."

## Important MVP note

The similarity lookup is intentionally implemented with SQLite + cosine similarity so the project can be built quickly. For production scale, replace this with Redis/pgvector/Pinecone/another vector index and add cache expiry, concurrency controls, auth, rate limits and robust evaluation.
