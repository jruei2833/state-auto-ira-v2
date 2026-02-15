# State Auto-IRA Research Project

**Identifying firms that established their own 401(k) plans instead of using state auto-IRA programs**

---

## The Research Question

When states mandate that employers provide retirement savings access, employers have a choice: enroll employees in the state's auto-IRA program (cheaper, less administrative burden) or establish their own 401(k) plan (more costly, more complex). The mandate only requires the cheaper option — so why do some firms voluntarily choose the more expensive path?

This is the question at the heart of Sita Slavov's NBER research. Her work finds that state auto-IRA mandates act as *catalysts* for private retirement plan formation rather than crowding out employer-sponsored plans. The mandates appear to prompt firms to think about retirement benefits, and some decide that a full 401(k) — with employer matching, greater investment options, and higher contribution limits — better serves their business goals.

But Slavov's research, based on aggregate administrative tax data, couldn't identify *which specific firms* made this choice. Without a firm-level dataset, the follow-up question remains unanswered: **what types of firms tend to set up their own 401(k) rather than defaulting to the state program?**

This project fills that gap.

---

## What This Dataset Provides

Using DOL Form 5500 filings, we identified **106,577 to 115,690 firms** (depending on mandate date definition) across 10 states that established new 401(k) plans after their state's auto-IRA mandate took effect. Each record includes firm name, EIN, state, city, plan start date, and employee count — enabling the kind of firm-level analysis that wasn't previously possible.

This dataset can support research into questions like:
- Are mandate-responsive firms concentrated in certain industries or firm sizes?
- Do firms in states with earlier mandates show different patterns than later adopters?
- What is the relationship between firm size and the decision to establish a 401(k) vs. use the state program?
- How do employer contribution patterns vary across mandate-responsive firms?

---

## Datasets

Two versions using different mandate date definitions:

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

- **Claude.ai audited Antigravity's work**: PASS
- **Antigravity audited Claude.ai's script**: PASS — 3 mandate dates adjusted per recommendation

---

## Known Limitations

1. **Correlation, not causation**: The dataset identifies firms that started 401(k)s after mandates, but cannot prove the mandate caused the decision. Establishing causality would require difference-in-differences analysis comparing mandate states to non-mandate states, or qualitative evidence such as firm statements citing the mandate.
2. **Employer contribution coverage**: Only 3.4-3.7% of records have contribution amounts. Form 5500-SF filers (~95% of dataset) do not file Schedule H/I. Match formulas (e.g., "50% up to 6%") are not available in Form 5500 data — they are disclosed in Summary Plan Descriptions (SPDs).
3. **Filing lag**: Plans established in late 2024 won't fully appear until 2025-2026, so recent mandate states (ME, DE, NJ) are underrepresented.
4. **Zero-employee plans**: 15.2% of records show 0 employees (newly established or solo entrepreneur plans).

---

## Recommended Next Steps

1. **Firm-level analysis**: Use the dataset to characterize which types of firms chose 401(k)s — by industry, size, geography, and contribution patterns
2. **Difference-in-differences**: Pull Form 5500 data for non-mandate states as a control group to establish whether mandates caused the observed 401(k) adoption
3. **Qualitative evidence**: Search for press releases, company statements, or news articles where firms cite the state mandate as motivation for establishing a 401(k)
4. **Alternative contribution data**: Explore BrightScope, Vanguard's How America Saves, or PSCA Annual Survey for match formula data
5. **Annual refresh**: Re-run as new Form 5500 filings become available (Vermont's July 2025 mandate will generate data in 2026)

---

## Reproducing the Dataset

Requires ~6 GB of raw Form 5500 data downloaded from the DOL website.

```bash
# Download raw data to form5500-raw-data/ (see methodology for file list)
# Then run:
python build_both.py
```

This produces both v1-inclusive and v2-conservative datasets. See `methodology/state_auto_ira_prompts_log.md` for the complete record of prompts and tools used across all runs.

---

## References

- Slavov, S. (2024). "State Auto-IRA Mandates and Firm Retirement Plan Adoption." NBER Working Paper.
- DOL Form 5500 Data Dictionary and Filing Instructions
- CalSavers, OregonSaves, Illinois Secure Choice program documentation
