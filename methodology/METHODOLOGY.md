# Methodology: State Auto-IRA 401(k) Dataset

Generated: 2026-02-15 14:48

## Data Source
DOL Form 5500 bulk datasets (2017-2024) from EFAST2 system.

## Filtering Criteria
1. TYPE_PENSION_BNFT_CODE contains '2J' (401(k) plans)
2. Single-employer plans (Form 5500: entity code 2, Form 5500-SF: entity code 1)
3. State is one of the 10 mandate states
4. PLAN_EFF_DATE is after the state mandate date
5. Deduplicated by EIN for unique firms

## Two Versions
- **v1-inclusive**: Uses legislation/regulation dates (more firms)
- **v2-conservative**: Uses program launch dates (fewer firms, more defensible)
- See data/README.md for full comparison
