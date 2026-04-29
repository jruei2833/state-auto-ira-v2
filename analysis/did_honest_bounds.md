# Honest DiD Sensitivity Bounds

**Date:** 2026-04-29
**Reference:** Rambachan & Roth (2023), "A More Credible Approach to Parallel Trends," *Review of Economic Studies*
**Implementation:** R package `HonestDiD` 0.2.8
**Panel:** v2-conservative (`analysis/did_panel_v2_conservative.csv`)
**Estimator base:** Callaway-Sant'Anna ATT(g,t) → dynamic (event-time) aggregation; equal-weight average across event times 0–6 is the parameter being bounded.
**Output files:** `did_honest_bounds_v2_conservative.csv`, `did_honest_bounds_v2_conservative.png`, `did_honest_bounds.R`, `did_honest_bounds.log`

## Why this exists

The DiD design memo explicitly recommends Honest DiD bounds (Rambachan & Roth 2023) as a robustness check on the event-study estimates: "to bound how much the post-treatment estimates can change under plausible violations of parallel trends." This document reports those bounds for the v2-conservative event study.

The headline DiD result is robust ONLY if you believe the parallel-trends assumption holds exactly. Honest DiD asks: *how badly* could parallel trends be violated, and *how does the ATT change* under those violations? It produces a range of conclusions across a continuum of pre-trend-violation severities, indexed by a parameter (M for smoothness, Mbar for relative magnitudes).

## Result

| Restriction | Parameter | 95% lower bound | 95% upper bound | Width | Crosses zero? |
|---|---|---|---|---|---|
| **Original CS (unrestricted)** | — | 1.15 | 4.18 | 3.03 | no |
| Smoothness (DeltaSD) | M = 0 | -0.48 | 9.08 | 9.55 | yes (barely) |
| Smoothness (DeltaSD) | M = 0.5 | -6.03 | 14.62 | 20.65 | yes |
| Smoothness (DeltaSD) | M = 1 | -11.84 | 20.41 | 32.25 | yes |
| Smoothness (DeltaSD) | M = 2 | -23.73 | 32.34 | 56.07 | yes |
| **Relative magnitudes (DeltaRM)** | **Mbar = 0.5** | -0.70 | 5.86 | 6.56 | yes |
| **Relative magnitudes (DeltaRM)** | **Mbar = 1** | -3.32 | 8.49 | 11.81 | yes |
| Relative magnitudes (DeltaRM) | Mbar = 2 | -8.89 | 14.02 | 22.91 | yes |

Plot: `analysis/did_honest_bounds_v2_conservative.png`

## What the parameters mean

- **DeltaSD (smoothness restriction):** Allows the post-treatment differential trend to deviate from a linear extrapolation of the pre-trend by at most M per period. M = 0 means the post-treatment trend exactly continues the pre-trend; M > 0 progressively relaxes that. M is in the same units as the outcome (new 401(k) plans per 1,000 establishments).
- **DeltaRM (relative magnitudes restriction):** Allows the post-treatment differential trend to be at most Mbar × the largest pre-treatment differential. Mbar = 1 corresponds to the most-cited Rambachan-Roth recommendation: "post-treatment violations no larger than the largest pre-treatment violation." Mbar > 1 progressively relaxes.

The two restrictions answer the same kind of question with slightly different formal structure. DeltaRM is more interpretable for policy memos because it scales with the actual pre-trend variation in the data.

## Interpretation

**Under the unrestricted CS estimate, the average post-treatment ATT is 2.66 with 95% CI [1.15, 4.18] — significant.** The CI here is for the equal-weight average of the event-time effects t = 0, 1, 2, …, 6, which is a different parameter than the simple cohort-weighted ATT (2.37 with [1.51, 3.23]). The two diverge because the equal-weight average pulls in the noisy t = 4 estimate (5.96 with SE 4.0), inflating both the point estimate and the variance.

**The result is fragile to plausible parallel-trend violations.** Under even the *strictest* honest restriction (DeltaSD with M = 0, which is effectively "the post-treatment differential trend is exactly the linear continuation of the pre-trend"), the lower bound just barely crosses zero at -0.48. Under more permissive restrictions, the lower bound drops well below zero. The most policy-relevant restriction — DeltaRM with Mbar = 1 ("post-treatment violations no larger than the largest pre-treatment violation") — gives a CI of [-3.32, 8.49], which crosses zero comfortably.

**The fragility is driven primarily by the noisy late event-time estimates, not by violation of parallel trends in the data.** The CS event-study showed flat pre-trends (all six pre-period coefficients had CIs containing zero), so the *pre-trend evidence* is not problematic. The width comes from the equal-weight averaging including imprecise late-period coefficients (t = 4 in particular). The simple cohort-weighted ATT, which the DiD design memo recommends as the headline, weights cohorts more efficiently and would be expected to have tighter honest bounds; but HonestDiD is built around the event-study parameter, so we report those.

## Bottom line for the policy memo

Three defensible framings, ordered from strongest to weakest claim:

1. **(Strong)** "The DiD estimate is significant under the unrestricted CS bootstrap, [1.15, 4.18] for the average post-treatment effect." — true but ignores the honest-DiD critique.

2. **(Moderate)** "Under the strictest honest-DiD restriction (post-treatment trend exactly extrapolating from pre-trend, M = 0), the lower bound is just barely below zero. The result is therefore not robust to *any* deviation from a strict linear-pre-trend extrapolation." — accurate but probably overstates the policy relevance of M = 0.

3. **(Conservative)** "Under the most policy-relevant honest restriction (DeltaRM with Mbar = 1), the average post-treatment ATT could plausibly be anywhere from -3.32 to 8.49 plans per 1,000 establishments. The point estimate of 2.66 is consistent with a meaningful policy effect, but the data alone cannot rule out a null or modestly negative effect." — this is the framing I'd recommend for an external audience.

The key reason the honest bounds are wide is the **t = 4 event-time effect** (5.96 ± 4.0 SE), which is essentially driven by a single cohort with one observation at horizon t+4. That cohort is Illinois (cohort 2018), and its t+4 effect is in 2022 — the same year California's program launched, which complicates interpretation. **A targeted re-analysis dropping or down-weighting t = 4 would tighten the honest bounds materially.**

## Caveats and limitations

1. **Sigma scaling.** The CS package's bootstrap-based standard errors don't match the analytical influence-function variance exactly. We used the influence-function correlation matrix, scaled to match the bootstrap SE diagonal. This is a defensible approximation but introduces some uncertainty about the exact width of the bounds. A more rigorous run would re-compute the variance directly via the cluster bootstrap on the full event study (slower; left for follow-up).

2. **Equal-weight averaging vs. cohort-weighted ATT.** The HonestDiD package operates on event-study coefficients with linear-combination weights l_vec. We used equal weights across t = 0..6, which gives the average post-treatment effect across event times. This is *not* the same as the simple cohort-weighted ATT of 2.37 reported as the headline, which weights cohorts by size. The honest bounds for the simple cohort-weighted ATT would require either implementing l_vec from cohort weights (non-trivial because cohorts are observed at different event-time horizons) or re-running on a cohort-specific basis. Recommend: report the equal-weight bounds as the official Honest DiD result, but caveat that they don't directly bound the headline simple ATT.

3. **The t = 4 event-time effect is dominating the average.** As noted above, this is a feature of the cohort structure: only one cohort (Illinois 2018) is observed at t + 4 in the panel, and its single observation has wide variance. The HonestDiD bounds reflect this honestly, but the resulting wide CI is more about cohort balance than pre-trend fragility.

4. **OR (cohort 2017) is omitted from the cohort aggregation but included in the event-study aggregation as t = 0 → 7.** This means OR shows up in event times 0 through 7, but its t = 7 observation is dropped because we restricted the panel to event times -6 through +6. There's no separate cohort-2017 ATT in the honest bounds.

## Files produced

| File | Contents |
|---|---|
| `analysis/did_honest_bounds.R` | R script; uses `did` and `HonestDiD` |
| `analysis/did_honest_bounds.log` | Full Rscript output, including raw CS event study and sensitivity printouts |
| `analysis/did_honest_bounds_v2_conservative.csv` | Tidy table of bounds (one row per restriction × parameter) |
| `analysis/did_honest_bounds_v2_conservative.png` | Sensitivity plot |

## What would change conclusions

If the user is willing to re-run, the following would tighten the bounds materially:

- **Drop t = 4 (or any horizon with a single cohort).** Restrict the event window to only horizons where ≥ 2 cohorts contribute. This would remove the noisy late-horizon estimates from the average.
- **Use the simple cohort-weighted ATT instead of equal-weight average.** Requires deriving the corresponding l_vec or re-running with a different aggregation.
- **Use cluster bootstrap variance directly.** Replace the influence-function-based sigma with a direct cluster bootstrap on the dynamic aggregation. Slower but more accurate.
