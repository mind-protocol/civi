# ingest — Implementation: File watcher and parsers

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Tail reader | `src/ingest/civ6_jsonl_tail_reader.py` |
| Parser and normalizer | `src/ingest/raw_event_parser_and_normalizer.py` |
| Dedup and coalesce | `src/ingest/event_deduplicator_and_coalescer.py` |

---

## DATA FLOW

1. Tail reader yields raw JSON lines.
2. Parser normalizes into EventNormalized records.
3. Dedup/coalesce filters and emits final events.
4. Telemetry reports ingest lag and error counts.

---

## CONFIG

- `config/config.yaml`: ingest polling interval and dedup windows.
- `config/event_schema.yaml`: required fields, aliases, unknown handling.
- `config/token_map.yaml`: token compression rules (optional).

---

## NOTES

Use non-blocking reads and tolerate partial lines by buffering.
