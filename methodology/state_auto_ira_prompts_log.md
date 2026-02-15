# State Auto-IRA Research Project
## Methodology Prompts Log

**Project:** State Auto-IRA 401(k) Adoption Research  
**Client:** America First Policy  
**Researcher:** Janyjor  
**Date:** February 3, 2026  
**Tools Used:** Claude Code, Codex (OpenAI)

---

## Overview

This document contains all prompts used to build and validate the dataset of firms that established 401(k) plans in response to state auto-IRA mandates. The project used two independent AI tools (Claude Code and Codex) for cross-validation.

---

## Phase 1: Project Setup & Initial Data Pull (Claude Code)

### Prompt 1 - Full Data Pull

```
First, create a new project folder at ~/github/state-auto-ira-v2/ with this structure:

state-auto-ira-v2/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── methodology/
├── validation/
├── scripts/
└── deliverables/

Initialize it as a git repo.

Then, working ONLY within this new folder, build a dataset of firms that established 401(k) plans in response to state auto-IRA mandates.

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
- https://askebsa.dol.gov/FOIA%20Files/2018/All/F_SCH_H_2018_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2019/All/F_SCH_H_2019_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2020/All/F_SCH_H_2020_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2021/All/F_SCH_H_2021_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2022/All/F_SCH_H_2022_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2023/All/F_SCH_H_2023_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2024/All/F_SCH_H_2024_All.zip

Schedule I (employer contributions - small plans):
- https://askebsa.dol.gov/FOIA%20Files/2017/All/F_SCH_I_2017_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2018/All/F_SCH_I_2018_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2019/All/F_SCH_I_2019_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2020/All/F_SCH_I_2020_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2021/All/F_SCH_I_2021_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2022/All/F_SCH_I_2022_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2023/All/F_SCH_I_2023_All.zip
- https://askebsa.dol.gov/FOIA%20Files/2024/All/F_SCH_I_2024_All.zip

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
   - firm_name
   - ein
   - state
   - city
   - plan_effective_date
   - employee_count
   - employer_contribution_amount
   - plan_year

2. /methodology/METHODOLOGY.md documenting:
   - Exact files downloaded
   - Filters applied
   - Join logic used
   - Record counts at each filtering step

3. /deliverables/summary_statistics.csv with:
   - Record count by state
   - Average employees by state
   - Total/average employer contribution by state

Do not reference any files from previous project attempts. This is a fresh start.
```

**Result:** Claude Code produced 112,142 unique firms across 10 states.

---

## Phase 2: Verification Prompts (Claude Code)

### Prompt 2 - Verify California Dates

```
Can you show me 5 sample records from California with their plan_effective_date to confirm they are all after November 1, 2018?
```

**Result:** All California records confirmed to have plan effective dates after November 1, 2018. Earliest CA plan in dataset: November 4, 2018.

---

### Prompt 3 - Verify 2J Filter

```
Can you confirm all 112,142 records have TYPE_PENSION_BNFT_CODE containing "2J"?
```

**Result:** 100% of filtered records contain "2J" pension benefit code, confirming all are 401(k) plans.

---

### Prompt 4 - Verify Multi-Employer Exclusion

```
Did you filter out multi-employer plans? How many were excluded?
```

**Result:** 
- Excluded: 16,768 multi-employer/multiple-employer plans
- Kept: 1,643,712 single-employer plans (99.0%)
- Filter used: TYPE_PLAN_ENTITY_CD = 1

---

## Phase 3: Codex Cross-Validation

### Prompt 5 - Codex Data Pull (Initial)

```
The Form 5500 raw data files are already downloaded and located at:
C:\Users\JanyjorRuei\Documents\GITHUB\state-auto-ira-v2\form5500-raw-data

Run the analysis script using --local-dir to point to this folder. Build the dataset of firms that established 401(k) plans in response to state auto-IRA mandates.

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

Run the script now and show me the results.
```

**Issue:** Codex could not access external URLs (blocked in sandboxed environment).

---

### Prompt 6 - Fix Codex Path

```
Option 1 - Update the script to use the correct path:

C:\Users\JanyjorRuei\github\state-auto-ira-v2\form5500-raw-data\

The subfolders are:
- form5500\
- form5500sf\
- schedule_h\
- schedule_i\

Update the script and re-run it.
```

**Result:** Codex produced 112,142 unique firms - matching Claude Code exactly.

---

## Phase 4: Final Documentation

### Prompt 7 - Cross-Validation Report

```
Create a cross-validation report at ~/github/state-auto-ira-v2/validation/cross_validation_report.md that documents:

1. Tools used: Claude Code and Codex
2. Data source: DOL Form 5500 bulk datasets (2017-2024)
3. Methodology: Both tools applied identical filtering criteria
4. Results: Both tools produced 112,142 unique firms with identical state-by-state counts
5. Conclusion: Cross-validation PASSED - datasets are verified

Include a comparison table showing the state-by-state match.
```

**Result:** Cross-validation report created.

---

### Prompt 8 - Final Deliverables

```
Yes, please:

1. Add total record counts to the cross_validation_report.md
2. Add today's date (February 3, 2026) to the report
3. Update the README.md to link to the cross_validation_report.md
4. Create a final deliverables summary in ~/github/state-auto-ira-v2/deliverables/FINAL_SUMMARY.md that includes:
   - Project overview (State Auto-IRA research for America First Policy)
   - Key finding: 112,142 firms established 401(k) plans after state mandates
   - Data source and methodology summary
   - List of output files and their locations
   - Cross-validation status: PASSED
```

**Result:** All final documentation created.

---

## Command Line Commands (Windows)

```cmd
cd C:\Users\JanyjorRuei\github\state-auto-ira-v2
pip install pandas requests
python scripts/build_dataset.py
```

---

## Cross-Validation Results

| State | Claude Code | Codex | Match |
|-------|-------------|-------|-------|
| CA | 79,485 | 79,485 | ✅ |
| IL | 14,035 | 14,035 | ✅ |
| OR | 7,015 | 7,015 | ✅ |
| MD | 3,464 | 3,464 | ✅ |
| CO | 2,630 | 2,630 | ✅ |
| CT | 2,332 | 2,332 | ✅ |
| VA | 2,054 | 2,054 | ✅ |
| NJ | 783 | 783 | ✅ |
| DE | 207 | 207 | ✅ |
| ME | 137 | 137 | ✅ |
| **TOTAL** | **112,142** | **112,142** | ✅ |

**Cross-Validation Status: PASSED**

---

## Final Deliverables

| File | Location | Description |
|------|----------|-------------|
| Dataset | `data/processed/state_auto_ira_401k_dataset.csv` | 112,142 firms |
| Summary Stats | `deliverables/summary_statistics.csv` | By state |
| Methodology | `methodology/METHODOLOGY.md` | Full documentation |
| Cross-Validation | `validation/cross_validation_report.md` | Validation report |
| Final Summary | `deliverables/FINAL_SUMMARY.md` | Executive summary |
| README | `README.md` | Project overview |
| This Document | `methodology/PROMPTS_LOG.md` | All prompts used |

---

*Document generated: February 3, 2026*
