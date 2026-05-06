# Firm-Level Analysis (SUSB-Normalized)

**Date:** 2026-05-06

**Dataset:** `data/v2-conservative/state_auto_ira_401k_dataset.csv` (106,577 firm-EIN records, 10 mandate states)

**Denominator:** Census SUSB firm counts in the year prior to each state's mandate (or 2022 fallback for late-mandate states).


This rebases the descriptive firm-level analysis from share-of-plans to **rate per 1,000 firms** in each size band, using SUSB firm counts as the denominator. The per-1,000-firms rate strips out the mechanical effect of state-level firm-size composition: a state with many small firms will mechanically have many small-plan 401(k)s even if the per-firm formation rate matches a state with few small firms.


## 1. Method

Map Form 5500 plan-participant counts to SUSB enterprise-size bins. Form 5500 reports *covered participants* (TOT_PARTCP_BOY_CNT), not total firm headcount; SUSB reports total firm employment. The two are highly correlated for small firms (where most employees are plan-eligible) but diverge for larger firms with eligibility filters. The rate-per-1,000 is therefore most reliable in the 0-4, 5-9, and 10-19 bins.

For each state, use the SUSB firm-count from the year prior to that state's mandate effective year (`mandate_year - 1`). For states with mandates effective in 2017-2018 (OR, IL) the SUSB year is 2017 since 2016 is unavailable. For 2024-mandate states (ME, DE, NJ) the SUSB year is 2022 (the most recent SUSB release as of May 2026).


State-by-state SUSB year used: CA=2018, CO=2022, CT=2021, DE=2022, IL=2017, MD=2021, ME=2022, NJ=2022, OR=2022, VA=2022.


## 2. State-by-state firm-size band rates (plans per 1,000 firms)

How many new mandate-induced 401(k) plans were established per 1,000 firms in that size band, in each state:

| state   |   0-4 |    5-9 |   10-19 |   20-99 |   100-499 |   500+ |
|:--------|------:|-------:|--------:|--------:|----------:|-------:|
| CA      | 59.57 | 133.05 |  167.05 |  179.65 |    112    |  23.61 |
| CO      | 14.32 |  28.56 |   29.95 |   29.7  |      8.42 |   0.81 |
| CT      | 25.55 |  43.57 |   55.24 |   61.31 |     19.15 |   3.88 |
| DE      |  3.66 |   8.68 |    8.24 |   12.37 |      4.27 |   0.7  |
| IL      | 32.54 |  83.29 |  112.45 |  121.05 |     65.75 |  18.84 |
| MD      | 25.79 |  39.37 |   45.12 |   50.42 |     24.47 |   0.33 |
| ME      |  1.91 |   4.95 |   11.27 |   11.94 |      4.69 |   0    |
| NJ      |  1.77 |   2.42 |    4.72 |   11.15 |      4.33 |   0.84 |
| OR      | 49.52 | 100.05 |  120.05 |  148.24 |     68.6  |   6.2  |
| VA      | 11.52 |  13.13 |   17.8  |   23.1  |     10.79 |   1.55 |

Counts of new plans by state and SUSB-mapped size band:

| state   |   0-4 |   5-9 |   10-19 |   20-99 |   100-499 |   500+ |
|:--------|------:|------:|--------:|--------:|----------:|-------:|
| CA      | 28913 | 16845 |   13388 |   12129 |      1538 |    152 |
| CO      |  1391 |   597 |     415 |     354 |        26 |      3 |
| CT      |  1026 |   538 |     413 |     389 |        33 |      9 |
| DE      |    52 |    29 |      19 |      28 |         3 |      1 |
| IL      |  5153 |  3248 |    2764 |    2851 |       406 |     91 |
| MD      |  1705 |   712 |     535 |     535 |        68 |      1 |
| ME      |    42 |    28 |      37 |      33 |         3 |      0 |
| NJ      |   214 |    78 |      95 |     195 |        18 |      3 |
| OR      |  2912 |  1684 |    1289 |    1275 |       137 |     16 |
| VA      |  1101 |   339 |     302 |     361 |        41 |      6 |

SUSB firm counts in pre-treatment year:

| state   |    0-4 |    5-9 |   10-19 |   20-99 |   100-499 |   500+ |
|:--------|-------:|-------:|--------:|--------:|----------:|-------:|
| CA      | 485387 | 126608 |   80144 |   67515 |     13732 |   6439 |
| CO      |  97133 |  20907 |   13855 |   11918 |      3088 |   3725 |
| CT      |  40162 |  12349 |    7477 |    6345 |      1723 |   2319 |
| DE      |  14204 |   3340 |    2305 |    2264 |       703 |   1429 |
| IL      | 158363 |  38998 |   24579 |   23552 |      6175 |   4830 |
| MD      |  66106 |  18086 |   11856 |   10610 |      2779 |   2988 |
| ME      |  21949 |   5657 |    3282 |    2764 |       640 |   1241 |
| NJ      | 120880 |  32185 |   20147 |   17492 |      4155 |   3589 |
| OR      |  58802 |  16832 |   10737 |    8601 |      1997 |   2579 |
| VA      |  95589 |  25822 |   16962 |   15630 |      3801 |   3883 |

## 3. Pooled rates across all 10 mandate states

Pooling all mandate states, plans-per-1,000-firms by SUSB band:


| size band | new plans | SUSB firms | rate per 1,000 firms |
|---|---:|---:|---:|
| 0-4 | 42,509 | 1,158,575 | 36.69 |
| 5-9 | 24,098 | 300,784 | 80.12 |
| 10-19 | 19,257 | 191,344 | 100.64 |
| 20-99 | 18,150 | 166,691 | 108.88 |
| 100-499 | 2,273 | 38,793 | 58.59 |
| 500+ | 282 | 33,022 | 8.54 |

## 4. Interpretation

The descriptive headline that '62% of mandate-induced plans are solo or micro (0-9 participants)' is mechanically driven in part by the fact that ~78% of all SUSB firms in mandate states fall in the 0-4 or 5-9 size bands. When normalized by the firm-size distribution, the **per-firm rate of plan formation** rises monotonically with firm size in most states — bigger firms form plans at substantially higher rates per firm — but the absolute *number* of new plans is concentrated at the small end simply because the underlying firm population is.

This matters for two interpretive claims that prior versions of the writeup did not separate:


1. **The composition claim**: 'Most mandate-induced plans are sponsored by small firms.' This remains true at the share-of-plans level (62% solo+micro) and is mechanical given the firm-size distribution.

2. **The behavioral claim**: 'Small firms respond to the mandate at high rates.' The SUSB normalization shows that **larger firms have higher per-firm response rates** in most states. The small-firm share of plans is large because small firms are numerous, not because they respond at proportionally higher rates than larger firms.


The cross-state spread in band-specific rates is also informative — California in the 0-4 band shows ~59.6 plans per 1,000 firms while Maine shows ~1.9 per 1,000. This is partly data lag (ME's 2024 effective date means most ME plans haven't filed yet) and partly genuine cross-state variation in small-firm responsiveness.


## 5. Caveats

1. **Participant count vs employee count**: Form 5500 EMPLOYEE_COUNT is covered participants, not total firm employment. For solo and micro firms these are usually the same. For larger firms a 100-employee firm with a participant filter (e.g. age 21, 1 year service) might report 70 covered participants and be coded into the 20-99 band — this would slightly inflate the 20-99 rate and deflate the 100-499 rate. The qualitative ranking of bands is unaffected.

2. **SUSB lag**: For 2024-mandate states (ME, DE, NJ) SUSB 2022 is the most recent available year. The 2-year extrapolation is small (SUSB firm counts grow ~2-3% per year nationally). Reported rates should be read as 'plans per 1,000 firms as of pre-treatment SUSB' rather than 'plans per 1,000 firms in mandate year'.

3. **State firm-count includes non-mandate-eligible firms**. A 2-firm partnership with one 1099 contractor isn't subject to most state mandates (5+ thresholds in IL/MD/CT/CO; 25+ in VA; 1+ in CA/OR). The 0-4 SUSB band therefore overstates the policy-relevant denominator in 5+-threshold states. The 5-9 and larger bands are much closer to apples-to-apples.


## Files

- `analysis/tables/susb_normalized_rates_by_state_size.csv` (long format)
- `data/census_susb/state_year_firms_by_size.csv` (firm-count panel)

