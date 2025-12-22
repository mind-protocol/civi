# audio_runtime_windows — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Windows player runs queue with no overlap.
- Playback is non-blocking for the main pipeline.

**What's still being designed:**
- Ducking policy for layered audio.
- Warmup behavior for voices.

**What's proposed (v2+):**
- Crossfade and prioritization rules.

---

## CURRENT STATE

Audio runtime now includes a queue player stub and tests for queue behavior.

---

## IN PROGRESS

### Low latency player contract

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define queue, stop/replay, and no-overlap invariants.

---

## RECENT CHANGES

### 2025-12-21: Seed audio_runtime_windows docs

- **What:** Added initial objectives, algorithm, validation, implementation, and health notes.
- **Why:** Lock Windows-first playback rules.
- **Files:** `docs/civ6_living_narrator/audio_runtime_windows/`
- **Struggles/Insights:** Keep playback async and reliable.

### 2025-12-21: Implement audio queue stub

- **What:** Added in-process queue player stub, config file, and tests for enqueue/stop/replay.
- **Why:** Establish no-overlap queue behavior before IPC wiring.
- **Files:** `runtime_windows/audio_player/audio_queue_player.py`, `runtime_windows/audio_player/config_player.yaml`, `tests/test_audio_queue_player.py`
- **Struggles/Insights:** Python import required a .py file for tests.

---

## KNOWN ISSUES

### Player API undefined

- **Severity:** medium
- **Symptom:** No IPC contract for player process.
- **Suspected cause:** Implementation not drafted.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Queue stub and tests are in place.

**What you need to understand:**
Audio should not overlap; queue control must be explicit.

**Watch out for:**
Blocking calls in the main pipeline.

**Open questions I had:**
How to expose player status and queue depth?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Audio runtime now has a queue stub and tests for basic playback controls.

**Decisions made:**
No overlap and non-blocking playback are hard rules.

**Needs your input:**
Confirm player IPC protocol and warmup behavior.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: implement IPC wiring and actual audio playback.

### Tests to Run

```bash
pytest tests/test_audio_queue_player.py
```

### Immediate

- [ ] Define IPC commands (queue, stop, replay).
- [ ] Define warmup sequence.

### Later

- [ ] Add ducking policy.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to keep audio latency low across TTS calls.

**Intuitions:**
Warmup at startup avoids first-line lag.

**What I wish I'd known at the start:**
Preferred TTS engine for Windows.

---

## POINTERS

| What | Where |
|------|-------|
| Player stub | `runtime_windows/audio_player/audio_queue_player.py` |
| Config stub | `runtime_windows/audio_player/config_player.yaml` |
