# OBJECTIFS — Lua Mod: Event Extraction and Emission

```
STATUS: DRAFT
CREATED: 2025-12-22
VERIFIED: n/a (not yet implemented)
```

## PRIMARY OBJECTIVES (ranked)

1. **Reliable event capture** — never miss a significant game event that the narrator might want to comment on.
2. **Minimal game impact** — zero perceptible lag or interference with normal gameplay.
3. **Clean append-only output** — produce valid JSONL that the WSL pipeline can tail without corruption.

## NON-OBJECTIVES

- Exhaustive logging of every micro-action (unit selection, camera movement).
- Interpreting or filtering events — that's the decision engine's job.
- Audio playback or TTS — that lives on the Windows runtime side.

## TRADEOFFS (canonical decisions)

- When in doubt about whether to emit an event, **emit it** — the pipeline will filter.
- Prefer simpler event schemas over richer ones to reduce mod complexity.
- Accept slight redundancy in events rather than complex deduplication in Lua.

## SUCCESS SIGNALS (observable)

- Events appear in `events.jsonl` within the same frame they occur.
- Game FPS remains unaffected with mod enabled.
- JSONL file never contains malformed lines (valid JSON per line).
