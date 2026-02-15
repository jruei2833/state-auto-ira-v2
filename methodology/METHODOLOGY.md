# Methodology: State Auto-IRA 401(k) Dataset

Generated: 2026-02-15 13:26

## Data Source
DOL Form 5500 bulk datasets (2017-2024) from EFAST2 system.

## Filtering Criteria
1. TYPE_PENSION_BNFT_CODE contains '2J' (401(k) plans)
2. Single-employer plans (Form 5500: entity code 2, Form 5500-SF: entity code 1)
3. State is one of the 10 mandate states
4. PLAN_EFF_DATE is after the state mandate date
5. Deduplicated by EIN for unique firms

## State Mandate Dates
| State | Program | Mandate Date |
|-------|---------|-------------|
| CA | CalSavers | 2018-11-01 |
| CO | SecureSavings | 2023-01-01 |
| CT | MyCTSavings | 2022-04-01 |
| DE | EARNS | 2024-01-01 |
| IL | Secure Choice | 2018-05-01 |
| MD | MarylandSaves | 2022-09-01 |
| ME | Maine Retirement Savings | 2024-01-01 |
| NJ | RetireReady NJ | 2024-03-01 |
| OR | OregonSaves | 2017-11-01 |
| VA | RetirePath | 2023-07-01 |

## Results
- Total unique firms: 115,690
- States with data: 10
