"""Run rag_slow incident drill and capture before/after metrics."""
from __future__ import annotations

import json
import time
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
EVIDENCE_DIR = Path(__file__).resolve().parent.parent / "docs" / "evidence"
PAYLOAD = {
    "user_id": "u_incident",
    "session_id": "s_incident",
    "feature": "qa",
    "message": "Explain monitoring policy and refund rules",
}


def snapshot(client: httpx.Client) -> dict:
    return client.get(f"{BASE_URL}/metrics").json()


def send_chat(client: httpx.Client) -> dict:
    r = client.post(f"{BASE_URL}/chat", json=PAYLOAD)
    r.raise_for_status()
    return r.json()


def main() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    report: dict = {"scenario": "rag_slow", "steps": []}

    with httpx.Client(timeout=60.0) as client:
        before = snapshot(client)
        baseline = send_chat(client)
        report["steps"].append({"phase": "baseline", "metrics": before, "response": baseline})

        client.post(f"{BASE_URL}/incidents/rag_slow/enable").raise_for_status()
        time.sleep(0.5)
        during = snapshot(client)
        slow = send_chat(client)
        report["steps"].append({"phase": "incident_active", "metrics": during, "response": slow})

        client.post(f"{BASE_URL}/incidents/rag_slow/disable").raise_for_status()
        time.sleep(0.5)
        after = snapshot(client)
        recovered = send_chat(client)
        report["steps"].append({"phase": "recovered", "metrics": after, "response": recovered})

    report["analysis"] = {
        "symptom": "latency_p95 spiked when rag_slow was enabled",
        "baseline_latency_ms": report["steps"][0]["response"]["latency_ms"],
        "incident_latency_ms": report["steps"][1]["response"]["latency_ms"],
        "correlation_id_during_incident": report["steps"][1]["response"]["correlation_id"],
        "root_cause": "retrieve() sleeps 2.5s when STATE['rag_slow'] is True (mock_rag.py)",
        "debug_flow": "Metrics (P95↑) → Traces (slow RAG span) → Logs (correlation_id links request)",
        "fix_action": "POST /incidents/rag_slow/disable",
        "preventive_measure": "Alert on latency_p95 > 5000ms with runbook docs/alerts.md#1-high-latency-p95",
    }

    out = EVIDENCE_DIR / "incident_rag_slow.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Incident drill report: {out}")
    print(json.dumps(report["analysis"], indent=2))


if __name__ == "__main__":
    main()
