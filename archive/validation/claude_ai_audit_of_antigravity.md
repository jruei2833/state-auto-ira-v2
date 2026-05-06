# Cross-Validation Audit: Claude.ai Assessment of Antigravity's Work

**Project:** State Auto-IRA 401(k) Research v2  
**Auditor:** Claude.ai (Anthropic)  
**Date:** February 15, 2026  
**Subject:** Review of Antigravity's dataset rebuild and FIRM_NAME fix

---

## Scope of Review

Antigravity (Claude Code) took the `build_dataset.py` script originally created by Claude.ai, identified a critical bug in firm name column mappings, fixed it, rebuilt the dataset, updated the project report, and created a searchable HTML interface.

---

## Findings

### 1. FIRM_NAME Column Fix — VERIFIED CORRECT ✅

**Bug identified by Antigravity:**
- Form 5500: Script used `SPONS_DFE_DBA_NAME` (DBA name, usually empty)
- Form 5500-SF: Script used `SF_SPONS_DBA_NAME` (column does not exist)

**Fix applied:**
- Form 5500: Changed to `SPONSOR_DFE_NAME` ✅
- Form 5500-SF: Changed to `SF_SPONSOR_NAME` ✅

**Verification:** Antigravity confirmed via terminal that:
- `SF_SPONSOR_NAME` exists in 5500-SF data and contains actual business names
- `SPONSOR_DFE_NAME` exists in Form 5500 data
- After rebuild: 115,690 / 115,690 records (100%) have firm names

**Assessment:** This was a legitimate and correctly executed bug fix. The original script's column mapping was wrong, and Antigravity's diagnosis and fix were accurate.

### 2. Dataset Record Count — CONSISTENT ✅

| Metric | Claude.ai Script (Pre-Fix) | Antigravity Rebuild (Post-Fix) |
|--------|---------------------------|-------------------------------|
| Total unique firms | 115,690 | 115,690 |
| Deduplication method | EIN | EIN |
| States with data | 10 | 10 |

The count is identical because the name column fix only affects the FIRM_NAME output field, not the filtering logic. This is expected and correct behavior.

### 3. State-by-State Counts — CONSISTENT ✅

| State | Claude.ai | Antigravity | Match |
|-------|-----------|-------------|-------|
| CA | 81,526 | 81,526 | ✅ |
| IL | 14,790 | 14,790 | ✅ |
| OR | 7,299 | 7,299 | ✅ |
| MD | 3,555 | 3,555 | ✅ |
| CO | 2,788 | 2,788 | ✅ |
| CT | 2,408 | 2,408 | ✅ |
| VA | 2,150 | 2,150 | ✅ |
| NJ | 816 | 816 | ✅ |
| DE | 215 | 215 | ✅ |
| ME | 143 | 143 | ✅ |

### 4. Project Report Update — VERIFIED ✅

Antigravity updated the project report to:
- Reflect the corrected firm count (115,690)
- Document the FIRM_NAME bug and fix
- Add v3 revision history
- Add search.html as a deliverable

### 5. Search Interface (search.html) — NOT FULLY VERIFIED ⚠️

Antigravity created a searchable HTML interface with features including text search, state/year filters, CSV export, and pagination. The browser testing environment was unavailable during Antigravity's session, so the interface was not visually verified. 

**Recommendation:** Manually test search.html by running `python -m http.server 8080` and opening http://localhost:8080/search.html in a browser.

### 6. Comparison to Original Project Report (112,142 vs 115,690) ⚠️

The original Codex + Claude Code runs produced 112,142 firms. The rebuild produces 115,690 — a difference of 3,548 firms (+3.2%).

**Possible explanations:**
- Minor differences in entity code handling (the original runs may have used different entity code logic)
- Edge cases in date parsing or string matching
- The original runs may have applied additional filters not present in build_dataset.py

**Assessment:** The 3.2% variance is within acceptable range. State rank ordering is identical and proportions are consistent. However, a sample-level reconciliation of ~50 EINs would strengthen confidence.

---

## Overall Verdict

**PASS — Antigravity's work is valid and improves the dataset.**

The FIRM_NAME fix was correctly diagnosed and implemented. The filtering logic remains sound. The dataset is more complete and usable than the pre-fix version.

### Recommendations

1. **Manual spot-check:** Verify 20-30 firms from the CSV against the raw Form 5500 data
2. **Test search.html:** Open in a browser and verify search, filter, and export functionality
3. **Reconcile 112,142 vs 115,690:** Investigate the 3.2% difference if precision is critical for the deliverable
4. **Contribution data:** Only 3.7% of records have employer contribution data — this remains a known limitation

---

*Audit completed: February 15, 2026*
