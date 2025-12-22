# win_wsl_bridge — Validation: File append, rotation, restarts

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
THIS:           ./VALIDATION_FileAppend_Rotation_Restarts.md
IMPLEMENTATION: ./IMPLEMENTATION_Bridge_Folder_And_Launcher.md
HEALTH:         ./HEALTH_Restart_Survivability.md
SYNC:           ./SYNC_Bridge_Files_Ports_Launcher.md
```

---

## INVARIANTS

### V1: Append-only tailing

```
Tail reader never truncates or rewrites the source file
```

**Checked by:** `test_windows_bridge_rotation_and_tail.py`

### V2: Session rotation resets offsets

```
When session_id changes, tail offset resets and new file is opened
```

**Checked by:** `test_windows_bridge_rotation_and_tail.py`

### V3: Partial lines are retried

```
Incomplete JSON lines are buffered and retried, not emitted
```

**Checked by:** `test_windows_bridge_rotation_and_tail.py`

---

## ERROR CONDITIONS

### E1: Missing bridge folder

```
WHEN:    bridge path not found
THEN:    backend logs and retries; no crash
SYMPTOM: ingest_lag_ms grows, no events emitted
```

**Verified by:** NOT YET VERIFIED

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_windows_bridge_rotation_and_tail.py
```
