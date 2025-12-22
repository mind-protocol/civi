# audio_runtime_windows — Health: Queue depth and stutter rate

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| queue_depth | low | Sustained growth indicates backlog |
| stutter_rate | 0 | Stutters indicate playback issues |
| audio_latency_ms | < 1000 | End-to-end playback latency |

---

## ALERTS

- queue_depth > 3 for 2 minutes.
- stutter_rate spikes above threshold.
