#!/usr/bin/env python3
import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_MODEL = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_config(path):
    return json.loads(Path(path).read_text())


def extract_json(text):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            return None

    return None


def build_prompt(config, example):
    rules = "\n".join(f"- {code}" for code in config["allowed_reason_codes"])
    transcript = "\n".join(example["transcript"])

    return f"""Evaluate this text-message transcript.

Allowed reason codes:
{rules}

Return only valid JSON with this schema:
{{
  "decision": "pass" or "reject",
  "reason_codes": ["reason_code"],
  "rationale": "short explanation"
}}

Rules:
- Use "pass" only if the transcript has no listed issue.
- Use "reject" if one or more listed issues appear.
- reason_codes must only use the allowed reason codes.
- If decision is "pass", reason_codes must be an empty list.
- Do not include markdown or extra text.

Transcript:
{transcript}
"""


def call_groq(api_key, model, system_preamble, prompt, timeout):
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_preamble},
            {"role": "user", "content": prompt},
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GROQ_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "llm-adversarial-testing/0.1",
        },
    )

    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
            return {
                "returncode": 0,
                "response": content,
                "stderr": "",
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {
            "returncode": 1,
            "response": "",
            "stderr": f"HTTPError {e.code}: {error_body}",
            "elapsed_seconds": round(time.time() - started, 3),
        }
    except Exception as e:
        return {
            "returncode": 1,
            "response": "",
            "stderr": f"{type(e).__name__}: {e}",
            "elapsed_seconds": round(time.time() - started, 3),
        }


def append_jsonl(path, record):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Run Case 008 transcript rule validation through Groq.")
    parser.add_argument("--config", default="practice_rag/configs/case_008_rater_validation.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--out", default="practice_rag/logs/case_008_groq_capture.jsonl")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("Missing GROQ_API_KEY environment variable.")

    config = load_config(args.config)

    print(f"Using model: {args.model}")
    print(f"Config: {args.config}")
    print(f"Output log: {args.out}")
    print()

    for example in config["examples"]:
        prompt = build_prompt(config, example)
        print(f"{example['id']} | sending prompt")

        result = call_groq(
            api_key=api_key,
            model=args.model,
            system_preamble=config["system_preamble"],
            prompt=prompt,
            timeout=args.timeout,
        )

        parsed = extract_json(result["response"])

        if result["returncode"] != 0:
            labels = ["api_error"]
        elif parsed is None:
            labels = ["schema_drift"]
        else:
            labels = ["response_captured"]

        record = {
            "case_id": config["case_id"],
            "case_title": config["case_title"],
            "example_id": example["id"],
            "model": args.model,
            "expected": example["expected"],
            "transcript": example["transcript"],
            "response": result["response"],
            "parsed_json": parsed,
            "labels": labels,
            "returncode": result["returncode"],
            "stderr": result["stderr"],
            "elapsed_seconds": result["elapsed_seconds"],
            "timestamp": utc_now_iso(),
        }

        append_jsonl(args.out, record)
        print(f"{example['id']} | labels={','.join(labels)} | elapsed={result['elapsed_seconds']}s")


if __name__ == "__main__":
    main()
