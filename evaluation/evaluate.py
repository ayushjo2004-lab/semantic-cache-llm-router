import json, requests, statistics, time

API = "http://localhost:8000"
data = json.load(open("dataset.json"))

results = []
for item in data:
    t = time.perf_counter()
    r = requests.post(f"{API}/query", json=item, timeout=120)
    elapsed = (time.perf_counter()-t)*1000
    x = r.json()
    results.append(x)
    print(f"{item['query'][:45]:45} | cache={x['cache_hit']} | model={x['model']} | {elapsed:.0f}ms")

hits = sum(x["cache_hit"] for x in results)
print("\\nEvaluation")
print("Queries:", len(results))
print("Cache hits:", hits)
print("Cache hit rate:", round(hits/len(results)*100, 2), "%")
print("Avg latency:", round(statistics.mean(x["latency_ms"] for x in results), 2), "ms")
print("Estimated cost:", round(sum(x["estimated_cost"] for x in results), 6), "USD")
