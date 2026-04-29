import requests
from utils import safe_json_loads

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma"

PROMPT_TEMPLATE = """
Extract structured order data from the message.

Schema:
{{
  "person": string,
  "expenses": [
    {{"name": string, "amount": integer}}
  ]
}}

Rules:
- Extract item/service name
- Extract total price in integer (Rupiah, no dots/commas)
- If currency mentioned like 50k → convert to 50000
- If multiple items, separate them
- If no name, use "unknown"

Message:
{message}
"""

def extract_order(message: str):
    prompt = PROMPT_TEMPLATE.format(message=message)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    text_output = result.get("response", "")

    print("\n🧠 RAW MODEL OUTPUT:")
    print(text_output)

    return safe_json_loads(text_output)