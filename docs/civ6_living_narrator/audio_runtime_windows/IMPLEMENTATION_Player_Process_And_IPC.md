# audio_runtime_windows — Implementation: Player process and IPC

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Audio player | `runtime_windows/audio_player/audio_queue_player.py` |
| Player config | `runtime_windows/audio_player/config_player.yaml` |
| Launcher | `runtime_windows/launcher/Start_LivingNarrator.ps1` |

---

## DATA FLOW

1. Player process listens for IPC commands.
2. Queue receives play/stop/replay commands.
3. Status updates sent back to telemetry.

---

## CONFIG

- `runtime_windows/audio_player/config_player.yaml`: device, volume, queue settings.

---

## NOTES

Use a lightweight IPC mechanism (stdin, local socket, or file-based queue).
