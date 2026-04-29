import requests
from utils import safe_json_loads
from utils import normalize_category


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma"

PROMPT_TEMPLATE = """
Extract structured order data from the message.

Schema:
{{
  "expenses": [
    {{
      "name": string,
      "amount": integer,
      "category": string
    }}
  ]
}}

Categories:
- food
- transport
- shopping
- bills
- entertainment
- other

Rules:
- Extract item/service name
- Extract total price in integer (Rupiah, no dots/commas)
- Convert formats: 25k=25000, 10rb=10000, 1jt=1000000
- If multiple items, separate them
- If no name, use "unknown"
- Assign the most relevant category
- If unsure → use "other"

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
    parsed = safe_json_loads(text_output)

    print("\n🧠 RAW MODEL OUTPUT:")
    print(text_output)

    return post_process(parsed)

def post_process(data: dict):
    for item in data.get("expenses", []):
        if not item.get("category"):
            item["category"] = normalize_category(item.get("name", ""))

    return data