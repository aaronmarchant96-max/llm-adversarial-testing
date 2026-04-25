#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def load_cases(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def append_jsonl(path: Path, record):
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def print_progress(message):
    print(message, flush=True)


def truncate_for_context(text: str, max_chars: int = 350) -> str:
    collapsed = " ".join((text or "").strip().split())
    return collapsed[:max_chars]


def build_prompt(system_preamble, seed_prompt, transcript, current_prompt, final_json_instruction=None):
    lines = []
    lines.append(system_preamble.strip())
    lines.append("")
    lines.append(f"Conversation seed: {seed_prompt.strip()}")
    lines.append("")
    lines.append("Transcript so far:")

    if transcript:
        for idx, item in enumerate(transcript, start=1):
            lines.append(f"User turn {idx}: {item['user']}")
            lines.append(f"Model turn {idx}: {item['assistant']}")
    else:
        lines.append("<empty>")

    lines.append("")
    lines.append(f"Current user turn: {current_prompt.strip()}")
    if final_json_instruction:
        lines.append(final_json_instruction.strip())
    lines.append("")
    lines.append("Respond to the current user turn only.")
    return "\n".join(lines)


def extract_json_candidate(text: str):
    stripped = (text or "").strip()
    if not stripped:
        return None
    first_obj = stripped.find("{")
    last_obj = stripped.rfind("}")
    if first_obj != -1 and last_obj != -1 and last_obj > first_obj:
        return stripped[first_obj:last_obj + 1].strip()
    return None


def parse_json_if_possible(response_text: str):
    candidate = extract_json_candidate(response_text)
    if not candidate:
        return None
    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def run_groq_chat(model: str, prompt: str, api_key: str, timeout_seconds: int):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "llm-adversarial-testing/0.1",
        },
        method="POST",
    )

    started = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout_seconds) as resp:
            elapsed = round(time.perf_counter() - started, 3)
            raw = resp.read().decode("utf-8")
            decoded = json.loads(raw)
            content = (
                decoded.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            return {
                "response": (content or "").strip(),
                "returncode": 0,
                "stderr": "",
                "elapsed_seconds": elapsed,
                "timed_out": False,
            }
    except error.HTTPError as exc:
        elapsed = round(time.perf_counter() - started, 3)
        details = ""
        try:
            details = exc.read().decode("utf-8")
        except Exception:
            details = str(exc)
        return {
            "response": "",
            "returncode": 1,
            "stderr": f"HTTPError {exc.code}: {details}",
            "elapsed_seconds": elapsed,
            "timed_out": False,
        }
    except Exception as exc:
        elapsed = round(time.perf_counter() - started, 3)
        return {
            "response": "",
            "returncode": 1,
            "stderr": str(exc),
            "elapsed_seconds": elapsed,
            "timed_out": False,
        }


def run_case_variant(case, variant_name, shared, model, timeout_seconds, out_path, api_key):
    run_id = f"{case['case_id']}_{variant_name}_{uuid.uuid4().hex[:8]}"
    transcript = []
    turns = case["variants"][variant_name]
    total_turns = len(turns)
    print_progress(f"\n=== Running {case['case_id']} [{variant_name}] as {run_id} ===")

    for turn_def in turns:
        turn_number = turn_def["turn"]
        expects_json = bool(turn_def.get("expects_json", False))
        current_prompt = turn_def["prompt"]
        final_json_instruction = shared.get("final_json_instruction") if expects_json else None
        case_system_preamble = case.get("system_preamble") or shared.get("system_preamble", "")

        prompt = build_prompt(
            system_preamble=case_system_preamble,
            seed_prompt=case["seed_prompt"],
            transcript=transcript,
            current_prompt=current_prompt,
            final_json_instruction=final_json_instruction,
        )

        print_progress(f"[{run_id}] turn {turn_number}/{total_turns} | vector={turn_def['attack_vector']} | sending prompt")
        run_result = run_groq_chat(
            model=model,
            prompt=prompt,
            api_key=api_key,
            timeout_seconds=timeout_seconds,
        )
        response = run_result["response"]
        parsed_json = parse_json_if_possible(response) if expects_json else None
        if run_result["returncode"] != 0:
            labels = ["api_error"]
        elif response:
            labels = ["response_captured"]
        else:
            labels = ["collapse"]

        record = {
            "run_id": run_id,
            "case_id": case["case_id"],
            "case_title": case["title"],
            "variant": variant_name,
            "turn": turn_number,
            "total_turns": total_turns,
            "attack_vector": turn_def["attack_vector"],
            "model": model,
            "input": current_prompt,
            "response": response,
            "returncode": run_result["returncode"],
            "stderr": run_result["stderr"],
            "elapsed_seconds": run_result["elapsed_seconds"],
            "labels": labels,
            "parsed_json": parsed_json,
            "timestamp": utc_now_iso(),
        }

        append_jsonl(out_path, record)
        print_progress(
            f"[{run_id}] turn {turn_number}/{total_turns} | labels={','.join(labels)} | elapsed={run_result['elapsed_seconds']:.3f}s"
        )

        transcript.append({
            "user": current_prompt,
            "assistant": truncate_for_context(response, 350),
        })


def parse_args():
    parser = argparse.ArgumentParser(description="Run a single arena case variant using Groq chat completions.")
    default_cases = Path(__file__).resolve().parents[1] / "configs" / "arena_cases.json"
    default_out = Path(__file__).resolve().parents[1] / "logs" / "arena_runs_groq.jsonl"
    parser.add_argument("--case-id", default=None, help="Run only one case_id")
    parser.add_argument("--variant", choices=["control", "pressure", "all"], default="all", help="Which variant to run")
    parser.add_argument("--model", default="llama-3.1-8b-instant", help="Groq model name")
    parser.add_argument("--out", default=str(default_out), help="JSONL output path")
    parser.add_argument("--cases", default=str(default_cases), help="Path to arena_cases.json")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds")
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Missing GROQ_API_KEY environment variable.", file=sys.stderr)
        return 1

    cases_path = Path(args.cases)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("", encoding="utf-8")
    if not cases_path.exists():
        print(f"Cases file not found: {cases_path}", file=sys.stderr)
        return 1

    config = load_cases(cases_path)
    shared = config["shared"]
    selected_cases = config.get("cases", [])
    if args.case_id:
        selected_cases = [case for case in selected_cases if case.get("case_id") == args.case_id]

    if not selected_cases:
        print("No matching cases found.", file=sys.stderr)
        return 1

    variants = ["control", "pressure"] if args.variant == "all" else [args.variant]

    print_progress(f"Using model: {args.model}")
    print_progress(f"Cases file: {cases_path}")
    print_progress(f"Output log: {out_path}")
    print_progress(f"Timeout: {args.timeout}s")

    for case in selected_cases:
        for variant_name in variants:
            if variant_name not in case.get("variants", {}):
                print_progress(f"Skipping {case['case_id']} variant {variant_name}: not defined")
                continue
            run_case_variant(
                case=case,
                variant_name=variant_name,
                shared=shared,
                model=args.model,
                timeout_seconds=args.timeout,
                out_path=out_path,
                api_key=api_key,
            )

    print_progress("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
