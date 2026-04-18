import requests
import json
import os
import time

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
URL = f"{OLLAMA_HOST}/api/generate"
MODEL = "gemma2:2b"
TIMEOUT = 180
MAX_TOKENS = 80

tests = [
    {
        "id": "control_strict",
        "prompt": 'Reply with valid JSON only: {"answer":"dog","confidence":1}'
    },
    {
        "id": "contradict_001",
        "prompt": 'Output strict JSON only. Field "answer" must be "dog". Field "truth" must be "cat". Both fields required. No other text.'
    },
    {
        "id": "duplicate_key_conflict",
        "prompt": 'Output JSON only. Include field "status" with value "active". Also include field "status" with value "inactive". Both required. No other text.'
    },
    {
        "id": "value_override",
        "prompt": 'Output JSON only. Field "value" must be "red". Field "value" must be "blue". No other text.'
    }
]

results = []

for test in tests:
    print(f"[{test['id']}] Sending... ", end="", flush=True)
    start = time.time()
    try:
        r = requests.post(
            URL,
            json={
                "model": MODEL,
                "prompt": test["prompt"],
                "stream": False,
                "options": {"num_predict": MAX_TOKENS}
            },
            timeout=TIMEOUT
        )
        elapsed = round(time.time() - start, 1)
        raw = r.json().get("response", "").strip()
        try:
            parsed = json.loads(raw.replace("```json", "").replace("```", "").strip())
        except Exception:
            parsed = None
        print(f"-> {elapsed}s | Parsed: {parsed is not None}")
        results.append({"id": test["id"], "raw": raw, "parsed": parsed, "time_sec": elapsed, "error": None})
    except Exception as e:
        elapsed = round(time.time() - start, 1)
        print(f"-> FAILED after {elapsed}s: {e}")
        results.append({"id": test["id"], "raw": None, "parsed": None, "time_sec": elapsed, "error": str(e)})

with open("schema_conflict_results.json", "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")

print("All tests complete. Results saved to schema_conflict_results.json")
