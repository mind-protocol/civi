# moment_graph — Algorithm: Create, merge, promote, decay, myth

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
THIS:           ./ALGORITHM_Create_Merge_Promote_Decay_Myth.md
VALIDATION:     ./VALIDATION_Lifecycle_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Moment_Store_And_Indexing.md
HEALTH:         ./HEALTH_Moment_Count_Charge_Distribution.md
SYNC:           ./SYNC_Moment_Lifecycle.md
```

---

## OVERVIEW

Maintain a sparse graph of moments, promote a few to myth, decay the rest, and select callbacks with explicit references.

---

## STEPS

1. For each normalized event, score importance and tags.
2. If importance >= create_threshold, create a moment.
3. Merge with nearby moments if tag overlap and turn distance < merge_window.
4. Promote to myth if charge >= promote_threshold.
5. Decay charge each turn; drop moments below decay_floor.
6. Select callbacks when tag overlap or time gate passes; emit moment_refs.

---

## OUTPUTS

- Moment records with tags, charge, and myth flag.
- Callback candidates with moment_refs.
