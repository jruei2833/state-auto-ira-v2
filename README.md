# State Auto-IRA Research Project (v2)

## Project Overview

This project identifies firms across states with auto-IRA mandates that chose to establish their own 401(k) plans rather than enrolling employees in state programs. The research builds on Sita Slavov's finding that state mandates act as catalysts—not crowding out private retirement plans, but prompting firms to start their own.

**Client:** America First Policy
**Researcher:** Janyjor
**Deadline:** February 2, 2026

## Research Question

Which firms, in states with auto-IRA mandates, chose to establish their own 401(k) plans after the mandate took effect?

## Methodology

Two independent AI tools (Codex and Claude Code) build datasets from the same source (DOL Form 5500 bulk data). Results are cross-validated to ensure data quality.

### Data Source
- DOL Form 5500 bulk datasets (2017-2024)
- URL: https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets

### Target States and Mandate Dates
| State | Program | Mandate Effective |
|-------|---------|-------------------|
| Oregon | OregonSaves | November 2017 |
| Illinois | Secure Choice | May 2018 |
| California | CalSavers | November 2018 |
| Connecticut | MyCTSavings | April 2022 |
| Maryland | MarylandSaves | September 2022 |
| Colorado | SecureSavings | January 2023 |
| Virginia | RetirePath | July 2023 |
| Maine | - | January 2024 |
| Delaware | EARNS | January 2024 |
| New Jersey | - | March 2024 |
| Vermont | - | July 2025 |

### Filtering Criteria
- Plan type: 401(k) / defined contribution (pension code 2J)
- Single-employer plans only
- Plan effective date (PLNEFF_DT) after state mandate date
- Deduplicated by EIN (unique firms)

## Folder Structure
```
state-auto-ira-v2/
├── README.md
├── data/
│   ├── codex/           # Codex dataset output
│   └── claude-code/     # Claude Code dataset output
├── methodology/
│   ├── codex-methodology.md
│   └── claude-code-methodology.md
├── validation/
│   └── cross-validation-assessment.md
└── deliverables/
    └── final-dataset.csv
```

## Validation Approach

1. Codex builds dataset independently
2. Claude Code builds dataset independently
3. Cross-audit: each tool reviews the other's output
4. Reconcile differences and document findings

## Key Fields in Output Dataset

| Column | Description |
|--------|-------------|
| Firm Name | Employer/sponsor name |
| EIN | Employer Identification Number |
| State | Two-letter state code |
| City | Firm location |
| Plan Effective Date | When 401(k) was established (PLNEFF_DT) |
| Employee Count | Number of plan participants |
| Employer Contribution | Annual employer contribution amount |
| Industry Code | NAICS code if available |

## References

- Slavov, S. (2024). State Auto-IRA Mandates and Firm Retirement Plan Adoption. NBER Working Paper.
- DOL Form 5500 Data Dictionary
