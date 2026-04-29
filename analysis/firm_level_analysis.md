# Firm-Level Descriptive Analysis (v2-conservative dataset)

**Date:** 2026-04-29
**Dataset:** `data/v2-conservative/state_auto_ira_401k_dataset.csv` (106,577 firms)
**Source filters:** new single-employer 401(k) plans (pension code 2J) with plan effective date after the v2-conservative mandate date in each of 10 mandate states. Deduplicated by EIN.

---

## 1. Firm-size distribution

Size buckets (covered-participant counts from Form 5500 / 5500-SF, beginning-of-year):

- **solo:** 0-1
- **micro:** 2-9
- **small:** 10-49
- **medium:** 50-249
- **large:** 250+

(There is no formal workplan defining these bands. The bands are SBA-style ranges adapted for plan-participant counts; see "Notes" at the end for what would change if the workplan defines them differently.)

| size_bucket   |   n_firms |   pct_of_total |
|:--------------|----------:|---------------:|
| solo          |     21148 |          19.84 |
| micro         |     45459 |          42.65 |
| small         |     32960 |          30.93 |
| medium        |      6260 |           5.87 |
| large         |       742 |           0.7  |
| unknown       |         8 |           0.01 |

The **modal mandate-induced 401(k) is a micro-firm plan**: ~43% of firms in the dataset have 2-9 covered participants. About 20% are solo (0-1 participants) — these are sole proprietorships and very small partnerships establishing owner-only / one-employee 401(k)s. Together, solo + micro account for roughly 62% of all firms in the dataset.

This is consistent with what auto-IRA mandates were designed to do: the threshold for state-program eligibility is typically 5+ employees (varies by state), so very small firms that don't qualify for the state program but still want some retirement vehicle are establishing 401(k)s.

Large firms (250+ participants) are rare (742 firms, 0.70% of total). Most large firms already had 401(k)s before mandates took effect, so the new-plan dataset captures relatively few of them.

## 2. State-by-size distribution

Counts of new 401(k) plans by state and size bucket:

| STATE   |   solo |   micro |   small |   medium |   large |   unknown |   total |
|:--------|-------:|--------:|--------:|---------:|--------:|----------:|--------:|
| CA      |  14115 |   31643 |   22524 |     4217 |     466 |         7 |   72972 |
| CO      |    890 |    1098 |     699 |       90 |       9 |         0 |    2786 |
| CT      |    583 |     981 |     709 |      123 |      12 |         1 |    2409 |
| DE      |     36 |      45 |      40 |        8 |       3 |         0 |     132 |
| IL      |   2447 |    5954 |    4875 |     1054 |     183 |         0 |   14513 |
| MD      |    838 |    1579 |     955 |      171 |      13 |         0 |    3556 |
| ME      |     27 |      43 |      60 |       13 |       0 |         0 |     143 |
| NJ      |    111 |     181 |     254 |       51 |       6 |         0 |     603 |
| OR      |   1399 |    3197 |    2267 |      413 |      37 |         0 |    7313 |
| VA      |    702 |     738 |     577 |      120 |      13 |         0 |    2150 |
| TOTAL   |  21148 |   45459 |   32960 |     6260 |     742 |         8 |  106577 |

Same table as percentages within each state (rows sum to ~100):

| STATE   |   solo |   micro |   small |   medium |   large |   unknown |
|:--------|-------:|--------:|--------:|---------:|--------:|----------:|
| CA      |   19.3 |    43.4 |    30.9 |      5.8 |     0.6 |         0 |
| CO      |   32   |    39.4 |    25.1 |      3.2 |     0.3 |         0 |
| CT      |   24.2 |    40.7 |    29.4 |      5.1 |     0.5 |         0 |
| DE      |   27.3 |    34.1 |    30.3 |      6.1 |     2.3 |         0 |
| IL      |   16.9 |    41   |    33.6 |      7.3 |     1.3 |         0 |
| MD      |   23.6 |    44.4 |    26.9 |      4.8 |     0.4 |         0 |
| ME      |   18.9 |    30.1 |    42   |      9.1 |     0   |         0 |
| NJ      |   18.4 |    30   |    42.1 |      8.5 |     1   |         0 |
| OR      |   19.1 |    43.7 |    31   |      5.6 |     0.5 |         0 |
| VA      |   32.6 |    34.3 |    26.8 |      5.6 |     0.6 |         0 |

**Highest solo share:** VA (32.6%), CO (31.9%), DE (27.3%).
**Lowest solo share:** IL (16.9%), NJ (18.4%), ME (18.9%).

The cross-state variation in solo share is large — high-solo states have nearly twice the solo concentration of low-solo states. This is worth flagging as an interpretation caveat: when we say "X% of firms in mandate states established 401(k)s after mandate," the *kind* of firm differs materially across states. A state with a high solo share is largely capturing self-employed individuals; a state with a low solo share is capturing more genuine employer-employee plan formation.

## 3. Plan-start-year by state

Counts of new plans by year of plan effective date and state:

| start_year   |    CA |   CO |   CT |   DE |    IL |   MD |   ME |   NJ |   OR |   VA |   total |
|:-------------|------:|-----:|-----:|-----:|------:|-----:|-----:|-----:|-----:|-----:|--------:|
| 2017         |     0 |    0 |    0 |    0 |     0 |    0 |    0 |    0 |   13 |    0 |      13 |
| 2018         |     0 |    0 |    0 |    0 |    47 |    0 |    0 |    0 |  886 |    0 |     933 |
| 2019         |   741 |    0 |    0 |    0 |  2018 |    0 |    0 |    0 | 1026 |    0 |    3785 |
| 2020         | 10017 |    0 |    0 |    0 |  1768 |    0 |    0 |    0 |  880 |    0 |   12665 |
| 2021         | 11672 |    0 |    0 |    0 |  2036 |    0 |    0 |    0 |  936 |    0 |   14644 |
| 2022         | 22626 |    0 |  154 |    0 |  2379 |  102 |    0 |    0 | 1019 |    0 |   26280 |
| 2023         | 13639 |  655 | 1379 |    0 |  3279 | 1697 |    0 |    0 | 1376 |  215 |   22240 |
| 2024         | 14068 | 2110 |  856 |  126 |  2955 | 1723 |  129 |  554 | 1155 | 1899 |   25575 |
| 2025         |   209 |   21 |   20 |    6 |    31 |   34 |   14 |   49 |   22 |   36 |     442 |
| TOTAL        | 72972 | 2786 | 2409 |  132 | 14513 | 3556 |  143 |  603 | 7313 | 2150 |  106577 |

Most plans cluster in 2022-2024, reflecting both (a) the staggered roll-out of mandates across states and (b) DOL filing lag — the 2024 effective-year plans are concentrated in Form5500SF_2024 filings, which are still partially incomplete.

Per-state plan-start summary (median, min, max year, n):

| STATE   |   median |   min |   max |     n |
|:--------|---------:|------:|------:|------:|
| CA      |     2022 |  2019 |  2025 | 72972 |
| CO      |     2024 |  2023 |  2025 |  2786 |
| CT      |     2023 |  2022 |  2025 |  2409 |
| DE      |     2024 |  2024 |  2025 |   132 |
| IL      |     2022 |  2018 |  2025 | 14513 |
| MD      |     2023 |  2022 |  2025 |  3556 |
| ME      |     2024 |  2024 |  2025 |   143 |
| NJ      |     2024 |  2024 |  2025 |   603 |
| OR      |     2021 |  2017 |  2025 |  7313 |
| VA      |     2024 |  2023 |  2025 |  2150 |

## 4. Employer contribution patterns (subset)

Schedule H/I employer contribution data is available for only **3,649 firms (3.4% of the full dataset)**. The match rate is low because (a) Schedule H is filed only by 100+ participant plans, and (b) Schedule I was discontinued for plan years 2023+. Most firms in this dataset are too small to file Schedule H and too recent to have a Schedule I filing on record.

Among firms with contribution data:

| metric                    |     value |
|:--------------------------|----------:|
| n_firms_with_contrib_data |   3649    |
| pct_of_full_dataset       |      3.42 |
| n_zero_contrib            |   2268    |
| pct_zero_contrib          |     62.15 |
| median_total_contrib      |      0    |
| mean_total_contrib        | 116240    |
| p75_total_contrib         |  10964    |
| p95_total_contrib         | 244046    |
| median_per_employee       |      0    |
| mean_per_employee         |   4429.78 |

**62% of firms with contribution data report zero employer contribution.** This includes both (a) plans where the employer chose a non-matching design and (b) plans where the employer simply hadn't yet contributed in the reported year. The median contribution is **$0**; the 75th percentile is **$10,964**.

By state:

| STATE   |    n |   median |     mean |   pct_zero |
|:--------|-----:|---------:|---------:|-----------:|
| CA      | 2123 |        0 |  67241.1 |      63.07 |
| CO      |  129 |        0 |  34504.6 |      75.97 |
| CT      |   74 |        0 |  55675   |      70.27 |
| DE      |    2 |     5885 |   5885   |      50    |
| IL      |  794 |        0 | 321848   |      55.79 |
| MD      |   83 |        0 |  19890.9 |      77.11 |
| ME      |    4 |        0 |      0   |     100    |
| NJ      |   14 |        0 |  15434.5 |      78.57 |
| OR      |  350 |        0 |  41616.1 |      55.43 |
| VA      |   76 |        0 |  11127   |      81.58 |

By size bucket:

| size_bucket   |    n |   median |     mean |   pct_zero |
|:--------------|-----:|---------:|---------:|-----------:|
| solo          | 1244 |      0   |  57287.1 |      85.45 |
| micro         |  745 |      0   |  27098.8 |      54.5  |
| small         |  504 |  11073.5 | 297225   |      34.72 |
| medium        |  737 |      0   | 120646   |      53.19 |
| large         |  415 |      0   | 226325   |      55.18 |
| unknown       |    4 |      0   |  16324   |      75    |

The contribution pattern is highly skewed: large firms with contribution data report substantially higher mean contributions than small firms, but the *median* is near zero across most size buckets. The high mean / low median pattern reflects a small number of very large contributors driving the average — useful to know when interpreting any per-employee contribution figure for these mandate-induced plans.

---

## Caveats

1. **EMPLOYEE_COUNT is "covered participants" not "headcount."** Form 5500's TOT_PARTCP_BOY_CNT counts plan participants, not all employees. A firm with 50 employees but only 30 plan participants would be coded "small" (10-49) here even though it has medium headcount. This affects bucket boundaries but not the qualitative picture.

2. **Some plans have effective dates after their filing year.** A 2024 Form 5500-SF can report a plan effective in 2025-08; the dataset includes these. They appear in `start_year=2025` in Table 3.

3. **Solo plans dominate.** ~62% of the dataset is solo or micro (0-9 participants). Any ATT-style claim about "401(k) plan formation" needs to disclose this composition. The DiD robustness check restricting to plans with positive employee count drops the ATT from 2.37 to 1.82 (analysis/did_results.md), and that's the version that makes a sharper claim about employer-employee retirement coverage.

4. **Contribution data is non-representative.** The 3.4% of firms with EMPLOYER_CONTRIBUTION populated are systematically larger and older than the dataset as a whole. Any cross-state contribution comparison must caveat this.

## Files

- `analysis/tables/size_distribution_overall.csv`
- `analysis/tables/state_by_size.csv`
- `analysis/tables/state_by_size_pct.csv`
- `analysis/tables/plan_start_year_by_state.csv`
- `analysis/tables/plan_start_year_summary.csv`
- `analysis/tables/contribution_summary.csv`
- `analysis/tables/contribution_by_state.csv`
- `analysis/tables/contribution_by_size.csv`
- `analysis/tables/pct_solo_by_state.csv`
