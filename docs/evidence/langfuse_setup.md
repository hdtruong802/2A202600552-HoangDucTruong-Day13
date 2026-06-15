# Langfuse Tracing — Completed

- `tracing_enabled`: **true**
- Traces on Langfuse: **30+** (verified by `python scripts/check_langfuse.py`)
- Fix applied: migrated `app/tracing.py` from deprecated `langfuse.decorators` to Langfuse 3.x (`from langfuse import observe, get_client`)

## Verify locally

```bash
python scripts/check_langfuse.py
python scripts/load_test.py --concurrency 3
```

View traces: https://cloud.langfuse.com

Screenshots saved:
- `docs/evidence/langfuse_traces.png`
- `docs/evidence/langfuse_waterfall.png`
