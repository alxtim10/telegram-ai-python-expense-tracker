import requests
from utils import safe_json_loads
from utils import normalize_category


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"

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

Message:
{message}
"""

def extract_order(message: str):
    prompt = f"""
Extract expense from this message.

Return JSON:
{{"expenses":[{{"name":string,"amount":integer,"category":string}}]}}

Rules:
- Only extract what exists in the message
- Do not invent data
- One expense → one item
- Convert 25k=25000
- If no expense → return empty list

Example:
Message: aku beli nasi goreng 20000
Output: {{"expenses":[{{"name":"nasi goreng","amount":20000,"category":"food"}}]}}

Message:
{message}
"""

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