# State Auto-IRA Research Project

**Identifying firms that established 401(k) plans in response to state auto-IRA mandates**

---

## Key Finding

State auto-IRA mandates act as catalysts for private retirement plan formation. We identified **106,577 to 115,690 unique firms** (depending on mandate date definition) across 10 states that established 401(k) plans after their state's auto-IRA mandate took effect, supporting Sita Slavov's NBER research.

---

## Datasets

This project provides two dataset versions using different mandate date definitions:

| Version | Firms | Approach | Use Case |
|---------|-------|----------|----------|
| **v1-inclusive** | 115,690 | Legislation/regulation dates | Maximum mandate impact |
| **v2-conservative** | 106,577 | Program launch/enforcement dates | Conservative, defensible estimates |

The 9,113-firm difference is almost entirely in California (8,540 firms) due to the gap between regulations being adopted (Nov 2018) and CalSavers launching statewide (Jul 2019). See `data/data_README.md` for full comparison.

### State-by-State Results

| State | Program | v1-inclusive | v2-conservative |
|-------|---------|-------------|-----------------|
| California | CalSavers | 81,512 | 72,972 |
| Illinois | Secure Choice | 14,793 | 14,513 |
| Oregon | OregonSaves | 7,308 | 7,313 |
| Maryland | MarylandSaves | 3,556 | 3,556 |
| Colorado | SecureSavings | 2,787 | 2,786 |
| Connecticut | MyCTSavings | 2,410 | 2,409 |
| Virginia | RetirePath | 2,150 | 2,150 |
| New Jersey | RetireReady NJ | 816 | 603 |
| Delaware | EARNS | 215 | 132 |
| Maine | Maine Retirement Savings | 143 | 143 |

---

## Repository Structure

```
state-auto-ira-v2/
├── README.md                          # This file
├── build_both.py                      # Script to reproduce both datasets
├── build_dataset.py                   # Single-version build script
├── data/
│   ├── data_README.md                 # Explains v1 vs v2 differences
│   ├── v1-inclusive/                   # 115,690 firms (legislation dates)
│   │   ├── state_auto_ira_401k_dataset.csv
│   │   └── summary_statistics.csv
│   ├── v2-conservative/               # 106,577 firms (launch dates)
│   │   ├── state_auto_ira_401k_dataset.csv
│   │   └── summary_statistics.csv
│   └── processed/                     # Latest single build output
├── deliverables/
│   ├── State_AutoIRA_Project_Report.md
│   ├── FINAL_SUMMARY.md
│   └── summary_statistics.csv
├── methodology/
│   ├── METHODOLOGY.md
│   └── state_auto_ira_prompts_log.md
├── validation/
│   ├── cross_validation_report.md
│   ├── claude_ai_audit_of_antigravity.md
│   ├── antigravity_audit_of_claude_ai.md
│   ├── spot_check_results.txt
│   └── audit_results.txt
└── form5500-raw-data/                 # NOT in repo (too large, in .gitignore)
    ├── form5500/                      # ~1.3 GB
    ├── form5500sf/                    # ~4.0 GB
    ├── schedule_h/                    # ~450 MB
    └── schedule_i/                    # ~160 MB
```

---

## Data Source

DOL Form 5500 bulk datasets (2017-2024) via the EFAST2 system:
https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets

### Files Used

| File | Description | Size (8 years) |
|------|-------------|----------------|
| Form 5500 | Large plan filings (100+ participants) | ~1.3 GB |
| Form 5500-SF | Small plan filings (<100 participants) | ~4.0 GB |
| Schedule H | Large plan financial data | ~450 MB |
| Schedule I | Small plan financial data | ~160 MB |

---

## Methodology

1. **Filter** Form 5500 and 5500-SF for 401(k) plans (pension code 2J)
2. **Filter** for single-employer plans (entity code 2 for Form 5500, code 1 for 5500-SF)
3. **Filter** for 10 mandate states (OR, IL, CA, CT, MD, CO, VA, ME, DE, NJ)
4. **Filter** for plans with effective dates after the state's mandate date
5. **Deduplicate** by EIN to count unique firms
6. **Join** employer contribution data from Schedule H/I (3.4-3.7% match rate)

### Filtering Criteria

| Filter | Form 5500 | Form 5500-SF |
|--------|-----------|--------------|
| 401(k) plans | TYPE_PENSION_BNFT_CODE contains "2J" | SF_TYPE_PENSION_BNFT_CODE contains "2J" |
| Single-employer | TYPE_PLAN_ENTITY_CD = 2 | SF_PLAN_ENTITY_CD = 1 |
| Plan start date | PLAN_EFF_DATE > mandate date | SF_PLAN_EFF_DATE > mandate date |
| Firm name | SPONSOR_DFE_NAME | SF_SPONSOR_NAME |

---

## Validation

### Cross-Validation (3 tools)

| Tool | Run | Records | Status |
|------|-----|---------|--------|
| Google Antigravity | v1 (Jan 2026) | 80,453 | Superseded by v2 |
| Claude Code | v1 (Jan 2026) | 112,385 | Superseded by v2 |
| Codex | v2 (Feb 2026) | 112,142 | 100% match with Claude Code v2 |
| Claude Code | v2 (Feb 2026) | 112,142 | 100% match with Codex |
| build_dataset.py | v3 (Feb 2026) | 115,690 / 106,577 | Current (with EIN fix + name fix) |

### Spot Check

20 randomly sampled firms verified against raw Form 5500 data: **18/20 passed** all checks. 2 firms had cosmetic EIN display issues (firms exist, padding mismatch).

### Independent Audits

- **Claude.ai audited Antigravity's work**: PASS — FIRM_NAME fix correctly diagnosed and implemented
- **Antigravity audited Claude.ai's script**: PASS — filtering logic fundamentally sound, 3 mandate dates adjusted per recommendation

---

## Known Limitations

1. **Employer contribution coverage**: Only 3.4-3.7% of records have contribution amounts. Form 5500-SF filers (~95% of dataset) do not file Schedule H/I.
2. **Correlation, not causation**: Cannot prove mandates caused 401(k) establishment. Would require difference-in-differences analysis.
3. **Filing lag**: Plans established in late 2024 won't fully appear until 2025-2026.
4. **Match formulas unavailable**: Only aggregate contribution dollars, not match percentages (e.g., "50% up to 6%").
5. **Zero-employee plans**: 15.2% of records show 0 employees (newly established or solo plans).

---

## Reproducing the Dataset

Requires ~6 GB of raw Form 5500 data downloaded from the DOL website.

```bash
# Download raw data to form5500-raw-data/ (see methodology for file list)
# Then run:
python build_both.py
```

This produces both v1-inclusive and v2-conservative datasets.

---

## References

- Slavov, S. (2024). "State Auto-IRA Mandates and Firm Retirement Plan Adoption." NBER Working Paper.
- DOL Form 5500 Data Dictionary and Filing Instructions
- CalSavers, OregonSaves, Illinois Secure Choice program documentation
