# Skill: `ngram.onboard_understand_module_codebase`
@ngram:id: SKILL.ONBOARD.UNDERSTAND_EXISTING_CODEBASE.CONFIRM_CANON

## Maps to VIEW
`.ngram/views/VIEW_Onboard_Understand_Existing_Codebase.md`

## Purpose
Identify canonical paths/symbols/dataflow and confirm naming/comment/monitoring expectations for the module.

## Inputs (YAML)
```yaml
module: "<area/module>"
code_roots: ["<paths>"]
```

## Outputs (YAML)
```yaml
canonical_surfaces:
  - file: "<path>"
    symbols: ["<function/class>"]
dataflow_notes: ["<key flows>"]
naming_terms: ["<canon terms>"]
```

## Gates (non-negotiable)
- If canonical surface is unclear, log `@ngram:escalation` and proceed with other modules/tasks.
- Must update IMPLEMENTATION_* with discovered surfaces/docking points.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

## CONFLICTS

### DECISION: Give this skill a conflict-resolution trace
- Conflict: The skill references `@ngram:escalation` as a blocker marker but had no `CONFLICTS` section documenting how a decision should be recorded, so the escalation history could disappear.
- Resolution: Added this `CONFLICTS` section with the required `DECISION` entry to capture how decisions about `@ngram:escalation` markers should be applied and recorded going forward.
- Reasoning: Aligning the onboarding skill with the repository-wide workflow prevents escalations from being forgotten and gives future agents a clear template for what files to update and what the resolution looked like.
- Updated: `.claude/skills/SKILL_Onboard_Understand_Existing_Module_Codebase_And_Confirm_Canon.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: Logged the conflict-resolution expectations for this skill so every `@ngram:escalation` marker now ends up with a documented `DECISION` summary and a note about what changed.

## Conflict resolution
When you discover a disagreement between docs, code, or monitoring artifacts while onboarding a module, record it inside this skill's `CONFLICTS` section using the `@ngram:escalation` marker so reviewers see the blocker quickly. Once a human decision arrives, follow these steps:

1. **Understand the conflict** — read the module's SYNC (and any relevant PATTERNS/OBJECTIFS) to capture the context, constraints, and what the decision needs to satisfy.
2. **Apply the decision**
   - Update the conflicting sources (docs, IMPLEMENTATION notes, validation, etc.) so they agree with the chosen path.
   - Replace the `ESCALATION` entry with a `DECISION` entry in the `CONFLICTS` section, including a `Resolved:` summary that points to the files that changed.
   - Use the template below so future agents immediately understand what happened.
3. **Verify and document** — rerun `ngram validate` (and any relevant health checks) so the chain reflects the resolved state, then note the validation outcome inside the module's SYNC entry.
4. **Clean up** — if every `CONFLICTS` entry is now a `DECISION`, you may remove the section, but keep the resolved notes in SYNC so the history remains traceable.

### DECISION entry template
```
### DECISION: {short description}
- Conflict: {what contradicted what}
- Resolution: {what was changed to align the sources}
- Reasoning: {why this change is correct}
- Updated: `{path/to/file}`
- Resolved: {summary of the edit}
```

If you are unable to complete the resolution, add a `## GAPS` section to the module SYNC describing what was done, what remains, and why you stopped (missing info or pending human decisions). Do not claim completion without a commit.
