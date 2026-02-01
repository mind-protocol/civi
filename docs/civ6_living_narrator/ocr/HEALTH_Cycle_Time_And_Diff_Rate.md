# OCR — Health: Cycle Time and Diff Rate

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```

---

## SIGNALS

### H1: Cycle Completion Rate

**What:** Percentage of OCR cycles that complete successfully.

**Healthy:** >= 95%
**Degraded:** 80-95%
**Critical:** < 80%

**How to check:**
```bash
# Count successful cycles in last 100
grep -c "changes detected\|No changes" narrator/logs/daemon.log | tail -100
```

### H2: Cycle Time

**What:** Time to complete one OCR cycle (all regions).

**Healthy:** < 2s
**Degraded:** 2-4s
**Critical:** > 4s (risks missing 5s interval)

**How to check:**
```bash
# Add timing to ocr_watcher.py output
# Or profile with:
time python3 scripts/ocr_watcher.py --game ck3 --once
```

### H3: Diff Rate

**What:** Number of diffs generated per hour.

**Healthy:** 10-100 diffs/hour (game is active, changes detected)
**Degraded:** < 10 diffs/hour (game idle or OCR failing)
**Critical:** 0 diffs/hour for 10+ minutes during active play

**How to check:**
```bash
# Count diffs in last hour
find narrator/state/ocr_diffs.jsonl -mmin -60 -exec wc -l {} \;
```

### H4: High-Priority Diff Rate

**What:** Diffs with priority >= 7 (events, notifications).

**Healthy:** At least 1 high-priority diff per 10 minutes during active play
**Degraded:** No high-priority diffs for 20+ minutes
**Critical:** No high-priority diffs for 60+ minutes during active play

**How to check:**
```bash
# Count high-priority diffs
grep '"priority": [789]' narrator/state/ocr_diffs.jsonl | wc -l
```

### H5: OCR Error Rate

**What:** Percentage of regions that fail OCR.

**Healthy:** < 5%
**Degraded:** 5-20%
**Critical:** > 20%

**How to check:**
```bash
# Look for OCR errors in state
grep -c "OCR Error" narrator/state/ocr_state.json
```

### H6: State File Freshness

**What:** Age of ocr_state.json.

**Healthy:** < 10s (updated every cycle)
**Degraded:** 10-30s
**Critical:** > 30s (OCR watcher not running or stalled)

**How to check:**
```bash
# Check file modification time
stat narrator/state/ocr_state.json
```

---

## ALERTS

| Condition | Severity | Action |
|-----------|----------|--------|
| OCR watcher not running | Critical | Restart: `./run.sh` |
| Cycle time > 4s | Warning | Check CPU, reduce regions |
| No diffs for 30min | Warning | Check screenshot capture |
| All regions empty | Critical | Check game is visible, regions correct |
| Tesseract errors | Warning | Check Tesseract installation |
| Diffs file > 10MB | Warning | Truncate old entries |

---

## MONITORING COMMANDS

```bash
# Is OCR watcher running?
ps aux | grep ocr_watcher

# Latest state
cat narrator/state/ocr_state.json | jq '.last_update'

# Recent diffs
tail -20 narrator/state/ocr_diffs.jsonl | jq -r '.summary'

# High-priority diffs
grep '"priority": 10' narrator/state/ocr_diffs.jsonl | tail -5

# Regions with content
cat narrator/state/ocr_state.json | jq '.last_results | keys'
```

---

## HEALTH CHECK SCRIPT

```bash
#!/bin/bash
# health_check_ocr.sh

echo "=== OCR Health Check ==="

# 1. Process running?
if pgrep -f ocr_watcher.py > /dev/null; then
    echo "✅ OCR watcher running"
else
    echo "❌ OCR watcher NOT running"
    exit 1
fi

# 2. State file fresh?
STATE_AGE=$(( $(date +%s) - $(stat -c %Y narrator/state/ocr_state.json) ))
if [ $STATE_AGE -lt 10 ]; then
    echo "✅ State fresh (${STATE_AGE}s old)"
else
    echo "⚠️  State stale (${STATE_AGE}s old)"
fi

# 3. Recent diffs?
DIFF_COUNT=$(find narrator/state/ocr_diffs.jsonl -mmin -10 -exec wc -l {} \; 2>/dev/null || echo 0)
echo "📊 Diffs in last 10min: $DIFF_COUNT"

# 4. Regions with content
REGIONS=$(cat narrator/state/ocr_state.json | jq '.last_results | keys | length')
echo "📍 Active regions: $REGIONS"

echo "=== Done ==="
```
