# win_wsl_bridge — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Windows-first runtime path with WSL dev tooling.
- Session-based JSONL rotation and tailing.

**What's still being designed:**
- Launcher behavior and auto-restart contract.
- Port exposure for overlay or router.

**What's proposed (v2+):**
- Bidirectional bridge with explicit IPC protocol.

---

## CURRENT STATE

Bridge module now includes session id resolution, path resolution, and rotation helpers with tests.

---

## IN PROGRESS

### Rotation and partial-line handling

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define session rotation, tail offsets, and partial JSON handling.

---

## RECENT CHANGES

### 2025-12-21: Seed bridge module docs

- **What:** Added initial patterns, algorithm, validation, implementation, and health notes.
- **Why:** Establish Windows/WSL integration boundaries early.
- **Files:** `docs/civ6_living_narrator/win_wsl_bridge/`
- **Struggles/Insights:** Keep rotation state machine simple.

### 2025-12-21: Implement session rotation helpers

- **What:** Added bridge path resolver, launcher contracts, and session rotation helper plus tests.
- **Why:** Establish the runtime session id contract and reset tail state on rotation.
- **Files:** `src/win_wsl_bridge/bridge_path_resolver.py`, `src/win_wsl_bridge/launcher_contracts_and_ports.py`, `src/win_wsl_bridge/session_file_rotator.py`, `tests/test_windows_bridge_rotation_and_tail.py`
- **Struggles/Insights:** Session id is sourced from env to keep launcher in control.

---

## KNOWN ISSUES

### Launcher contract undefined

- **Severity:** medium
- **Symptom:** No clear start/stop behavior for Windows scripts.
- **Suspected cause:** Missing launcher spec.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Session rotation helper and tests are in place.

**What you need to understand:**
Bridge should prefer Windows runtime with WSL dev; tailing must tolerate partial lines and rotation.

**Watch out for:**
Do not hard-lock files; support session file naming conventions.

**Open questions I had:**
How to detect active session reliably?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Bridge now has session id and path resolution helpers with rotation tests.

**Decisions made:**
Windows-first runtime is the default; session rotation is required.

**Needs your input:**
Confirm launcher UX and log locations.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: implement active session detection and launcher wiring.

### Tests to Run

```bash
pytest tests/test_windows_bridge_rotation_and_tail.py
```

### Immediate

- [ ] Specify session_id detection and rotation rules.
- [ ] Define bridge folder structure and config keys.

### Later

- [ ] Add Windows launcher scripts with restart policy.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Rotation state machine and WSL path mapping.

**Intuitions:**
Launcher should own session_id creation to simplify tailing.

**What I wish I'd known at the start:**
Expected Civ6 Lua mod output paths.

---

## POINTERS

| What | Where |
|------|-------|
| Session rotator | `src/win_wsl_bridge/session_file_rotator.py` |
| Path resolver | `src/win_wsl_bridge/bridge_path_resolver.py` |
| Launcher contracts | `src/win_wsl_bridge/launcher_contracts_and_ports.py` |
