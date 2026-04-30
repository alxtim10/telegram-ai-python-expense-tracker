import os
import requests
from dotenv import load_dotenv
from utils import safe_json_loads

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_API_URL")

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
- Extract total price in integer (Rupiah)
- Convert formats: 25k=25000, 10rb=10000, 1jt=1000000
- If multiple items, separate them
- If no name, use "unknown"
- Assign category properly

Message:
{message}
"""


def extract_order(message: str):
    prompt = PROMPT_TEMPLATE.format(message=message)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, json=payload)
    result = response.json()

    # 🔍 Extract text response
    try:
        text_output = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        print("❌ Gemini error:", result)
        return {}

    print("🧠 RAW GEMINI OUTPUT:")
    print(text_output)

    return safe_json_loads(text_output)