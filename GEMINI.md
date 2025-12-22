# CLAUDE.md

## Project: Civ6 Living Narrator

### Commands
- **Run Pipeline**: `./run.sh` (Runs the full loop)
- **Run One Step**: `./step.sh` (Processes current events and exits)
- **Run Tests**: `pytest`
- **Lint/Check**: `ngram doctor`
- **Docs**: `ngram context <file>`

### Coding Style
- **Python**: 
  - Use `snake_case` for files and functions.
  - Use `CamelCase` for classes.
  - Type hinting is mandatory (`from typing import ...`).
  - Use `logger` instead of `print`.
  - Prefer descriptive variable names.
- **Documentation**:
  - Follow the `ngram` protocol: `OBJECTIFS` -> `BEHAVIORS` -> `PATTERNS` -> ...
  - Update `SYNC_Project_State.md` after significant changes.

### Agent Structure
- **Agents**: Located in `agents/<name>/`.
- **Identity**: `agents/<name>/CLAUDE.md` defines the system prompt and tools.
- **CLI Interaction**: Used via `src/llm_router/simple_llm_client.py`.

# ngram

@.ngram/PRINCIPLES.md

---

@.ngram/PROTOCOL.md

---

## Before Any Task

Check project state:
```
.ngram/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

## Choose Your VIEW

Based on your task, load ONE view from `.ngram/views/`:

| Task | VIEW |
|------|------|
| Processing raw data (chats, PDFs) | VIEW_Ingest_Process_Raw_Data_Sources.md |
| Getting oriented | VIEW_Onboard_Understand_Existing_Codebase.md |
| Analyzing structure | VIEW_Analyze_Structural_Analysis.md |
| Defining architecture | VIEW_Specify_Design_Vision_And_Architecture.md |
| Writing/modifying code | VIEW_Implement_Write_Or_Modify_Code.md |
| Adding features | VIEW_Extend_Add_Features_To_Existing.md |
| Pair programming | VIEW_Collaborate_Pair_Program_With_Human.md |
| Health checks | VIEW_Health_Define_Health_Checks_And_Verify.md |
| Debugging | VIEW_Debug_Investigate_And_Fix_Issues.md |
| Reviewing changes | VIEW_Review_Evaluate_Changes.md |
| Refactoring | VIEW_Refactor_Improve_Code_Structure.md |

## After Any Change

Update `.ngram/state/SYNC_Project_State.md` with what you did.
If you changed a module, update its `docs/{area}/{module}/SYNC_*.md` too.

