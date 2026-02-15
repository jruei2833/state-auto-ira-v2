# Dataset Versions

This project contains two versions of the dataset, differing only in which mandate dates are used to filter firms.

## v1-inclusive (115,690 firms)

Uses the **earliest defensible date** for each state — typically when legislation was signed or regulations were adopted. This captures firms that may have started 401(k) plans in anticipation of the mandate, before the program formally launched.

| State | Mandate Date Used | Basis |
|-------|-------------------|-------|
| OR | November 1, 2017 | First employer deadline |
| IL | **May 1, 2018** | Program "went live" |
| CA | **November 1, 2018** | Regulations adopted |
| CT | April 1, 2022 | Registration opened |
| MD | September 1, 2022 | Statewide launch |
| CO | January 1, 2023 | Program launched |
| VA | July 1, 2023 | Program opened |
| ME | January 1, 2024 | Program launched |
| DE | **January 1, 2024** | Legislation effective |
| NJ | **March 1, 2024** | Regulations finalized |

## v2-conservative (106,577 firms)

Uses the **actual program launch or first enforcement date** for each state. This is more conservative — every firm in this dataset started their 401(k) after the state program was operational.

| State | Mandate Date Used | Basis |
|-------|-------------------|-------|
| OR | November 1, 2017 | First employer deadline |
| IL | **November 1, 2018** | First enforcement deadline |
| CA | **July 1, 2019** | CalSavers statewide launch |
| CT | April 1, 2022 | Registration opened |
| MD | September 1, 2022 | Statewide launch |
| CO | January 1, 2023 | Program launched |
| VA | July 1, 2023 | Program opened |
| ME | January 1, 2024 | Program launched |
| DE | **July 1, 2024** | EARNS program launch |
| NJ | **June 30, 2024** | RetireReady NJ launch |

## Which to use?

- **For policy analysis showing maximum mandate impact:** Use v1-inclusive
- **For conservative estimates tied to program operations:** Use v2-conservative
- **The difference (9,113 firms)** is almost entirely in California (8,560) due to the 8-month gap between regulations being adopted and the program launching

## Common to both versions

- Data source: DOL Form 5500 bulk datasets (2017-2024)
- Filter: Pension code 2J (401(k) plans), single-employer only
- Deduplication: By EIN (unique firms)
- All 10 mandate states represented
