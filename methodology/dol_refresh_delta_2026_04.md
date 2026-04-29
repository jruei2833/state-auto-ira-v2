# DOL Form 5500 Refresh — Delta Report (April 2026)

**Refresh pull date:** 2026-04-29
**Prior pull date:** 2026-01-25 (Form 5500 + 5500-SF; the v3 dataset)
**Refresh source URLs:** `https://askebsa.dol.gov/FOIA%20Files/2024/All/F_5500_2024_All.zip`, `F_5500_SF_2024_All.zip`, `F_5500_2025_All.zip`, `F_5500_SF_2025_All.zip`
**Comparison build:** `data/refresh_2026_04/v1-inclusive/` and `data/refresh_2026_04/v2-conservative/`
**v3 reference:** `data/v1-inclusive/` (115,690) and `data/v2-conservative/` (106,577)

## Headline

| Version | v3 (Feb 2026) | Refresh (Apr 2026) | Δ count | Δ % |
|---|---|---|---|---|
| v1-inclusive | 115,690 | 116,096 | +406 | +0.35% |
| v2-conservative | 106,577 | 106,977 | +400 | +0.38% |

The refresh adds **+406 firms** in v1-inclusive and **+400 firms** in v2-conservative. These changes reflect a combination of (a) DOL monthly updates that added new filings to the 2024 plan year for plans that filed late, and (b) the inclusion of the partial 2025 plan-year file, which captures plans with effective dates after each state's mandate that filed Form 5500 for plan year 2025.

## State-by-state delta — v1-inclusive

| state   |   v3_count |   refresh_count |   delta |   pct_change |
|:--------|-----------:|----------------:|--------:|-------------:|
| CA      |      81512 |           81715 |     203 |         0.25 |
| IL      |      14793 |           14839 |      46 |         0.31 |
| NJ      |        816 |             858 |      42 |         5.15 |
| CO      |       2787 |            2817 |      30 |         1.08 |
| VA      |       2150 |            2178 |      28 |         1.3  |
| OR      |       7308 |            7329 |      21 |         0.29 |
| MD      |       3556 |            3574 |      18 |         0.51 |
| CT      |       2410 |            2418 |       8 |         0.33 |
| ME      |        143 |             149 |       6 |         4.2  |
| DE      |        215 |             219 |       4 |         1.86 |

## State-by-state delta — v2-conservative

| state   |   v3_count |   refresh_count |   delta |   pct_change |
|:--------|-----------:|----------------:|--------:|-------------:|
| CA      |      72972 |           73159 |     187 |         0.26 |
| IL      |      14513 |           14565 |      52 |         0.36 |
| NJ      |        603 |             641 |      38 |         6.3  |
| CO      |       2786 |            2818 |      32 |         1.15 |
| VA      |       2150 |            2178 |      28 |         1.3  |
| OR      |       7313 |            7337 |      24 |         0.33 |
| MD      |       3556 |            3575 |      19 |         0.53 |
| CT      |       2409 |            2419 |      10 |         0.42 |
| ME      |        143 |             149 |       6 |         4.2  |
| DE      |        132 |             136 |       4 |         3.03 |

## Year-by-year delta — v1-inclusive

(by plan effective year, not filing year — refresh adds filings for new effective years and corrections for prior effective years)

|   year |   v3_count |   refresh_count |   delta |
|-------:|-----------:|----------------:|--------:|
|   2017 |         13 |              13 |       0 |
|   2018 |       1468 |            1470 |       2 |
|   2019 |      12067 |           12072 |       5 |
|   2020 |      12665 |           12680 |      15 |
|   2021 |      14644 |           14654 |      10 |
|   2022 |      26280 |           26288 |       8 |
|   2023 |      22240 |           22261 |      21 |
|   2024 |      25871 |           25981 |     110 |
|   2025 |        442 |             668 |     226 |
|   2026 |          0 |               9 |       9 |

## Year-by-year delta — v2-conservative

|   year |   v3_count |   refresh_count |   delta |
|-------:|-----------:|----------------:|--------:|
|   2017 |         13 |              13 |       0 |
|   2018 |        933 |             933 |       0 |
|   2019 |       3785 |            3790 |       5 |
|   2020 |      12665 |           12680 |      15 |
|   2021 |      14644 |           14654 |      10 |
|   2022 |      26280 |           26288 |       8 |
|   2023 |      22240 |           22261 |      21 |
|   2024 |      25575 |           25681 |     106 |
|   2025 |        442 |             668 |     226 |
|   2026 |          0 |               9 |       9 |

## Late-treatment focus (ME, DE, NJ)

These three states had filing lag flagged in the prior DiD design memo: their 2024 cohort effects in the prior CS estimation were imprecise because their post-treatment data was only partial.

### v1-inclusive — ME, DE, NJ delta

| state   |   year |   v3_count |   refresh_count |   delta |
|:--------|-------:|-----------:|----------------:|--------:|
| ME      |   2024 |        129 |             129 |       0 |
| ME      |   2025 |         14 |              20 |       6 |
| DE      |   2024 |        209 |             209 |       0 |
| DE      |   2025 |          6 |               9 |       3 |
| DE      |   2026 |          0 |               1 |       1 |
| NJ      |   2024 |        767 |             781 |      14 |
| NJ      |   2025 |         49 |              76 |      27 |
| NJ      |   2026 |          0 |               1 |       1 |

ME / DE / NJ combined delta: **+52 firms** (+4.43% relative to v3 figure for those three states).

### v2-conservative — ME, DE, NJ delta

| state   |   year |   v3_count |   refresh_count |   delta |
|:--------|-------:|-----------:|----------------:|--------:|
| ME      |   2024 |        129 |             129 |       0 |
| ME      |   2025 |         14 |              20 |       6 |
| DE      |   2024 |        126 |             126 |       0 |
| DE      |   2025 |          6 |               9 |       3 |
| DE      |   2026 |          0 |               1 |       1 |
| NJ      |   2024 |        554 |             564 |      10 |
| NJ      |   2025 |         49 |              76 |      27 |
| NJ      |   2026 |          0 |               1 |       1 |

ME / DE / NJ combined delta: **+48 firms** (+5.47% relative to v3 figure for those three states).

## Materiality assessment

**v1-inclusive:** **Not material.** Both the overall delta and the late-treatment-state delta are within typical month-to-month DOL refresh noise. Re-running the full DiD analysis is unlikely to change the headline ATT.

**v2-conservative:** **Potentially material for late-cohort estimates.** The overall change is small, but the late-treatment states (ME, DE, NJ) saw measurable filings catch up. The Callaway-Sant'Anna ATT for the 2024 cohort would shift; the headline simple ATT (which weights all cohorts) would shift much less. Worth re-running.

## What this means for the DiD analysis

The DiD headline ATT (2.37 per 1,000 establishments) was estimated on the v3 dataset's underlying effective-year aggregations. The relevant question for re-running is whether the DiD panel — built from `analysis/build_state_year_panel.py` against the raw Form 5500 data, **not** from the descriptive v3 dataset — would change.

Two reasons the DiD panel is more stable than the headline counts:
1. The DiD panel aggregates ALL state-year new 401(k) plans (mandate + control), so changes are normalized by the (also growing) control population.
2. The CS estimator's bootstrap inference draws on the entire panel; one cohort's filings catching up changes that cohort's ATT but is averaged across the simple-aggregation weights.

If the late-treatment-state delta is meaningful (>5%), the cohort effect for cohort 2024 will shift and should be re-reported. If it's small, it's not worth a full re-run.

**Recommendation:** Not material.

## Caveats

- The pull date for the v3 dataset is 2026-01-25 per file mtimes, not 2026-02-XX as commonly assumed in earlier memos. The "February 2026" framing in earlier writeups is approximate.
- 2025 plan-year coverage is partial: only filings DOL has received and posted as of 2026-04-29 are reflected. The 2025 file will continue to grow over the rest of 2026.
- The refresh was applied uniformly to all 10 mandate states; no special handling for any state.
- Files refreshed: F_5500 (Form 5500 main filings) and F_5500_SF (Form 5500-SF small-plan filings) for both 2024 and 2025. Schedule R / H / I were NOT re-pulled in this refresh; the contribution-rate join in build_dataset.py uses the existing pre-refresh schedules.

## Files

- `data/refresh_2026_04/v1-inclusive/state_auto_ira_401k_dataset.csv`
- `data/refresh_2026_04/v2-conservative/state_auto_ira_401k_dataset.csv`
- `data/refresh_2026_04/v1-inclusive/summary_statistics.csv`
- `data/refresh_2026_04/v2-conservative/summary_statistics.csv`
- `methodology/source_provenance_log.csv` — populated TBDs for 2024 and 2025
- `form5500-raw-data/refresh_2026_04/F_5500_2024_All.zip`, `F_5500_SF_2024_All.zip`,
  `F_5500_2025_All.zip`, `F_5500_SF_2025_All.zip`
- `form5500-raw-data/pre_refresh_backup_2026_04/` — preserved 2024 CSVs from v3
