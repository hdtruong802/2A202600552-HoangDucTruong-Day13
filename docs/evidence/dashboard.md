# Dashboard Evidence

6-panel dashboard is served at: **http://127.0.0.1:8000/dashboard**

Panels:
1. Latency P50/P95/P99 (ms) — SLO line at 3000ms
2. Traffic (requests)
3. Error rate (%) — SLO line at 2%
4. Cost over time (USD) — daily budget SLO $2.50
5. Tokens in / out
6. Quality proxy (avg score) — SLO line at 0.75

Auto-refresh: 20 seconds. Data source: `/metrics` and `/metrics/timeseries`.

Screenshot: `docs/evidence/dashboard_6_panels.png`
