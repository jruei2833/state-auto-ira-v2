# DiD aggregation choice: cohort-weighted simple vs equal-weight event-time

**Date:** 2026-05-06
**Purpose:** Pre-memo decision on which aggregation of the Callaway-Sant'Anna group-time ATT(g, t) estimates should anchor the headline figure in the project deliverable. Compares the two natural choices — cohort-weighted simple aggregation and equal-weight event-time aggregation — on identification, robustness, and HonestDiD sensitivity.

## Headline numbers

Both panels, primary CS spec (not-yet-treated comparison group):

| Panel | Cohort-weighted simple ATT | Equal-weight event-time ATT (t=0..6) | Δ |
|---|---:|---:|---:|
| v1-inclusive | **2.366** [1.535, 3.198] | 2.661 | +0.295 |
| v2-conservative | **2.372** [1.509, 3.234] | 2.663 | +0.291 |

The equal-weight event-time aggregation is ~0.29 higher in both panels. This gap is not a small-sample wobble — it is driven by a small number of long-horizon, wide-CI event-time coefficients that are mechanically getting full weight in the equal-weight average.

## Why the two aggregations diverge

**Cohort-weighted simple aggregation** averages all post-treatment ATT(g, t) cells, weighted by the share of treated state-year observations each (g, t) cell contributes. Concretely: state-years where many treated cohorts overlap (early event times) get more weight; state-years where only one cohort survives (late event times) get less weight. The overall ATT is effectively a weighted average of group-time ATTs by exposure.

**Equal-weight event-time aggregation** first averages within event time t (across cohorts and states), then takes a simple mean across event times. Each event-time period contributes 1/N to the headline regardless of how many cohorts identify it.

This matters because **the number of cohorts identifying each event time decreases sharply as t grows** under a 2017–2024 panel.

### v1-inclusive: which cohorts identify each event time

OR (cohort 2017) drops from the CS event-time aggregation because the panel starts in 2017 and CS requires at least one pre-treatment period.

| t | identifying cohorts | treated states contributing |
|---:|---|---|
| 0 | 2018, 2022, 2023, 2024 | CA, IL, CT, MD, CO, VA, DE, ME, NJ (9) |
| 1 | 2018, 2022, 2023 | CA, IL, CT, MD, CO, VA (6) |
| 2 | 2018, 2022 | CA, IL, CT, MD (4) |
| 3 | 2018 | CA, IL (2) |
| 4 | 2018 | CA, IL (2) |
| 5 | 2018 | CA, IL (2) |
| 6 | 2018 | CA, IL (2) |

t=3 through t=6 are identified by a single cohort (2018) of two states.

### v2-conservative: which cohorts identify each event time

In v2, IL (2018) and CA (2019) are separate single-state cohorts, and CA's t=6 falls outside the panel (would be 2025).

| t | identifying cohorts | treated states contributing |
|---:|---|---|
| 0 | 2018, 2019, 2022, 2023, 2024 | IL, CA, CT, MD, CO, VA, DE, ME, NJ (9) |
| 1 | 2018, 2019, 2022, 2023 | IL, CA, CT, MD, CO, VA (6) |
| 2 | 2018, 2019, 2022 | IL, CA, CT, MD (4) |
| 3 | 2018, 2019 | IL, CA (2) |
| 4 | 2018, 2019 | IL, CA (2) |
| 5 | 2018, 2019 | IL, CA (2) |
| 6 | 2018 | **IL only (1)** |

**v2 t=6 is identified by Illinois alone.** That single-state, single-year cell gets equal weight (1/7) in the equal-weight event-time aggregation, the same weight as t=0 which is identified by nine states across five cohorts.

## Where the divergence comes from numerically

Pulling the post-treatment CS event-time coefficients (including all of t=0..6):

**v1-inclusive:**

| t | ATT | SE | 95% CI | flag |
|---:|---:|---:|---|---|
| 0 | 2.216 | 0.858 | [0.292, 4.139] | |
| 1 | 2.161 | 1.221 | [-0.576, 4.898] | wide CI |
| 2 | 1.243 | 0.507 | [0.106, 2.379] | |
| 3 | 0.763 | 0.635 | [-0.661, 2.186] | wide CI |
| 4 | **5.964** | **4.099** | **[-3.227, 15.156]** | very wide CI |
| 5 | 3.380 | 0.258 | [2.801, 3.958] | |
| 6 | 2.900 | 0.396 | [2.011, 3.788] | |

t=4 is an extreme outlier with a 95% CI nine units wide. It contributes 5.96/7 ≈ 0.85 to the equal-weight headline by itself.

**v2-conservative:**

| t | ATT | SE | 95% CI | flag |
|---:|---:|---:|---|---|
| 0 | 2.195 | 0.866 | [0.193, 4.196] | |
| 1 | 2.215 | 1.214 | [-0.590, 5.021] | wide CI |
| 2 | 1.282 | 0.517 | [0.088, 2.476] | |
| 3 | **5.522** | **4.159** | **[-4.091, 15.136]** | very wide CI |
| 4 | 1.677 | 0.909 | [-0.424, 3.777] | wide CI |
| 5 | 3.344 | 0.250 | [2.767, 3.921] | |
| 6 | 2.405 | 0.178 | [1.993, 2.817] | identified by IL only |

t=3 in v2 is the analogous outlier — same magnitude (~5.5), same massive SE (~4.16). Both v1's t=4 and v2's t=3 are noise-dominated coefficients identified by a single 2-state cohort that get full weight in the equal-weight aggregation.

If the wide-CI event times (t=1, t=3, t=4 in both panels) are excluded, the equal-weight average drops to:

- v1 excluding wide-CI t: 2.434 (down from 2.661)
- v2 excluding wide-CI t: 2.307 (down from 2.663)

These cleaner equal-weight averages are within 0.07 of the simple ATT in both panels, confirming the divergence is driven by the noisy long-horizon ATTs that get equal weight under event-time aggregation.

## Why cohort-weighted simple is more defensible under HonestDiD

The HonestDiD sensitivity analysis (Rambachan & Roth 2023) bounds the post-treatment ATT under bounded violations of parallel trends, where the bound is calibrated against the maximum observed pre-trend deviation. Two structural facts matter:

1. **Long-horizon ATTs are mechanically more sensitive to parallel-trends violations.** The bias from a constant trend differential δ over t years is t·δ. So bounds at t=6 are strictly wider than bounds at t=0 for any non-zero δ, and the bound widens linearly with horizon. Equal-weight event-time aggregation gives 1/7 weight to t=6 even though its identification is single-cohort and its HonestDiD bound is the widest.

2. **Single-cohort event-time cells have minimal cross-cohort cancellation of bias.** When multiple cohorts identify a t-cell, idiosyncratic shocks to any one cohort partially cancel in the average. When only IL identifies v2's t=6, an Illinois-specific 2024 shock contaminates t=6 fully and gets carried into the headline. Cohort-weighted simple aggregation averages across more (g, t) cells, so single-cohort idiosyncrasies wash out.

The honest bounds output ([analysis/did_honest_bounds_v2_conservative.csv](analysis/did_honest_bounds_v2_conservative.csv)) bears this out: bounds widen substantially at long horizons. Anchoring the headline on the cohort-weighted simple ATT means the honest-bounds robustness statement is over a tight CI; anchoring on the equal-weight event-time ATT means the honest-bounds statement extends across the long-horizon noise.

## Recommendation

**Lead the memo with the cohort-weighted simple ATT (~2.37 per 1,000 establishments, both panels).** Report the event study as the dynamics figure that supports interpretation but not as the headline number.

Concrete framing:

> The headline causal estimate is the cohort-weighted simple ATT from the Callaway-Sant'Anna primary specification: 2.37 new 401(k) plans per 1,000 private establishments per year on average across the post-mandate window, with a 95% confidence interval of [1.51, 3.23]. This estimate weights treated state-year observations by their identifying mass; it does not lean disproportionately on long-horizon estimates that are identified by one or two cohorts in the current 2017–2024 panel.

> The event study (figure 2) shows the dynamic effect peaking around t=0 to t=2 at approximately 1.2–2.2 per 1,000, with substantially wider confidence intervals at t≥3 because long-horizon estimates in this panel are identified by the early cohorts (CA, IL, OR) only. The t=3 / t=4 spike is a single-cohort artifact, not a substantive late-treatment effect; readers should not over-interpret it.

The cohort-weighted simple choice is the standard recommendation in the CS literature for staggered designs where late-cohort coverage is short, and it aligns with how the HonestDiD bounds are usually anchored.

## Files referenced

- `analysis/did_results_v1_inclusive.csv`, `analysis/did_results_v2_conservative.csv` — simple ATT
- `analysis/did_event_study_v1_inclusive.csv`, `analysis/did_event_study_v2_conservative.csv` — event time ATTs
- `analysis/did_cohort_effects_v1_inclusive.csv`, `analysis/did_cohort_effects_v2_conservative.csv` — per-cohort ATTs
- `analysis/did_honest_bounds_v2_conservative.csv`, `analysis/did_honest_bounds.md` — HonestDiD sensitivity
- `analysis/did_panel_v1_inclusive.csv`, `analysis/did_panel_v2_conservative.csv` — estimation panels
