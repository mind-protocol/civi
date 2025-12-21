# Skill: `ngram.implement_write_or_modify_code`
@ngram:id: SKILL.IMPLEMENT.WRITE_OR_MODIFY.DOC_CHAIN_COUPLING

## Maps to VIEW
`.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

## Purpose
Perform code edits while coupling implementation changes to doc chain updates and preserving canon naming/commenting and monitoring expectations.

## Inputs (YAML)
```yaml
module: "<area/module>"
task: "<what to change>"
```

## Outputs (YAML)
```yaml
code_changes: ["<files modified>"]
doc_updates: ["<docs updated>"]
markers:
  escalations: ["<@ngram:escalation>"]
  propositions: ["<@ngram:proposition>"]
```

## Gates (non-negotiable)
- Update doc chain for every meaningful code change.
- No new terms/names without canon support (PATTERNS/CONCEPT).
- Verify via health/runtime where applicable; do not claim done without evidence.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Conflict resolution
- Record blockers in the relevant `CONFLICTS` section of the affected SYNC before invoking this skill.
- Once a human decision exists, convert the `ESCALATION` entry into a `DECISION` entry, cite the doc/code now aligned, and add a `Resolved:` note describing the change.
- Keep `CONFLICTS` sections only while there are outstanding `ESCALATION` entries; drop the section or archive it once every item is a `DECISION`.

## Conflict resolution (detailed steps)
1. **Read first:** open the module SYNC plus any nearby PATTERNS/OBJECTIFS so you understand the conflict, the timeline, and the next handoff.
2. **Apply each decision:** update the docs/code according to the decision, convert the `ESCALATION` entry to a `DECISION`, record what was updated, and add a `Resolved:` summary that explains what changed.
3. **Verify evidence:** rerun `ngram validate` (and any relevant health checks) so the chain reflects the resolved state, then log those results in the SYNC.
4. **Clean up:** remove the `CONFLICTS` section or leave it only with `DECISION` entries; if the resolution is incomplete, add a `## GAPS` section to the SYNC describing what remains and why.

### DECISION entry template
Use this structure so future agents see what changed:
```
### DECISION: {short description}
- Conflict: {what contradicted what}
- Resolution: {what was changed to align the sources}
- Reasoning: {why the change is correct}
- Updated: `{path/to/file}`
- Resolved: {summary of what was reworked}
```

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.
