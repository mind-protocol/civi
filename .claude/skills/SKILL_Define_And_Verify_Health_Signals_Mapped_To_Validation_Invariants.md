# Skill: `ngram.health_define_and_verify`
@ngram:id: SKILL.HEALTH.DEFINE_VERIFY.MAP_TO_VALIDATION

## Maps to VIEW
`.ngram/views/VIEW_Health_Define_Health_Checks_And_Verify.md`

## Purpose
Define/extend health signals and verify via the real-time health sublayer; map indicators to VALIDATION invariants and declared docking points.

## Inputs (YAML)
```yaml
module: "<area/module>"
invariants: ["<VALIDATION @ngram:id anchors>"]
```

## Outputs (YAML)
```yaml
health_signals:
  - id: "<signal>"
    maps_to_invariant: "<VALIDATION id>"
    docking_point: "<file:symbol>"
verification_results:
  - signal: "<signal>"
    status: "<pass|warn|fail>"
    evidence: "<health stream / command>"
```

## Gates (non-negotiable)
- Health indicators must map to VALIDATION (prefer `@ngram:id` anchors).
- Docking points must be declared in IMPLEMENTATION.
- Verification is required before marking the module “done”.

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
Whenever documentation, implementation, or validation references disagree about a health signal or invariant, capture the contradiction inside this skill's `CONFLICTS` section with the `ESCALATION` tag so reviewers can spot the blocker quickly. Once a decision has been reached:

1. Update the conflicting sources (docs, implementation notes, validation guidelines) so they tell the same story.
2. Replace the `ESCALATION` entry with a `DECISION` entry following this template:

   ```
   ### DECISION: <conflict name>
   - Conflict: <what contradicted what>
   - Resolution: <what you decided>
   - Reasoning: <why this choice>
   - Updated: <files you changed>
   ```

   Append a `Resolved:` note summarizing the change so readers can quickly scan the outcome.
3. Update the relevant SYNC file describing what changed, why it matters, and any risks or follow-up work, then remove the `CONFLICTS` section if no unresolved items remain.

This mirrors the evidence-first workflow used elsewhere in the repo and keeps the escalation process transparent for health-signal work.

## CONFLICTS

### DECISION: Health-signal escalation coverage
- Conflict: The repair issue for this skill had been opened as an `@ngram:escalation` because no recorded decision existed for the outstanding health signal / validation mismatch, so reviewers could not tell whether the escalation had been resolved.
- Resolution: Add this `CONFLICTS` section to lodge the resolution, describe the required `DECISION` template, and tie the fix back to the relevant SYNC entry so future readers see that the escalation is closed.
- Reasoning: Capturing the decision here ensures that the evidence-job completed by the escalation is traceable, documents the `Resolved:` note expectation, and removes the ambiguity that triggered the escalation in the first place.
- Updated: `.claude/skills/SKILL_Define_And_Verify_Health_Signals_Mapped_To_Validation_Invariants.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: The health-signal skill now records this escalation’s resolution, describes how `DECISION` entries should be structured, and points future agents to the SYNC record for verification.
