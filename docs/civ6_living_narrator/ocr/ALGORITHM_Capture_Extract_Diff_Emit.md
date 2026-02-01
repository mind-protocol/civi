# OCR — Algorithm: Capture, Extract, Diff, Emit

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```

---

## OVERVIEW

The OCR watcher runs a continuous loop:

```
┌─────────────────────────────────────────────────────────────────┐
│                         OCR CYCLE (every 5s)                     │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Get      │───▶│ Crop     │───▶│ OCR      │───▶│ Compare  │  │
│  │ Screenshot│    │ Regions  │    │ Extract  │    │ Hashes   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                        │        │
│                                         ┌──────────────┘        │
│                                         ▼                       │
│                                  ┌──────────┐    ┌──────────┐  │
│                                  │ Changed? │───▶│ Emit     │  │
│                                  │          │ Yes│ Diff     │  │
│                                  └──────────┘    └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## STEPS

### Step 1: Get Latest Screenshot

```python
def get_latest_screenshot() -> Path | None:
    # Find most recent screen_*.png in SCREENSHOT_DIR
    # Return None if no screenshots or too old (>30s)
```

**Inputs:** `SCREENSHOT_DIR` path
**Outputs:** Path to latest screenshot or None
**Failure:** Returns None, cycle skips

### Step 2: Load and Validate Image

```python
def load_image(path: Path) -> Image:
    # Open with PIL
    # Verify it's a valid image
    # Return Image object
```

**Inputs:** Screenshot path
**Outputs:** PIL Image object
**Failure:** Logs error, cycle skips

### Step 3: Crop Regions

```python
def crop_region(img: Image, region: ScreenRegion) -> Image:
    # Convert percentage coords to pixels
    # left = width * region.x
    # top = height * region.y
    # right = width * (region.x + region.w)
    # bottom = height * (region.y + region.h)
    # Return cropped image
```

**Inputs:** Full image, region definition
**Outputs:** Cropped image for that region

### Step 4: Preprocess for OCR

```python
def preprocess_for_ocr(img: Image) -> Image:
    # Convert to grayscale
    # Auto-contrast (improve readability)
    # Sharpen
    # Scale up 2x (better OCR accuracy)
    # Return processed image
```

**Rationale:** Game UIs often have stylized text. Preprocessing improves Tesseract accuracy.

### Step 5: Extract Text (OCR)

```python
def ocr_region(img: Image, region: ScreenRegion) -> OCRResult:
    cropped = crop_region(img, region)
    processed = preprocess_for_ocr(cropped)
    text = pytesseract.image_to_string(processed, config=TESSERACT_CONFIG)

    # Clean up artifacts
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[|]{2,}', '', text)

    hash = md5(text.encode()).hexdigest()[:12]

    return OCRResult(region=region.name, text=text, hash=hash, timestamp=now())
```

**Config:** `--oem 3 --psm 6 -l eng+fra`
- OEM 3: Default (LSTM + legacy)
- PSM 6: Assume uniform block of text
- Languages: English + French

### Step 6: Compare with Previous State

```python
def detect_changes(current: dict, previous: dict) -> list[TextDiff]:
    diffs = []

    for region_name, current_result in current.items():
        prev = previous.get(region_name)

        if prev is None and len(current_result.text) > MIN_THRESHOLD:
            # New content appeared
            diffs.append(TextDiff(type="new", ...))

        elif prev and current_result.hash != prev.hash:
            # Content changed
            if change_significant(current_result, prev):
                diffs.append(TextDiff(type="changed", ...))

    # Check for disappeared content
    for region_name in previous:
        if region_name not in current:
            diffs.append(TextDiff(type="removed", ...))

    return sorted(diffs, key=lambda d: -d.priority)
```

**Threshold:** MIN_CHANGE_THRESHOLD = 50 characters

### Step 7: Emit Diffs

```python
def append_diff(diff: TextDiff):
    with open(OCR_DIFFS_FILE, "a") as f:
        f.write(json.dumps(asdict(diff)) + "\n")
```

**Output:** Append-only JSONL file

### Step 8: Save State

```python
def save_ocr_state(state: dict):
    OCR_STATE_FILE.write_text(json.dumps({
        "last_results": {name: asdict(r) for name, r in current.items()},
        "last_update": now().isoformat(),
        "screenshot": str(screenshot_path)
    }))
```

---

## EDGE CASES

| Case | Handling |
|------|----------|
| No screenshots | Skip cycle, log warning |
| Screenshot too old (>30s) | Skip cycle |
| OCR fails on region | Return empty text, log error |
| Image corrupted | Skip cycle, log error |
| Empty region (no text) | Don't store in results |
| Repeated identical text | Hash matches, no diff emitted |

---

## OUTPUTS

### Per Cycle
- 0-N diffs appended to `ocr_diffs.jsonl`
- Updated `ocr_state.json` with current region texts

### Diff Structure
```json
{
  "timestamp": "ISO8601",
  "region": "event_popup",
  "change_type": "new|changed|removed",
  "old_text": "previous content",
  "new_text": "current content",
  "summary": "[region] Human-readable summary",
  "priority": 1-10
}
```

---

## COMPLEXITY

| Operation | Time | Space |
|-----------|------|-------|
| Screenshot load | O(1) | O(pixels) |
| Region crop | O(1) per region | O(region_pixels) |
| OCR | O(pixels) per region | O(text_length) |
| Diff detection | O(regions) | O(1) |
| Total per cycle | ~500ms | ~50MB |
