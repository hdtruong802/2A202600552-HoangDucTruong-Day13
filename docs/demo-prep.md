# Live Demo Cheat Sheet — Day 13

## Start (30 giây)

```powershell
uvicorn app.main:app --reload
python scripts/check_langfuse.py
```

- Health: http://127.0.0.1:8000/health → `tracing_enabled: true`
- Dashboard: http://127.0.0.1:8000/dashboard

## Demo flow đề xuất (5–7 phút)

### 1. Logging pipeline (2 phút)
- Mở `app/middleware.py`: giải thích `clear_contextvars` → `correlation_id` → bind structlog → response headers
- Mở `app/main.py`: `bind_contextvars` enrich user/session/feature/model/env
- Show `docs/evidence/correlation_id.png` + `pii_redaction.png`

### 2. Tracing (1–2 phút)
- Show `docs/evidence/langfuse_traces.png` (50+ traces)
- Show `docs/evidence/langfuse_waterfall.png` — span `run`, tags metadata

### 3. Metrics & Dashboard (1 phút)
- Show `docs/evidence/dashboard_6_panels.png` — 6 panels + SLO lines

### 4. Incident drill (2 phút)
```powershell
python scripts/inject_incident.py --scenario rag_slow
python scripts/load_test.py
python scripts/inject_incident.py --scenario rag_slow --disable
```
- Flow: **Metrics** (P95↑) → **Traces** (RAG chậm) → **Logs** (`correlation_id`)
- RCA: `docs/evidence/incident_rag_slow.json`

### 5. Alerts (30 giây)
- Show `docs/evidence/alert_rules.png` → runbook `docs/alerts.md#1-high-latency-p95`

## Câu hỏi hay gặp

| Câu hỏi | Trả lời ngắn |
|---|---|
| P95 là gì? | 95% request có latency ≤ giá trị đó; tính trong `app/metrics.py` |
| PII regex ở đâu? | `app/pii.py` — email, phone, cccd, passport, address_vn |
| Tại sao rag_slow? | `mock_rag.py` sleep 2.5s khi `STATE['rag_slow']=True` |
| Audit log khác gì? | `data/audit.jsonl` — chỉ incident enable/disable, tách khỏi app logs |
