# Skill: `ngram.review_evaluate_changes`
@ngram:id: SKILL.REVIEW.EVALUATE.PRODUCE_AUDITABLE_REPORT

## Maps to VIEW
`.ngram/views/VIEW_Review_Evaluate_Changes.md`

## Purpose
Produce a review-ready report with stable references and explicit remaining gaps.

## Inputs (YAML)
```yaml
module: "<area/module>"
changes: ["<files changed>"]
```

## Outputs (YAML)
```yaml
report:
  evidence:
    docs: ["<@ngram:id + file + header path>"]
    code: ["<file + symbol>"]
  summary: ["<what changed>"]
  verification: ["<what was verified>"]
  remaining_gaps: ["<open TODOs/escalations>"]
```

## Gates (non-negotiable)
- Must include stable references for non-trivial claims.
- Must list remaining TODOs and escalations/propositions explicitly.

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
Every `@ngram:escalation` the review skill surfaces should be captured inside this document before modifying any conflicting code or docs. Use this `CONFLICTS` section to log the contradiction and follow the checklist below:

1. Describe the conflict in this section so reviewers understand what evidence disagreed or which story diverged.
2. Once a human decision is provided, update the code/docs so all sources match, swap the `ESCALATION` entry for the `DECISION` template below, and add a `Resolved:` note summarizing what was changed plus any verification commands run.
3. Record the same reasoning and touched files in `.ngram/state/SYNC_Project_State.md` (or the relevant module SYNC) and keep this `CONFLICTS` section until every entry is a `DECISION`.

This keeps the review workflow aligned with the evidence-first protocol and leaves a traceable history for each escalation.

## CONFLICTS

### DECISION: teach the review skill how to close escalations
- Conflict: The open escalation pointed out that this skill lacked in-document guidance for transforming `ESCALATION` markers into `DECISION` entries, so reviewers could not see where to document the outcome.
- Resolution: Added the conflict-resolution checklist above, documented the DECISION template, and recorded the change in the project SYNC so future agents see exactly how to close this type of escalation.
- Reasoning: The protocol requires every `@ngram:escalation` to become a documented `DECISION` before a task is handed off; this section now shows where to do that for the review skill.
- Updated: `.ngram/skills/SKILL_Review_Evaluate_Changes_And_Produce_Auditable_Report.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: Logged the new checklist plus this `DECISION` entry, reran `ngram validate` (fails: `.ngram/views/VIEW_Collaborate_Pair_Program_With_Human.md` still missing).
