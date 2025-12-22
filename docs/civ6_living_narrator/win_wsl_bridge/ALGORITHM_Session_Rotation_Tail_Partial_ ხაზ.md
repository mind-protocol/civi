# win_wsl_bridge — Algorithm: Session rotation and partial tail handling

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_WindowsFirst_Runtime.md
THIS:           ./ALGORITHM_Session_Rotation_Tail_Partial_ ხაზ.md
VALIDATION:     ./VALIDATION_FileAppend_Rotation_Restarts.md
IMPLEMENTATION: ./IMPLEMENTATION_Bridge_Folder_And_Launcher.md
HEALTH:         ./HEALTH_Restart_Survivability.md
SYNC:           ./SYNC_Bridge_Files_Ports_Launcher.md
```

---

## OVERVIEW

Track the active session id, follow its JSONL file, and tolerate partial lines. On session change, reopen the new file and reset tail offsets.

---

## STEPS

1. Determine active session id (from config or launcher contract).
2. Resolve Windows and WSL paths for the session JSONL file.
3. Tail the file from the last known offset.
4. If the last line is partial, buffer it and retry on next read.
5. On session id change, close current handle, reset buffer, and open the new file.

---

## EDGE CASES

- File rotation while reading: reopen and seek to zero.
- Session id missing: back off and retry with silence.
- Partial line across restart: discard buffer and resume at last safe offset.
