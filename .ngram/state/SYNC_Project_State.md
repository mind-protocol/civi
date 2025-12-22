# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: gemini
```

---

## CURRENT STATE

The project now supports multi-model LLM backends (Claude and Gemini) configurable via environment variables. The `llm_router` has been refactored to abstract the CLI client.

---

## ACTIVE WORK

### LLM Integration

- **Area:** `llm_router/`
- **Status:** in progress
- **Owner:** gemini
- **Context:** enabling Gemini support alongside Claude.

---

## RECENT CHANGES

### 2025-12-22: Gemini CLI Integration

- **What:** Refactored `simple_llm_client.py` to `LLMCLIClient`, added `.env` support, and implemented Gemini CLI call pattern (`-p`, `-y`, `--continue`).
- **Why:** To support `gemini-3-pro-preview` as requested.
- **Impact:** `SELECTED_MODEL` in `.env` now drives the backend choice.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| None | - | - | - |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `views/VIEW_Implement_Write_Or_Modify_Code.md`

**Current focus:** ensuring the narrator works with the selected model.

**Key context:**
The `LLMCLIClient` now handles dispatch.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
You can now use Gemini by setting `SELECTED_MODEL=gemini...` in `.env`. The system uses the `gemini` CLI tool with `-y` and `--continue` flags.

**Decisions made:**
Renamed `ClaudeCLIClient` to `LLMCLIClient` to be generic.

**Needs your input:**
Ensure `gemini` CLI tool is installed and authenticated in your environment.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `docs/civ6_living_narrator/llm_router` | DESIGNING | `docs/civ6_living_narrator/llm_router/SYNC_JSON_Contracts_And_Fallbacks.md` |

---