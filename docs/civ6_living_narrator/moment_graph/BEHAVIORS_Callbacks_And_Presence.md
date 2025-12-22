# moment_graph — Behaviors: Callbacks and presence

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Memory_And_Mythification.md
BEHAVIORS:      ./BEHAVIORS_Callbacks_And_Presence.md
ALGORITHM:      ./ALGORITHM_Create_Merge_Promote_Decay_Myth.md
VALIDATION:     ./VALIDATION_Lifecycle_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Moment_Store_And_Indexing.md
HEALTH:         ./HEALTH_Moment_Count_Charge_Distribution.md
SYNC:           ./SYNC_Moment_Lifecycle.md
```

---

## BEHAVIORS

### B1: Create moments from key events

Only high-importance events create new moments.

### B2: Merge similar moments

Moments with overlapping tags and close turns merge into one.

### B3: Promote to myth

Moments become mythic when they clear a promotion threshold.

### B4: Callback with references

Callbacks include moment_refs and only trigger with tag overlap or time gate.

---

## ANTI-BEHAVIORS

- A1: Endless memory list with no pruning.
- A2: Callbacks with no explicit references.
