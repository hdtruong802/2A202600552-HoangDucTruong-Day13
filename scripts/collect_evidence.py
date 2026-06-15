"""Collect lab evidence snippets for blueprint report."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
LOG_PATH = ROOT / "data" / "logs.jsonl"
AUDIT_PATH = ROOT / "data" / "audit.jsonl"
EVIDENCE_DIR = ROOT / "docs" / "evidence"
BASE_URL = "http://127.0.0.1:8000"


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def main() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_logs.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    (EVIDENCE_DIR / "validate_logs.txt").write_text(validate.stdout + validate.stderr, encoding="utf-8")

    logs = _read_jsonl(LOG_PATH)
    api_logs = [r for r in logs if r.get("service") == "api"]
    correlation_sample = next((r for r in api_logs if r.get("correlation_id")), {})
    pii_sample = next((r for r in api_logs if "REDACTED" in json.dumps(r)), {})

    metrics = {}
    health = {}
    try:
        with httpx.Client(timeout=10.0) as client:
            metrics = client.get(f"{BASE_URL}/metrics").json()
            health = client.get(f"{BASE_URL}/health").json()
    except httpx.HTTPError as exc:
        metrics = {"error": str(exc)}
        health = {"error": str(exc)}

    audit_logs = _read_jsonl(AUDIT_PATH)

    trace_count = 0
    public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret = os.getenv("LANGFUSE_SECRET_KEY", "")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    if public and secret:
        try:
            r = httpx.get(
                f"{host}/api/public/traces",
                auth=httpx.BasicAuth(public, secret),
                params={"limit": 100},
                timeout=30.0,
            )
            r.raise_for_status()
            data = r.json().get("data", [])
            trace_count = len(data) if isinstance(data, list) else 0
        except httpx.HTTPError:
            trace_count = -1

    summary = {
        "validate_logs_output": validate.stdout.strip(),
        "correlation_id_sample": correlation_sample,
        "pii_redaction_sample": pii_sample,
        "metrics_snapshot": metrics,
        "health": health,
        "audit_log_count": len(audit_logs),
        "audit_log_sample": audit_logs[-3:] if audit_logs else [],
        "unique_correlation_ids": len({r.get("correlation_id") for r in logs if r.get("correlation_id")}),
        "tracing_enabled": health.get("tracing_enabled", False),
        "langfuse_trace_count": trace_count,
    }

    (EVIDENCE_DIR / "lab_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Evidence written to docs/evidence/")
    print(f"  - validate_logs.txt")
    print(f"  - lab_summary.json")
    print(f"  - tracing_enabled: {summary['tracing_enabled']}")
    print(f"  - langfuse_trace_count: {summary['langfuse_trace_count']}")


if __name__ == "__main__":
    main()
