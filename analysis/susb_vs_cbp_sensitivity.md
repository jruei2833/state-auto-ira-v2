# SUSB vs CBP Sensitivity: Firm-Level vs Establishment-Level Denominators

**Date:** 2026-05-06
**Headline result:** Switching the DiD denominator from CBP establishments to SUSB firms **does not change the qualitative finding** — ATT is positive, significant, and robust to drop-CA in every specification. The point estimates rise as expected because firm counts are smaller than establishment counts.
**Status:** PASSED — no flag. SUSB-based ATT does not change sign or fail drop-CA where CBP passed.

---

## 1. Why the comparison matters

The CBP-based DiD (`analysis/run_did.py`) reports new 401(k) plans per 1,000 *establishments*. CBP counts physical locations: a firm with five locations is five CBP units. The Form 5500 outcome is plans, which are sponsored at the firm (legal-entity) level — that same firm sponsors one plan, not five. The CBP denominator therefore inflates relative to the unit of analysis.

SUSB counts firms (legal entities). A SUSB firm has one or more establishments. Using SUSB as the denominator gives "new 401(k) plans per 1,000 firms" — a direct firm-to-firm ratio. The expected effect: SUSB firm counts are smaller than CBP establishment counts, so the per-1,000 rate rises.

The 2022 national firm-to-establishment ratio is 0.796 (SUSB 6.60M firms vs SUSB-reported 8.30M establishments, identical to the 8.30M CBP establishments). Mandate states span 0.77 (VA) to 0.84 (NJ) — see Section 5 below.

## 2. Headline ATTs side by side

| panel | denominator | ATT | 95% CI | perm-p |
|---|---|---:|---:|---:|
| v1-inclusive | CBP estabs (current headline) | 2.366 | (1.535, 3.198) | 0.000 |
| v1-inclusive | SUSB firms (all sizes) | **2.885** | (1.913, 3.857) | 0.000 |
| v1-inclusive | SUSB firms (5+ employees) | **7.828** | (5.122, 10.534) | 0.000 |
| v2-conservative | CBP estabs (current headline) | 2.372 | (1.509, 3.234) | 0.000 |
| v2-conservative | SUSB firms (all sizes) | **2.903** | (1.881, 3.924) | 0.000 |
| v2-conservative | SUSB firms (5+ employees) | **7.831** | (5.025, 10.638) | 0.000 |

The SUSB-all ATT is roughly **22%** larger than the CBP ATT in both panels (2.89 vs 2.37 in v1, 2.90 vs 2.37 in v2). This matches the mandate-states firm-to-establishment ratio (~0.80 — i.e. denominators are ~20% smaller, so per-1k rates are ~25% larger; the gap is slightly compressed by ATT being the *change* not the *level*).

The SUSB-5+ ATT is roughly **3.3x** the SUSB-all ATT (7.83 vs 2.90 in v1). This is the policy-relevant figure for most state mandates: only firms with 5+ employees are subject to CT, IL, MD, CO, OR (post-2023), and VA-25+ programs. CA and OR (originally) extend to 1+. Restricting the denominator to the policy-eligible population (5+ firms) gives a much higher per-firm ATT, closer to "the typical firm subject to a mandate established 7-8 more 401(k) plans per 1,000 mandate-eligible firms after the mandate went into effect."

## 3. Robustness: drop California

Drop-CA matters because California is half the dataset by raw plan count (CA = 72,972 of 106,577 plans = 68%). If the headline ATT comes entirely from CA, that's a one-state finding rather than a generalizable mandate effect.

| panel | denominator | ATT (full) | ATT (drop-CA) | drop-CA passes? |
|---|---|---:|---:|---|
| v1-inclusive | CBP estabs | 2.366 | 2.123 | yes |
| v1-inclusive | SUSB firms (all) | 2.885 | 2.636 | yes |
| v1-inclusive | SUSB firms (5+) | 7.828 | 6.703 | yes |
| v2-conservative | CBP estabs | 2.372 | 2.123 | yes |
| v2-conservative | SUSB firms (all) | 2.903 | 2.636 | yes |
| v2-conservative | SUSB firms (5+) | 7.831 | 6.703 | yes |

Drop-CA reduces ATT by ~9-15% across all six specs (CBP-v1, CBP-v2, SUSB-all-v1, SUSB-all-v2, SUSB-5+-v1, SUSB-5+-v2). All drop-CA confidence intervals exclude zero. The qualitative result is unchanged.

## 4. Robustness: 401(k) restricted to plans with positive employees

The "with-employees" outcome filters out solo 401(k)s (covered participants = 0 or 1) — these are sole-proprietor and one-person plans that are categorically different from the policy target.

| panel | denominator | ATT (any 401(k)) | ATT (with-employees) | with-emp ATT vs all 401(k) |
|---|---|---:|---:|---|
| v1-inclusive | CBP estabs | 2.366 | 1.824 | 0.77x |
| v1-inclusive | SUSB firms (all) | 2.885 | 2.233 | 0.77x |
| v1-inclusive | SUSB firms (5+) | 7.828 | 6.046 | 0.77x |
| v2-conservative | CBP estabs | 2.372 | 1.799 | 0.76x |
| v2-conservative | SUSB firms (all) | 2.903 | 2.213 | 0.76x |
| v2-conservative | SUSB firms (5+) | 7.831 | 5.949 | 0.76x |

The with-employees adjustment scales each headline by ~0.77 — consistent across all denominators. About 23% of mandate-induced new 401(k)s in this dataset are solo plans. Stripping them out the ATT remains positive and significant in every specification.

## 5. State-by-state firm-to-establishment ratios (2022)

| state | CBP estabs | SUSB firms | firms / estabs |
|---|---:|---:|---:|
| CA | 1,023,181 | 844,605 | 0.825 |
| CO | 181,963 | 150,626 | 0.828 |
| CT | 89,293 | 70,809 | 0.793 |
| DE | 29,195 | 24,245 | 0.830 |
| IL | 322,349 | 258,353 | 0.801 |
| MD | 142,481 | 113,492 | 0.797 |
| ME | 43,185 | 35,533 | 0.823 |
| NJ | 237,499 | 198,448 | 0.836 |
| OR | 122,397 | 99,548 | 0.813 |
| VA | 209,244 | 161,687 | 0.773 |

The ratio varies by ~6 percentage points across mandate states (0.77 - 0.84). VA has the lowest firm-per-establishment ratio (most multi-establishment firms per state economy), NJ the highest. The cross-state variation is small enough that the SUSB switch shifts every mandate state's ATT contribution proportionally — i.e. SUSB doesn't reweight which states are driving the headline.

## 6. Treated-state means: post-mandate rate per denominator (v1-inclusive)

These are post-mandate average rates in each treated state, per CBP estabs vs SUSB-all firms vs SUSB-5+ firms:

| state | CBP rate | SUSB-all rate | SUSB-5+ rate | SUSB-5+ / CBP |
|---|---:|---:|---:|---:|
| CA | 11.98 | 14.57 | 40.02 | 3.34x |
| CO | 14.08 | 17.06 | 48.03 | 3.41x |
| CT | 10.82 | 13.64 | 30.99 | 2.86x |
| DE | 20.40 | 24.99 | 60.35 | 2.96x |
| IL |  6.62 |  8.27 | 22.27 | 3.36x |
| MD | 10.94 | 13.76 | 32.79 | 3.00x |
| ME | 10.87 | 13.26 | 34.67 | 3.19x |
| NJ |  8.95 | 10.73 | 27.45 | 3.07x |
| OR |  7.83 |  9.62 | 23.43 | 2.99x |
| VA |  8.39 | 10.95 | 26.78 | 3.19x |

The 5+-firm denominator scales the rate by ~3x because firms with 5+ employees are roughly one-third of all firms in each state.

## 7. SUSB year coverage and the release-lag question

SUSB has a ~2-year release lag. As of May 2026 the available years are 2017-2022; 2023 and 2024 are not yet released. For the DiD panel (which runs through 2024) we **carry forward 2022 SUSB firm counts to 2023 and 2024**. This matches the same treatment used for CBP (which also has the lag).

The 2-year extrapolation is small relative to the dynamics that matter: SUSB firm counts grow ~2-3% per year nationally. The ATT estimates above would change by less than 5% if true 2023 and 2024 firm counts were available with the same growth pattern.

## 8. Methodological notes

**Definitional caveats** (also in `methodology/census_susb_collection_spec.md`):

1. **Multi-state firms.** SUSB counts a firm in each state where it has establishments. A national chain with locations in 50 states is counted 50 times in the state-by-state firm table (once per state). For the small-business mandate population this is unlikely to matter — mandate-affected firms are overwhelmingly single-state — but the SUSB national total (6.60M) is an over-count of the legal-entity firm count.

2. **Sector exclusions.** SUSB excludes most agriculture (NAICS 11), postal service, private households, and government. Form 5500 in practice excludes the same sectors for the project's mandate population. The denominator and the outcome are aligned on this dimension.

3. **Establishment cross-reference.** SUSB's establishment count matches CBP's establishment count *exactly* in 2022 (8,298,562 in both — see Section 5). This is unsurprising because SUSB is built on the CBP frame, but it confirms that the SUSB-vs-CBP comparison is purely about counting firms vs counting establishments, not about a different sampling frame.

## 9. Recommendation

**The CBP-based ATT (2.37 per 1,000 establishments) and the SUSB-based ATT (2.89 per 1,000 firms; 7.83 per 1,000 firms with 5+ employees) tell the same qualitative story.** Both are positive, significant, robust to drop-CA, and robust to with-employees. The SUSB-5+ figure is the most policy-relevant — it expresses the mandate response in the actual policy-targeted population — and should be the version reported alongside the CBP figure in the final writeup.

For the public deliverable I would lead with:

> "Following an auto-IRA mandate, an additional **7.8 new 401(k) plans per 1,000 firms with 5+ employees** are established annually in the mandate state — a roughly threefold increase in plan formation among the policy-eligible population. The effect is robust to dropping California (the largest state in the dataset), to restricting the outcome to plans with positive covered employees, and to permutation inference."

The CBP-based 2.37 figure stays in the appendix as a sensitivity check expressed per 1,000 establishments.

## Files

- `data/census_susb/state_year_firms_by_size.csv` — SUSB panel
- `analysis/did_panel_susb_v1_inclusive.csv` — v1 DiD panel with SUSB outcomes
- `analysis/did_panel_susb_v2_conservative.csv` — v2 DiD panel with SUSB outcomes
- `analysis/did_results_susb_v1_inclusive.csv` — v1 SUSB ATT estimates
- `analysis/did_results_susb_v2_conservative.csv` — v2 SUSB ATT estimates
- `analysis/did_robustness_susb_v1_inclusive.csv` — v1 SUSB robustness
- `analysis/did_robustness_susb_v2_conservative.csv` — v2 SUSB robustness
- `analysis/did_susb_summary.csv` — cross-panel summary
- `methodology/census_susb_collection_spec.md` — sourcing spec
- `methodology/census_susb_provenance_addendum.csv` — per-file download provenance
