import requests

OLLAMA_URL = "http://localhost:11434"

SMALL_MODEL = "llama3.2:1b"
LARGE_MODEL = "llama3.2:3b"


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

    # Local Ollama = $0 API cost
    cost = 0.0

    return answer, model, input_tokens, output_tokens, cost
