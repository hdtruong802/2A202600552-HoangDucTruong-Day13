# Correlation ID Evidence

Sample log line from `data/logs.jsonl`:

```json
{
  "service": "api",
  "correlation_id": "req-38b13443",
  "user_id_hash": "2055254ee30a",
  "session_id": "s01",
  "feature": "qa",
  "model": "claude-sonnet-4-5",
  "env": "dev",
  "event": "request_received",
  "level": "info"
}
```

Response header: `x-request-id: req-38b13443`, `x-response-time-ms: <ms>`
