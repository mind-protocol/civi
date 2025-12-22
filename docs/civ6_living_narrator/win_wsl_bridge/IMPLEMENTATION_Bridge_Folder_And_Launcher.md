# win_wsl_bridge — Implementation: Bridge folder and launcher

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Session rotation | `src/win_wsl_bridge/session_file_rotator.py` |
| Path resolution | `src/win_wsl_bridge/bridge_path_resolver.py` |
| Launcher contracts | `src/win_wsl_bridge/launcher_contracts_and_ports.py` |
| Windows launcher | `runtime_windows/launcher/Start_LivingNarrator.ps1` |

---

## DATA FLOW

1. Launcher establishes session id and writes it to config or env.
2. Path resolver builds Windows and WSL paths for the session file.
3. Session rotator monitors session id changes and reopens files.
4. Tail reader consumes data through ingest.

---

## CONFIG

- `config/config.yaml`: bridge folder path, session id source.
- `runtime_windows/launcher/Start_LivingNarrator.ps1`: runtime orchestration.

---

## NOTES

Default to Windows runtime with WSL used only for dev and tests.
