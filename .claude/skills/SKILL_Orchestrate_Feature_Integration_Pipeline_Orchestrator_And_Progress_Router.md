# Skill: `ngram.orchestrate_feature_integration`
@ngram:id: SKILL.ORCH.FEATURE_INTEGRATION.PIPELINE.ORCHESTRATOR

## Maps to VIEW
`(wrapper skill; calls the sequence below)`

## Purpose
Run the full pipeline: ingest → per-module loop → close-out, enforcing never-stop work conservation and deterministic routing.

## Inputs (YAML)
```yaml
objective: "<goal + acceptance criteria>"
data_sources:
  - "<path-or-url>"
scope_hints:
  areas: ["<optional>"]
  modules: ["<optional>"]
constraints:
  do_not_touch: ["<paths/surfaces>"]
  patterns: ["<canon patterns to respect>"]
```

## Outputs (YAML)
```yaml
task_graph:
  - module: "<area/module>"
    todos: ["<todo-id>"]
    chosen_view: "<implement|extend|debug>"
    verification_plan: ["<health-check>"]
progress_log:
  - module: "<area/module>"
    status: "<scaffolded|documented|implemented|verified>"
```

## Gates (non-negotiable)
- Must load PROTOCOL and required VIEWS referenced by downstream skills.
- Must create at least one `@ngram:TODO` per module/task discovered.
- Must enforce pipeline order and never-stop work conservation.

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
Any `@ngram:escalation` tied to this orchestrator should be captured here before steering downstream work. Once a human decision exists:

1. Update every conflicting source (docs, code, SYNC) so they agree.
2. Replace the `ESCALATION` entry in this section with a `DECISION` entry using the template below, naming the contradiction and summarizing the resolution.
3. Add a `Resolved:` note that highlights what changed, which files were touched, and any verification commands run.

   ```
   ### DECISION: <conflict name>
   - Conflict: <what contradicted what>
   - Resolution: <what you decided>
   - Reasoning: <why this choice>
   - Updated: <files you changed>
   ```

4. Update `.ngram/state/SYNC_Project_State.md` (or an area/module SYNC if one exists) with the same reasoning, touched files, and remaining blockers.
5. Remove the `CONFLICTS` section once every entry is a `DECISION`.

This keeps the pipeline orchestrator aligned with the evidence-first workflow and prevents `@ngram:escalation` markers from lingering without documented outcomes.

## CONFLICTS

### DECISION: document how orchestrator escalations are closed
- Conflict: The escalation task flagged this skill for having an `@ngram:escalation` marker but no documented decision path or conflict-resolution guidance in the skill doc itself.
- Resolution: Added this conflict-resolution section, noted the expected template, and logged the change in the project SYNC so future agents can see how the escalation was addressed.
- Reasoning: The protocol dictates every `ESCALATION` becomes a `DECISION` entry with a `Resolved:` summary; this doc now shows exactly where to do that.
- Updated: `.claude/skills/SKILL_Orchestrate_Feature_Integration_Pipeline_Orchestrator_And_Progress_Router.md`, `.ngram/state/SYNC_Project_State.md`
- Resolved: Recorded the update, reran `ngram validate` (still fails because `.ngram/views/VIEW_Collaborate_Pair_Program_With_Human.md` is missing), captured that failure for the health log, and ensured the new guidance closes the loop.
