# State Auto-IRA Research Project — Prompts Log

**Purpose:** Complete record of every prompt used across all tools for full reproducibility.

---

## Overview of Runs

| Run | Tools | Result | Status |
|-----|-------|--------|--------|
| v1 (Jan 2026) | Google Antigravity + Claude Code | 80,453 / 112,385 | Superseded — filtering discrepancies |
| v2 (Feb 2026) | Claude Code + Codex | 112,142 / 112,142 | 100% match, but FIRM_NAME bug |
| v3 (Feb 2026) | build_dataset.py + Antigravity audit | 115,690 / 106,577 | Current — two versions with fixes |

---

## Phase 1: Claude Code Dataset Build (v2)

### Prompt 1 — Initial Data Pull

**Tool:** Claude Code
**Date:** February 3, 2026

```
I'm researching firms that established their own 401(k) plans in response to state auto-IRA
mandates. I need you to build a complete dataset using DOL Form 5500 bulk data.

**DATA SOURCES - EXACT URLs:**
Download the "All" datasets (not "Latest") from DOL EFAST2 for years 2017-2024:

Form 5500 (large plans):
- https://askebsa.dol.gov/FOIA%20Files/2017/All/F_5500_2017_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2018/All/F_5500_2018_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2019/All/F_5500_2019_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2020/All/F_5500_2020_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2021/All/F_5500_2021_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2022/All/F_5500_2022_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2023/All/F_5500_2023_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2024/All/F_5500_2024_All.zip

Form 5500-SF (small plans):
- https://askebsa.dol.gov/FOIA%20Files/2017/All/F_5500_SF_2017_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2018/All/F_5500_SF_2018_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2019/All/F_5500_SF_2019_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2020/All/F_5500_SF_2020_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2021/All/F_5500_SF_2021_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2022/All/F_5500_SF_2022_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2023/All/F_5500_SF_2023_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2024/All/F_5500_SF_2024_All.zip

Schedule H (employer contributions - large plans):
- https://askebsa.dol.gov/FOIA%20Files/2017/All/F_SCH_H_2017_All.zip
  (repeat for 2018-2024)

Schedule I (employer contributions - small plans):
- https://askebsa.dol.gov/FOIA%20Files/2017/All/F_SCH_I_2017_All.zip
  (repeat for 2018-2024)

**KEY FIELDS TO EXTRACT:**
From Form 5500/5500-SF:
- ACK_ID (for joining tables)
- SPONS_DFE_EIN (Employer ID)
- SPONS_DFE_MAIL_US_STATE or SPONS_DFE_LOC_US_STATE (State)
- SPONS_DFE_LOC_US_CITY (City)
- SPONSOR_DFE_NAME (Firm name)
- PLNEFF_DT (Plan Effective Date - CRITICAL for filtering)
- TYPE_PENSION_BNFT_CODE (must contain "2J" for 401k)
- TYPE_PLAN_ENTITY_CD (must equal "1" for single-employer)
- TOT_PARTCP_BOY_CNT (Participants)

From Schedule H/I:
- ACK_ID (for joining)
- EMPLR_CONTRIB_EOY_AMT or EMPLR_CONTRIB_AMT (Employer contribution)

**TARGET STATES AND MANDATE EFFECTIVE DATES:**
- Oregon (OR): November 1, 2017
- Illinois (IL): May 1, 2018
- California (CA): November 1, 2018
- Connecticut (CT): April 1, 2022
- Maryland (MD): September 1, 2022
- Colorado (CO): January 1, 2023
- Virginia (VA): July 1, 2023
- Maine (ME): January 1, 2024
- Delaware (DE): January 1, 2024
- New Jersey (NJ): March 1, 2024
- Vermont (VT): July 1, 2025

**FILTERING CRITERIA:**
1. TYPE_PENSION_BNFT_CODE contains "2J" (401k plans only)
2. TYPE_PLAN_ENTITY_CD = "1" (single-employer plans only, exclude multi-employer)
3. State is one of: OR, IL, CA, CT, MD, CO, VA, ME, DE, NJ, VT
4. PLNEFF_DT (Plan Effective Date) is AFTER that state's mandate date
5. Deduplicate by EIN to get unique FIRMS (not unique plans)

**OUTPUT:**
1. /data/processed/state_auto_ira_401k_dataset.csv with columns:
   - firm_name, ein, state, city, plan_effective_date, employee_count,
     employer_contribution_amount, plan_year
2. /methodology/METHODOLOGY.md documenting:
   - Exact files downloaded, filters applied, join logic used,
     record counts at each filtering step
3. /deliverables/summary_statistics.csv with:
   - Record count by state, average employees, average employer contribution

Do not reference any files from previous project attempts. This is a fresh start.
```

**Result:** 112,142 unique firms across 10 states (VT excluded — mandate not yet effective)

### Prompt 2 — Verify California Dates

**Tool:** Claude Code

```
Can you show me 5 sample records from California with their plan_effective_date
to confirm they are all after November 1, 2018?
```

### Prompt 3 — Verify 2J Filter

**Tool:** Claude Code

```
Can you confirm all 112,142 records have TYPE_PENSION_BNFT_CODE containing "2J"?
```

### Prompt 4 — Verify Multi-Employer Exclusion

**Tool:** Claude Code

```
Did you filter out multi-employer plans? How many were excluded?
```

**Result:** 16,768 multi-employer plans correctly excluded.

---

## Phase 2: Codex Cross-Validation

### Prompt 5 — Codex Data Pull

**Tool:** Codex (OpenAI)
**Date:** February 3, 2026

```
The Form 5500 raw data files are already downloaded and located at:
C:\Users\JanyjorRuei\Documents\GITHUB\state-auto-ira-v2\form5500-raw-data

The subfolders are:
- form5500/
- form5500sf/
- schedule_h/
- schedule_i/

Build the dataset of firms that established 401(k) plans in response to state
auto-IRA mandates.

**FILTERING CRITERIA:**
1. TYPE_PENSION_BNFT_CODE contains "2J" (401k plans only)
2. TYPE_PLAN_ENTITY_CD = "1" (single-employer plans only)
3. State is one of: OR, IL, CA, CT, MD, CO, VA, ME, DE, NJ, VT
4. PLNEFF_DT (Plan Effective Date) is AFTER that state's mandate date:
   - Oregon (OR): November 1, 2017
   - Illinois (IL): May 1, 2018
   - California (CA): November 1, 2018
   - Connecticut (CT): April 1, 2022
   - Maryland (MD): September 1, 2022
   - Colorado (CO): January 1, 2023
   - Virginia (VA): July 1, 2023
   - Maine (ME): January 1, 2024
   - Delaware (DE): January 1, 2024
   - New Jersey (NJ): March 1, 2024
   - Vermont (VT): July 1, 2025
5. Deduplicate by EIN to get unique FIRMS

**OUTPUT:**
1. state_auto_ira_401k_codex.csv (the dataset)
2. METHODOLOGY.md (documenting the process)
3. summary_statistics.csv (record count, avg employees, avg contribution by state)
```

**Result:** 112,142 firms — 100% match with Claude Code.

---

## Phase 3: build_dataset.py (v3, Python script)

### Prompt 6 — Script Creation

**Tool:** Claude.ai
**Date:** February 15, 2026

```
The output datasets from both Codex and Claude Code never made it into the repo.
All the raw Form 5500 data (~6GB) is in form5500-raw-data/. Write me a Python
script I can run locally to regenerate the dataset.

Filter criteria:
- TYPE_PENSION_BNFT_CODE contains "2J" (401k plans)
- TYPE_PLAN_ENTITY_CD: code 2 for Form 5500, code 1 for Form 5500-SF (single-employer)
- States: OR, IL, CA, CT, MD, CO, VA, ME, DE, NJ
- PLNEFF_DT after state mandate date
- Deduplicate by EIN for unique firms
- Include employer contributions from Schedule H and Schedule I
```

**Result:** 115,690 firms (v1-inclusive). Differences from 112,142 explained by entity code
handling (`"2.0"` vs `"2"` float/string issue) and EIN padding fix.

### Prompt 7 — Mandate Date Corrections

**Tool:** Claude.ai
**Date:** February 15, 2026

Applied corrections based on Antigravity's audit:

```
Update build_dataset.py with corrected mandate dates:
- Illinois: May 1, 2018 → November 1, 2018 (first enforcement deadline)
- California: November 1, 2018 → July 1, 2019 (CalSavers statewide launch)
- Delaware: January 1, 2024 → July 1, 2024 (EARNS program launch)
- New Jersey: March 1, 2024 → June 30, 2024 (RetireReady NJ launch)

Also fix EIN padding: add .str.replace('.0', '', regex=False) before .str.zfill(9)
```

**Result:** 106,577 firms (v2-conservative).

### Prompt 8 — Build Both Versions

**Tool:** Claude.ai
**Date:** February 15, 2026

```
Keep both versions — the 115,690 and the 106,577 — in separate folders with an
explanation. Create a single script (build_both.py) that generates both from the
raw data.
```

**Result:** `build_both.py` producing:
- `data/v1-inclusive/` — 115,690 firms
- `data/v2-conservative/` — 106,577 firms

---

## Phase 4: Cross-Audits

### Prompt 9 — Claude.ai Audits Antigravity

**Tool:** Claude.ai
**Date:** February 15, 2026

Based on review of Antigravity's terminal output and project report. Verified:
- FIRM_NAME column fix (SPONS_DFE_DBA_NAME → SPONSOR_DFE_NAME, SF_SPONS_DBA_NAME → SF_SPONSOR_NAME)
- Dataset count consistency
- State-by-state match

**Output:** `validation/claude_ai_audit_of_antigravity.md`

### Prompt 10 — Antigravity Audits Claude.ai

**Tool:** Google Antigravity (Claude Code)
**Date:** February 15, 2026

```
Please audit the build_dataset.py script that was originally created by Claude.ai
for the State Auto-IRA project. The script is in the repo root. Your job is to
review it as an independent validator.

Check the following:
1. FILTERING LOGIC: Does the 2J pension code filter correctly identify 401(k) plans?
   Is the single-employer filter correct (code 2 for Form 5500, code 1 for 5500-SF)?
2. MANDATE DATES: Are all 10 state mandate dates accurate?
3. DEDUPLICATION: Is EIN-based dedup correctly implemented? Does keeping the most
   recent record make sense?
4. DATE FILTERING: Does the script correctly exclude plans established BEFORE the
   mandate date?
5. CONTRIBUTION JOIN: Is the Schedule H/I join logic sound? Why is coverage only 3.7%?
6. EDGE CASES: Could any records be incorrectly included or excluded?
7. COUNT COMPARISON: The original Codex + Claude Code runs produced 112,142 firms.
   This script produces 115,690. Can you explain the 3,548 difference?

Verify by spot-checking 20 random firms from data/processed/state_auto_ira_401k_dataset.csv
against the raw Form 5500 files to confirm they meet all filtering criteria.

Save your audit report to validation/antigravity_audit_of_claude_ai.md
```

**Output:** `validation/antigravity_audit_of_claude_ai.md`
- 18/20 spot check passed (2 had cosmetic EIN padding issue)
- 3 mandate dates flagged for review → corrected in v2-conservative
- Script rated "fundamentally sound"

---

## Key Column Mappings (Discovered During Project)

These exact column names are critical for reproducibility:

### Form 5500

| Purpose | Column Name |
|---------|-------------|
| Pension type | TYPE_PENSION_BNFT_CODE |
| Entity type | TYPE_PLAN_ENTITY_CD (single-employer = **2**) |
| Plan effective date | PLAN_EFF_DATE |
| State | SPONS_DFE_MAIL_US_STATE |
| EIN | SPONS_DFE_EIN |
| Firm name | SPONSOR_DFE_NAME (NOT SPONS_DFE_DBA_NAME) |
| City | SPONS_DFE_MAIL_US_CITY |
| Plan name | PLAN_NAME |
| Participants | TOT_PARTCP_BOY_CNT |

### Form 5500-SF

| Purpose | Column Name |
|---------|-------------|
| Pension type | SF_TYPE_PENSION_BNFT_CODE |
| Entity type | SF_PLAN_ENTITY_CD (single-employer = **1**) |
| Plan effective date | SF_PLAN_EFF_DATE |
| State | SF_SPONS_US_STATE |
| EIN | SF_SPONS_EIN |
| Firm name | SF_SPONSOR_NAME (NOT SF_SPONS_DBA_NAME) |
| City | SF_SPONS_US_CITY |
| Plan name | SF_PLAN_NAME |
| Participants | SF_TOT_PARTCP_BOY_CNT |

**Critical notes:**
- Entity code meanings are DIFFERENT between Form 5500 and 5500-SF
- DBA name columns are mostly empty — use SPONSOR_DFE_NAME / SF_SPONSOR_NAME
- EINs stored as floats need `.str.replace('.0', '', regex=False)` before zero-padding

---

## Mandate Date Versions

### v1-inclusive (legislation/regulation dates)

| State | Date | Basis |
|-------|------|-------|
| OR | 2017-11-01 | First employer deadline |
| IL | 2018-05-01 | Program "went live" |
| CA | 2018-11-01 | Regulations adopted |
| CT | 2022-04-01 | Registration opened |
| MD | 2022-09-01 | Statewide launch |
| CO | 2023-01-01 | Program launched |
| VA | 2023-07-01 | Program opened |
| ME | 2024-01-01 | Program launched |
| DE | 2024-01-01 | Legislation effective |
| NJ | 2024-03-01 | Regulations finalized |

### v2-conservative (program launch/enforcement dates)

| State | Date | Basis |
|-------|------|-------|
| OR | 2017-11-01 | First employer deadline |
| IL | 2018-11-01 | First enforcement deadline |
| CA | 2019-07-01 | CalSavers statewide launch |
| CT | 2022-04-01 | Registration opened |
| MD | 2022-09-01 | Statewide launch |
| CO | 2023-01-01 | Program launched |
| VA | 2023-07-01 | Program opened |
| ME | 2024-01-01 | Program launched |
| DE | 2024-07-01 | EARNS program launch |
| NJ | 2024-06-30 | RetireReady NJ launch |

---

## Bugs Discovered and Fixed

| Bug | Impact | Fix |
|-----|--------|-----|
| Wrong name columns (SPONS_DFE_DBA_NAME / SF_SPONS_DBA_NAME) | 99.8% null firm names | Use SPONSOR_DFE_NAME / SF_SPONSOR_NAME |
| Entity code 2 vs 1 confusion between Form 5500 and 5500-SF | 99.7% of Form 5500 records dropped | Use code 2 for Form 5500, code 1 for 5500-SF |
| EIN float-to-string padding (61192265.0 → zfill fails) | 2/20 spot check lookup failures | Add .str.replace('.0', '') before .zfill(9) |
| Mandate dates using legislation vs launch dates | ~9,000 extra records in CA/IL | Created two versions (v1 and v2) |

---

*Prompts log compiled: February 15, 2026*
