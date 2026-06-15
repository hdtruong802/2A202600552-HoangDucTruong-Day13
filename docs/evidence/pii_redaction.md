# PII Redaction Evidence

Input message contained: `student@vinuni.edu.vn`

Logged preview (scrubbed):

```json
{
  "payload": {
    "message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"
  }
}
```

Patterns in `app/pii.py`: email, phone_vn, cccd, credit_card, passport, address_vn
