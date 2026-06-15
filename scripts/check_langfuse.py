"""Check Langfuse configuration and trace connectivity."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
secret = os.getenv("LANGFUSE_SECRET_KEY", "")
host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")


def count_traces(limit: int = 100) -> int:
    r = httpx.get(
        f"{host}/api/public/traces",
        auth=httpx.BasicAuth(public, secret),
        params={"limit": limit},
        timeout=30.0,
    )
    r.raise_for_status()
    payload = r.json()
    data = payload.get("data", [])
    return len(data) if isinstance(data, list) else 0


def main() -> None:
    if not public or not secret:
        print("Langfuse keys missing in .env")
        print("Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY, then restart uvicorn.")
        sys.exit(1)

    try:
        trace_count = count_traces()
        print(f"Langfuse OK — host={host}")
        print(f"Traces found: {trace_count}")
        if trace_count < 10:
            print("Need >= 10 traces. Run: python scripts/load_test.py --concurrency 3")
            sys.exit(1)
        print("Tracing requirement met (>= 10 traces).")
    except Exception as exc:
        print(f"Langfuse check failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
