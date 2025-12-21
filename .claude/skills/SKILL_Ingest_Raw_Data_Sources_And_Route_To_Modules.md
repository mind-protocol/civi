# Skill: `ngram.ingest_raw_data_sources`
@ngram:id: SKILL.INGEST.RAW_DATA.ROUTE_TO_MODULES

## Maps to VIEW
`.ngram/views/VIEW_Ingest_Process_Raw_Data_Sources.md`

## Purpose
Parse and route raw inputs into areas/modules/tasks; produce deterministic mapping and seed TODOs.

## Inputs (YAML)
```yaml
data_sources:
  - "<path-or-url>"
scope_hints:
  areas: ["<optional>"]
  modules: ["<optional>"]
```

## Outputs (YAML)
```yaml
routing_table:
  - data_item: "<name>"
    target_area: "<area>"
    target_module: "<module>"
    doc_chain_targets: ["PATTERNS", "BEHAVIORS", "ALGORITHM", "VALIDATION", "IMPLEMENTATION", "HEALTH", "SYNC"]
    implementation_surfaces: ["<optional file:symbol>"]
seeded_todos:
  - module: "<area/module>"
    todo: "<@ngram:TODO text>"
```

## Gates (non-negotiable)
- No code/doc edits until a routing table exists.
- If routing is ambiguous, log `@ngram:escalation` and route everything else first.

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
When two or more sources disagree (documents, code, or routing guidance), treat this skill as the executor of the documented decision:

1. Capture the contradiction inside the module's `CONFLICTS` section with `@ngram:escalation` so reviewers can spot the blocker during ingest routing reviews.
2. Once the investigation yields a decision, update every conflicting source so they agree, replace the `ESCALATION` entry with the `DECISION` template below, and add a `Resolved:` note summarizing what changed.
3. Update the relevant SYNC (module or project) with the same reasoning, list of touched files, and any remaining `@ngram:TODO`s or known risks; remove the `CONFLICTS` section if nothing is still outstanding.

## CONFLICTS

### DECISION: document ingestion escalation handling
- Conflict: This skill referenced logging `@ngram:escalation` for ambiguous routing choices but never recorded the resulting decision, leaving the escalation marker unresolved.
- Resolution: Added this conflict-resolution guidance and documented the action here so the escalation now points to a tangible decision and recorded the change in the project SYNC.
- Reasoning: Explicitly closing the escalation keeps the pipeline from flagging the same blocker repeatedly and tells future agents where to find the resolved instructions.
- Updated: `.claude/skills/SKILL_Ingest_Raw_Data_Sources_And_Route_To_Modules.md`, `.ngram/state/SYNC_Project_State.md`
Resolved: Ingest routing now has a documented conflict workflow, and the project SYNC records that this escalation marker has been satisfied.
