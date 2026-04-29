import requests
from utils import safe_json_loads
from utils import normalize_category


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma"

PROMPT_TEMPLATE = """
You are an API that extracts daily expenses from Indonesian messages.

Return ONLY valid JSON. No explanation.

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

Examples:

Message: aku beli kopi 25k
Output:
{{"expenses":[{{"name":"kopi","amount":25000,"category":"food"}}]}}

Message: naik gojek 15000
Output:
{{"expenses":[{{"name":"gojek","amount":15000,"category":"transport"}}]}}

Message:
{message}
"""

def extract_order(message: str):
    prompt = f"""
Extract expenses from this Indonesian message.

Return JSON ONLY:
{{"expenses":[{{"name":string,"amount":integer,"category":string}}]}}

Rules:
- Must include price
- Convert: 25k=25000, 10rb=10000, 1jt=1000000
- No price → return empty list

Example:
Message: aku beli kopi 25k
Output: {{"expenses":[{{"name":"kopi","amount":25000,"category":"food"}}]}}

Message: aku ngobrol doang
Output: {{"expenses":[]}}

Message:
{message}
"""

    print("INPUT:", message)
    print("OUTPUT:", response)

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