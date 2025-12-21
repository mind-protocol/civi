# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
```

---

## CURRENT STATE
The project is emphasizing the evidence-first debugging stance: conflicts in docs/code must be captured, resolved, and reflected in both the affected files and the guiding SYNC state. The recent work landed guidance inside `.claude/skills/SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md` so the skill can turn `ESCALATION` markers into documented `DECISION`s.

---

## ACTIVE WORK

### Conflict resolution docs
- **Area:** `.claude/skills/`
- **Status:** DESIGNING
- **Owner:** codex
- **Context:** Added explicit conflict-resolution flow for the debugging skill so that all escalations convert into decisions with evidence, a resolved note, and the matching SYNC update.

---

## RECENT CHANGES

### 2025-12-21: Document conflict resolution for debugging skill
- **What:** Added a dedicated “Conflict resolution” section to `SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md` explaining how to turn `@ngram:escalation` blockers into `DECISION` entries once code/docs align.
- **Why:** The Escalation issue highlighted that the skill lacked explicit guidance for closing the loop; the new text ensures future agents follow the prescribed format and leave a `Resolved:` note.
- **Impact:** Better traceability for disagreements that arise during investigations and fewer stalled escalations.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| *(none)* | - | - | - |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Debug_Investigate_And_Fix_Issues.md`

**Current focus:** Keep enforcing the conflict-resolution workflow for documentation and code, then propagate the pattern to other `SKILL_*.md` files as needed.

**Key context:**
- Every resolved conflict must land as a `DECISION` entry with `Resolved:` annotation.
- Update the relevant SYNC file and the skill doc even when the change is a small clarification.

**Watch out for:**
- Don’t leave any `ESCALATION` entries in `CONFLICTS` sections once the underlying contradiction has been addressed.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Documented the conflict-resolution workflow inside the debugging skill so that future agents know how to convert `ESCALATION` markers into `DECISION` entries and update SYNC accordingly.

**Decisions made recently:**
- Treat every conflict as evidence-first: capture the contradiction, decide, document the decision, and add a `Resolved:` note.

**Needs your input:** None for now; the new guidance is self-contained.

**Concerns:** Be mindful that this skill doc is the only place recording the format—if further conflict templates are needed, extend the doc chain.

---

## TODO

### High Priority
- [ ] None

### Backlog
- [ ] Extend conflict diagnostics to other skill docs once this pattern proves stable.
- IDEA: Record a `CONFLICTS` section template that many docs could reuse.

---

## CONSCIOUSNESS TRACE

**Project momentum:** Incremental—this sprint is about solidifying the workflow rather than shipping new features.

**Architectural concerns:** The current repo lacks a consistent place for `CONFLICTS` sections; keep an eye on drift if more modules need SYNC files.

**Opportunities noticed:** The conflict-resolution instructions could flow into a standalone template for future skill authors.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `.claude/skills/` | DESIGNING | (none yet; conflicts tracked inside the skill files themselves) |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| `debug_investigation_skill` | `.claude/skills/SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md` | `.claude/skills/SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md` | DESIGNING |

**Unmapped code:** None.

**Coverage notes:** The skill doc serves as both the implementation guidance and the documentation entry for this capability.
