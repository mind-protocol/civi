# win_wsl_bridge — Patterns: Windows-first runtime bridge

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_WindowsFirst_Runtime.md
ALGORITHM:      ./ALGORITHM_Session_Rotation_Tail_Partial_ ხაზ.md
VALIDATION:     ./VALIDATION_FileAppend_Rotation_Restarts.md
IMPLEMENTATION: ./IMPLEMENTATION_Bridge_Folder_And_Launcher.md
HEALTH:         ./HEALTH_Restart_Survivability.md
SYNC:           ./SYNC_Bridge_Files_Ports_Launcher.md
```

---

## THE PROBLEM

Civ 6 runs on Windows, while development often happens in WSL. The bridge must keep runtime reliable without cross-platform file lock issues.

---

## THE PATTERN

- Windows is the source of truth for runtime.
- WSL reads Windows files through /mnt/c when needed.
- Session rotation avoids long JSONL tail offsets.
- Partial lines are buffered until complete.

---

## PRINCIPLES

### Principle 1: Windows-first runtime

All runtime components should run on Windows by default to reduce friction.

### Principle 2: Append-only and tolerant tailing

Never lock the events file; tolerate partial lines and retry.

### Principle 3: Explicit session boundaries

Session id drives file rotation and resets tail offsets.

---

## SCOPE

### In Scope

- Path resolution between Windows and WSL.
- Session file rotation and tail restart rules.
- Launcher contracts for start/stop.

### Out of Scope

- Full IPC layer between WSL and Windows.
- Audio playback logic.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define session id source (launcher vs Lua mod).
- [ ] Decide rotation naming pattern.
