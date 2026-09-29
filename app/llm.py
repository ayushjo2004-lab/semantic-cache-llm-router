import requests

OLLAMA_URL = "http://localhost:11434"

SMALL_MODEL = "llama3.2:1b"
LARGE_MODEL = "llama3.2:3b"

# Reference pricing used for cost estimation.
# Ollama runs locally, so these are NOT actual charges.
MODEL_COST_PER_1K_TOKENS = {
    "llama3.2:1b": 0.0001,
    "llama3.2:3b": 0.0003,
}

def ask(query: str, route_name: str):

    model = SMALL_MODEL if route_name == "small" else LARGE_MODEL

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer clearly and concisely. If the request is technical, provide practical explanations."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()

    data = response.json()

    answer = data["message"]["content"]

    input_tokens = data.get("prompt_eval_count", 0)
    output_tokens = data.get("eval_count", 0)

    # Calculate estimated reference cost.
    # Ollama runs locally, so this is NOT an actual API charge.
    total_tokens = input_tokens + output_tokens

    cost_per_1k = MODEL_COST_PER_1K_TOKENS.get(model, 0.0)

    cost = (total_tokens / 1000) * cost_per_1k

    return answer, model, input_tokens, output_tokens, cost