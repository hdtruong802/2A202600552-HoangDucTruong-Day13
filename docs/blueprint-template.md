# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: HoangDucTruong-Individual
- [REPO_URL]: https://github.com/hdtruong802/2A202600552-HoangDucTruong-Day13
- [MEMBERS]:
  - Member A: Hoang Duc Truong | Role: Logging & PII
  - Member B: Hoang Duc Truong | Role: Tracing & Enrichment
  - Member C: Hoang Duc Truong | Role: SLO & Alerts
  - Member D: Hoang Duc Truong | Role: Load Test & Dashboard
  - Member E: Hoang Duc Truong | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 50
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/correlation_id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii_redaction.png
- [EVIDENCE_LANGFUSE_TRACES_SCREENSHOT]: docs/evidence/langfuse_traces.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/langfuse_waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: Trace waterfall hiển thị span `run` (agent) gồm retrieve (RAG) và LLM generate. Khi `rag_slow` bật, span retrieve kéo dài ~2.5s làm P95 tăng — dùng correlation_id `req-445c9647` để liên kết log với trace.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/evidence/dashboard_6_panels.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150ms |
| Error Rate | < 2% | 28d | 0.0% |
| Cost Budget | < $2.5/day | 1d | $0.058 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/evidence/alert_rules.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Latency tăng từ ~150ms lên ~2651ms; metrics P95/P99 spike sau khi enable incident.
- [ROOT_CAUSE_PROVED_BY]: correlation_id `req-445c9647` trong log + `mock_rag.py` sleep 2.5s khi `STATE['rag_slow']=True` (xem docs/evidence/incident_rag_slow.json)
- [FIX_ACTION]: `POST /incidents/rag_slow/disable` — latency trở về ~150ms
- [PREVENTIVE_MEASURE]: Alert `high_latency_p95` (latency_p95_ms > 5000 for 30m) với runbook kiểm tra RAG span và incident toggle

---

## 5. Individual Contributions & Evidence

### Hoang Duc Truong
- [TASKS_COMPLETED]:
  - Correlation ID middleware (`app/middleware.py`)
  - Log enrichment với user_id_hash, session_id, feature, model, env (`app/main.py`)
  - PII scrubbing processor + patterns passport/address VN (`app/logging_config.py`, `app/pii.py`)
  - Metrics time-series + error_rate (`app/metrics.py`)
  - 6-panel dashboard (`static/dashboard.html`, `/dashboard`)
  - Audit logs tách riêng (`data/audit.jsonl`)
  - Scripts: `collect_evidence.py`, `run_incident_drill.py`, `check_langfuse.py`
  - Incident drill rag_slow + RCA
- [EVIDENCE_LINK]: https://github.com/hdtruong802/2A202600552-HoangDucTruong-Day13/commits/main (eb89fd5..98368b0)

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: N/A
- [BONUS_AUDIT_LOGS]: Audit log riêng tại `data/audit.jsonl` — ghi `incident_enabled`/`incident_disabled` với actor `control_api`
- [BONUS_CUSTOM_METRIC]: N/A
