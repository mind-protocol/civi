# OCR — Validation: Change Detection and Priority

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```

---

## INVARIANTS

### I1: Hash Stability

**Statement:** Identical text produces identical hash.

```python
def test_hash_stability():
    text = "Your spymaster has uncovered a plot"
    h1 = md5(text.encode()).hexdigest()[:12]
    h2 = md5(text.encode()).hexdigest()[:12]
    assert h1 == h2
```

**Why it matters:** If hashes vary for same text, we get false positives (diff when nothing changed).

### I2: Change Threshold

**Statement:** Diffs only emitted when change exceeds MIN_CHANGE_THRESHOLD (50 chars) or region priority >= 7.

```python
def test_threshold():
    old = "Gold: 500"
    new = "Gold: 501"
    diff_size = abs(len(new) - len(old))
    assert diff_size < MIN_CHANGE_THRESHOLD

    # This should NOT trigger a diff unless priority >= 7
```

**Why it matters:** Prevents spam from minor UI updates (counters ticking).

### I3: Priority Ordering

**Statement:** Diffs are sorted by priority descending.

```python
def test_priority_order():
    diffs = [
        TextDiff(region="top_bar", priority=3, ...),
        TextDiff(region="event_popup", priority=10, ...),
        TextDiff(region="notifications", priority=7, ...)
    ]
    sorted_diffs = sorted(diffs, key=lambda d: -d.priority)
    assert sorted_diffs[0].region == "event_popup"
    assert sorted_diffs[1].region == "notifications"
```

**Why it matters:** Claude sees important changes first.

### I4: Region Bounds

**Statement:** All regions have valid bounds (0 <= x,y < 1, x+w <= 1, y+h <= 1).

```python
def test_region_bounds():
    for region in CK3_REGIONS:
        assert 0 <= region.x < 1
        assert 0 <= region.y < 1
        assert region.x + region.w <= 1
        assert region.y + region.h <= 1
```

**Why it matters:** Invalid bounds cause crop errors.

### I5: Append-Only Diffs

**Statement:** Diffs file is append-only. Existing entries never modified.

**Why it matters:** Daemon reads from cursor position. Modifying past entries breaks consumption.

---

## ERROR CONDITIONS

| Error | Detection | Recovery |
|-------|-----------|----------|
| Tesseract not installed | `pytesseract.get_tesseract_version()` fails | Exit with install instructions |
| Screenshot missing | `get_latest_screenshot()` returns None | Skip cycle |
| Image corrupted | PIL raises exception | Log, skip cycle |
| OCR timeout | Tesseract hangs | 10s timeout per region |
| Disk full | Write fails | Log error, continue (diffs lost) |

---

## VERIFICATION PROCEDURE

### Manual Test: OCR Accuracy

```bash
# Capture a screenshot with known text
# Run OCR once
python3 scripts/ocr_watcher.py --game ck3 --once

# Check output
cat narrator/state/ocr_state.json | jq '.last_results.event_popup.text'

# Verify extracted text matches visible text
```

### Manual Test: Change Detection

```bash
# Clear state
rm narrator/state/ocr_state.json narrator/state/ocr_diffs.jsonl

# Run OCR twice with different game state
python3 scripts/ocr_watcher.py --game ck3 --once
# Change something in game
python3 scripts/ocr_watcher.py --game ck3 --once

# Check diffs
cat narrator/state/ocr_diffs.jsonl
```

### Automated Test: Priority Ordering

```python
# tests/test_ocr_priority.py
def test_diffs_sorted_by_priority():
    diffs = detect_changes(current, previous, regions)
    priorities = [d.priority for d in diffs]
    assert priorities == sorted(priorities, reverse=True)
```

---

## BUDGET CONSTRAINTS

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Cycle time | <2s | Must complete before next cycle (5s) |
| Memory | <100MB | Avoid OOM on low-RAM systems |
| Diff file size | <10MB | Rotate or truncate if exceeded |
| OCR per region | <1s | Timeout and skip slow regions |
