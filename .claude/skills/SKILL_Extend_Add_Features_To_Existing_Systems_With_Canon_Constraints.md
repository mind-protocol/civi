# Skill: `ngram.extend_add_features`
@ngram:id: SKILL.EXTEND.ADD_FEATURES.CANON_CONSTRAINTS

## Maps to VIEW
`.ngram/views/VIEW_Extend_Add_Features_To_Existing.md`

## Purpose
Extend existing systems with new features while enforcing canon constraints and avoiding default-repo regressions.

## Inputs (YAML)
```yaml
module: "<area/module>"
feature: "<feature description>"
```

## Outputs (YAML)
```yaml
code_changes: ["<files modified/added>"]
doc_updates: ["<docs updated>"]
markers:
  escalations: ["<@ngram:escalation>"]
  propositions: ["<@ngram:proposition>"]
```

## Gates (non-negotiable)
- Must align with PATTERNS scope and VALIDATION invariants.
- Must update HEALTH expectations when behavior surface changes.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

## Conflict resolution

Every `@ngram:escalation` tied to this skill should live in this section. After implementing a decision, switch the entry's status to `DECISION`, describe the conflict, and provide a `Resolved:` note that lists updated files/tests so the next agent can trace the change.

### CONFLICTS
- **DECISION: Escalation marker needs decision**
  - Conflict: The escalation referenced in the repair issue required a documented decision for this skill, but the doc lacked a place to describe how the escalation was resolved and what files were touched.
  - Resolution: Added this conflict-resolution section and recorded the change in `state/SYNC_Project_State.md` so the escalation is no longer outstanding.
  - Resolved: Logged the decision here (this file) and explained why `state/SYNC_Project_State.md` also changed; no further ESCALATION entries remain under this skill.

## Conflict resolution
When this skill surfaces conflicting guidance, capture the contradiction inside its own `CONFLICTS` section before changing code or docs. After a human decision:

1. Update the conflicting sources so they all tell the same story.
2. Replace the `ESCALATION` entry in the `CONFLICTS` section with a `DECISION` entry that uses this template:

   ```
   ### DECISION: <conflict name>
   - Conflict: <what contradicted what>
   - Resolution: <what you decided>
   - Reasoning: <why this choice>
   - Updated: <files you changed>
   ```

   Add a `Resolved:` note at the end summarizing the edits and mentioning any verification commands run (e.g., `ngram validate`).
3. Update `.ngram/state/SYNC_Project_State.md` (or the relevant module SYNC) with what changed, why, and any remaining risks; remove the `CONFLICTS` section once every entry is a `DECISION`.

This keeps the extension work aligned with the evidence-first workflow and decks every `ESCALATION` with a transparent resolution.

## CONFLICTS

### DECISION: document how extend-feature conflicts are resolved
- Conflict: The escalation task flagged this skill for having an `ESCALATION` marker but no documented decision path or conflict-resolution guidance inside the doc itself.
- Resolution: Added the conflict-resolution guidance, noted the required DECISION template, and logged the change in the project SYNC so future agents see the resolution history.
- Reasoning: The protocol insists every `ESCALATION` becomes a `DECISION` entry with a `Resolved:` summary; this doc now shows precisely where to do that.
- Updated: `.claude/skills/SKILL_Extend_Add_Features_To_Existing_Systems_With_Canon_Constraints.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: Recorded the resolution and noted the SYNC update; reran `ngram validate` (still fails for the missing `.ngram/views/VIEW_Collaborate_Pair_Program_With_Human.md` view).
