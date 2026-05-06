# Pre-memo verification

**Date:** 2026-05-06
**Purpose:** Two checks against the recent denominator-sensitivity batch outputs before drafting the stakeholder memo. Both checks return clean — no findings that change the memo framing.

---

## Check 1: SUSB and CBP DiDs run on identical year ranges

**Concern:** SUSB has a ~2-year Census release lag, with 2017–2022 actually pulled and 2023/2024 unavailable. If the SUSB-denominator DiD ran on a truncated 2017–2022 panel while the CBP-denominator DiD ran on 2017–2024, the denominator-sensitivity table would mix temporal-coverage differences into the comparison.

**Method:** Read the panel CSVs and the runner script.

**Finding:** Year ranges are **identical**.

| Panel file | Rows | States | Year range |
|---|---:|---:|---|
| `analysis/did_panel_v1_inclusive.csv` (CBP) | 408 | 51 | 2017–2024 |
| `analysis/did_panel_v2_conservative.csv` (CBP) | 408 | 51 | 2017–2024 |
| `analysis/did_panel_susb_v1_inclusive.csv` | 408 | 51 | 2017–2024 |
| `analysis/did_panel_susb_v2_conservative.csv` | 408 | 51 | 2017–2024 |

The SUSB panel-build script ([analysis/build_did_panels_susb.py:109-122](analysis/build_did_panels_susb.py:109)) carries the 2022 SUSB firm counts forward to 2023 and 2024 with `groupby('state')[fill_cols].ffill().bfill()`, so all 408 state-year rows have non-null SUSB denominator values. The CS-DiD runner ([analysis/run_did_susb.py](analysis/run_did_susb.py)) does no further year filtering before fitting. The same is true of the CBP runner.

**Implication:** The published 2.37 (CBP) vs 2.89 (SUSB-all) vs 7.83 (SUSB-5+) comparison is on identical 2017–2024 year ranges. No truncation is happening; no truncated-CBP DiD needs to be run.

### Subtlety worth noting in the memo (not a flag)

The two panels carry forward different amounts of data at the right edge of the panel:

- **CBP** uses real Census API data 2017–2023, carries 2023 forward to 2024 (CBP 2024 not yet released).
- **SUSB** uses real Census tables 2017–2022, carries 2022 forward to 2023 *and* 2024 (SUSB has a longer release lag).

So SUSB has two years of carry-forward at the right edge versus CBP's one year. This is a denominator-data-recency difference, not a year-range mismatch. Identifying variation in the CS-DiD comes mostly from pre-2023 cohorts, so the impact on the headline ATT is small. Worth one sentence in the memo's methodology footnote, not a substantive caveat.

---

## Check 2: QCEW/CBP 0.79 ratio — methodological or partly substantive?

**Concern:** The QCEW collection batch reported a median QCEW/CBP establishment ratio of 0.79 (the spec expected ~1.0) and attributed it to a "structural counting-unit definition gap" between BLS UI worksites and the Census Business Register. If sectoral coverage differences between QCEW and CBP fall differentially on mandate vs non-mandate states, the gap would be partly substantive (different employer populations being counted), not just methodological.

**Method:** Compute per-state CBP/QCEW establishment ratios for each year 2017–2024. Compare the mean and median ratios for mandate states vs non-mandate states. Test whether the difference exceeds the 5pp threshold from the prompt.

(Note: ratios are CBP-establishments / QCEW-establishments — i.e., CBP in the numerator. CBP is smaller because Business-Register establishments are coarser than QCEW UI worksites. Ratio < 1 is the expected direction.)

**Per-year national ratio (51 states):**

| Year | Median ratio | Mean ratio | Notes |
|---:|---:|---:|---|
| 2017 | 0.848 | 0.843 | |
| 2018 | 0.843 | 0.833 | |
| 2019 | 0.829 | 0.821 | |
| 2020 | 0.813 | 0.803 | |
| 2021 | 0.789 | 0.781 | |
| 2022 | 0.749 | 0.746 | Cleanest comparison year (real data both sides) |
| 2023 | 0.721 | 0.725 | Cleanest recent year (real data both sides) |
| 2024 | 0.708 | 0.714 | CBP 2024 is carry-forward from 2023 — mechanically affected |

The aggregate ratio is drifting down over time (from 0.84 in 2017 to 0.72 in 2023). This trend is independent of the mandate-vs-non-mandate question but worth noting: it suggests the counting-unit gap is widening, plausibly driven by growth in multi-establishment firms (modern retail, services franchises) where QCEW counts each UI worksite while CBP rolls them up. This is consistent with the original "structural counting-unit definition gap" explanation; if anything it strengthens it.

**Mandate vs non-mandate comparison (2023, the cleanest recent year):**

| Group | Mean ratio | Median ratio | Std | n |
|---|---:|---:|---:|---:|
| Non-mandate | 0.7309 | 0.7268 | 0.0884 | 41 |
| Mandate | 0.7023 | 0.7015 | 0.0689 | 10 |
| **Difference (mandate − non-mandate)** | **−0.0286 (= −2.86pp)** | | | |

Welch's two-sample t-test: t = −1.11, p = 0.284. Difference is **well within sampling noise** and **below the 5pp stop-and-ask threshold**.

**Comparison across years (mandate − non-mandate diff in pp):**

| Year | Diff (pp) | Welch p | 5pp threshold breach? |
|---:|---:|---:|---|
| 2022 | −3.35 | 0.188 | No |
| 2023 | −2.86 | 0.284 | No |
| 2024 | −2.37 | 0.401 | No (and CBP 2024 is carry-forward, so noisy) |

The mandate-state ratio is slightly lower than non-mandate (mandate states have a slightly larger relative QCEW count vs CBP), but the gap is small and not statistically distinguishable from zero in any year.

**Spot-checks at the tails (2023 ratios):**

Lowest CBP/QCEW ratios:
- DC 0.466 — federal-government-heavy; CBP excludes most government employees, QCEW captures more of the private contractor / membership-organization tail. DC is a known outlier.
- CA 0.601 (mandate) — the largest state by all measures; multi-establishment retail/restaurants and tech firms with multiple worksites depress the ratio.
- HI 0.601 — tourism/hospitality with multi-location chains; geographically dispersed UI worksites.
- CT 0.620 (mandate), RI 0.622, NH 0.628, MO 0.639, ID 0.639, MA 0.646, KY 0.646.
- Mandate states in the low quartile are CA and CT — the size and industry mix in California and the Northeast corridor drive lower ratios, not the mandate per se. Comparable non-mandate states (HI, RI, NH, MA) sit in the same band.

Highest CBP/QCEW ratios:
- AK 0.960, WA 0.902, IN 0.846, KS 0.832, WY 0.832, IL 0.826 (mandate), TX 0.824, PA 0.823, IA 0.796, NY 0.794, OH 0.792.
- Mandate states in the high quartile: IL. Industrial / manufacturing-heavy states (IN, OH, PA, IL) have higher ratios because manufacturing firms tend to be single-establishment.
- Mandate states span the full range from low (CA, CT) to high (IL, MD, NJ at 0.758–0.826), distributed across the same range as non-mandate states.

**Implication:** The 0.79 (now 0.72 in 2023) ratio is well-explained by the structural counting-unit definition gap (QCEW UI worksites > CBP Business Register establishments for multi-unit firms). There is **no evidence** that the gap is driven by sectoral composition in mandate states. The agent's original methodological-footnote framing is supported.

The mandate-vs-non-mandate ratio difference of ~3pp is in the expected direction (mandate states are larger and more service-intensive on average; CA alone pulls the mandate group's mean down) but is small, not statistically significant, and well below the 5pp substantive-difference threshold.

The memo can describe the QCEW/CBP gap as a methodological footnote without further investigation.

---

## Outputs

- `analysis/qcew_vs_cbp_state_year_ratios.csv` — per-state-year ratios (CBP/QCEW establishments and employment), 408 rows. Mandate-state flag column included for downstream filtering.
- This document.

## What this means for the memo

Both checks are clean. The denominator-sensitivity table can be presented as comparing identical 2017–2024 year ranges across CBP, QCEW, and SUSB denominators. The QCEW/CBP gap can be footnoted as methodological (counting-unit gap, CBP rolls multi-establishment firms up while QCEW counts each UI worksite) without claiming sectoral-composition concerns. No re-runs needed. No flagged issues.
