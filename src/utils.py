import json
import re

def safe_json_loads(text):
    if not text:
        return {}

    # 🔹 Remove ```json ... ``` wrappers
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # 🔹 Extract JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}

    json_str = match.group()

    try:
        return json.loads(json_str)
    except Exception as e:
        print("❌ JSON parse error:", e)
        return {}