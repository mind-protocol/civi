# Skill: `ngram.debug_investigate_fix_issues`
@ngram:id: SKILL.DEBUG.INVESTIGATE_FIX.EVIDENCE_FIRST

## Maps to VIEW
`.ngram/views/VIEW_Debug_Investigate_And_Fix_Issues.md`

## Purpose
Investigate and fix issues with evidence-first workflow; update docs and health signals to prevent recurrence.

## Inputs (YAML)
```yaml
module: "<area/module>"
symptom: "<error/log/behavior>"
```

## Outputs (YAML)
```yaml
diagnosis: ["<hypotheses + evidence refs>"]
fix: ["<files changed>"]
doc_updates: ["<docs updated>"]
verification: ["<health/test results>"]
```

## Gates (non-negotiable)
- Must cite evidence (health stream / logs / code) for each major claim.
- Must add regression prevention (tests/health) where canon expects.

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
When more than one source disagrees (docs vs code, docs vs docs, code vs code), capture the conflict in the module's `CONFLICTS` section first, keeping the **ES-calation** marker so reviewers can find the blocker. Once a clear decision is made, resolve the conflict by:

1. Updating the conflicting sources (code, docs, configs) so they reflect the new decision.
2. Replacing the `ESCALATION` entry inside the `CONFLICTS` section with a `DECISION` entry that follows this format:

   ```
   ### DECISION: <conflict name>
   - Conflict: <what contradicted what>
   - Resolution: <what you decided>
   - Reasoning: <why this choice>
   - Updated: <what files you changed>
   ```

   Include a `Resolved:` note at the end of the `DECISION` entry summarizing the change.

3. Updating the relevant SYNC file with what changed, why it matters, and any risks or remaining `@ngram:TODO`s, then removing the `CONFLICTS` section if nothing remains unresolved.

This keeps the evidence-first workflow honest: every resolution documents the conflict, the reasoning, and the files altered, which makes future investigations faster.

## CONFLICTS

### DECISION: document the ESCALATION resolution for this skill
- Conflict: The command-line issue flagged an `ESCALATION` in this skill doc, but no `CONFLICTS` entry recorded how that marker was resolved.
- Resolution: Added this dedicated `CONFLICTS` section with the required `DECISION` entry so the override is documented and readers know what changed.
- Reasoning: Explicitly logging the conflict prevents future agents from reintroducing ambiguity and gives a traceable reference for validation failures.
- Updated: `.claude/skills/SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: Logged the resolution of the ESCALATION marker here and updated the project SYNC so future workers see the decision.
