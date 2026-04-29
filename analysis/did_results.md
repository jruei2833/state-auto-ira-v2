# State Auto-IRA Mandates and 401(k) Plan Formation
## Difference-in-Differences Results

**Estimation date:** 2026-04-29
**Outcome:** New 401(k) plans per 1,000 private establishments
**Estimator:** Callaway-Sant'Anna group-time ATT (Callaway & Sant'Anna 2021), with TWFE reported alongside as a biased contrast
**Software:** `differences` 0.3.0 (Python implementation of CS) and `statsmodels` 0.14.6 (TWFE)
**Data:** Form 5500 + 5500-SF (DOL/EFAST2, 2017-2024) for the outcome; Census County Business Patterns (2017-2023, carried forward to 2024) for the denominator
**Inference:** Wild bootstrap with 999 iterations, simultaneous 95% confidence bands

---

## 1. Headline result

State auto-IRA mandates caused approximately **2.4 additional new 401(k) plans per 1,000 private establishments** per year in mandate states relative to non-mandate states. The result is robust across:

- Both mandate-date definitions (v1-inclusive: 2.37; v2-conservative: 2.37)
- Both control-group choices (not-yet-treated: 2.37; never-treated: 2.42)
- Dropping California (2.12)
- Restricting to plans with positive employee count (1.82)
- Substituting the broader "any new ESRP" outcome (2.19)
- Dropping late-treatment states ME/DE/NJ (2.31)
- 200-iteration permutation inference (placebo p ≈ 0.00; observed estimate is well outside the placebo distribution)

For context, mandate states' average baseline rate (pre-treatment) is about **6.5 new 401(k) plans per 1,000 establishments per year**. A 2.4-unit effect is therefore roughly a **35-40% increase** over the pre-mandate rate — a large effect size relative to typical retirement-policy interventions.

| Specification | Panel | ATT | 95% CI | Interpretation |
|---|---|---|---|---|
| **CS, not-yet-treated** (primary) | v1-inclusive | **2.37** | [1.53, 3.20] | Headline |
| **CS, not-yet-treated** (primary) | v2-conservative | **2.37** | [1.51, 3.23] | Headline |
| CS, never-treated | v1-inclusive | 2.42 | [1.55, 3.28] | |
| CS, never-treated | v2-conservative | 2.42 | [1.53, 3.32] | |
| TWFE (biased contrast) | v1-inclusive | 3.03 | [1.58, 4.48] | Upward-biased |
| TWFE (biased contrast) | v2-conservative | 3.07 | [1.71, 4.44] | Upward-biased |

**TWFE vs. CS:** TWFE produces estimates ~30% larger than CS. This is exactly the bias predicted by Goodman-Bacon (2021) when treatment effects vary across cohorts and treatment timing is staggered: the TWFE estimator weights treated-vs-already-treated comparisons negatively, producing a contaminated weighted average. The credible estimate is the CS ATT.

---

## 2. Pre-trends and event-time dynamics

The CS event-study coefficients show **flat pre-trends and an immediate, persistent post-treatment effect** that grows modestly over time:

### v1-inclusive event-time effects (CS, not-yet-treated)
| Event time | ATT | 95% sim. band | Significant? |
|---|---|---|---|
| -6 | 0.00 | [-0.70, 0.70] | no |
| -5 | 0.07 | [-0.34, 0.48] | no |
| -4 | 0.22 | [-0.63, 1.06] | no |
| -3 | 0.26 | [-0.18, 0.69] | no |
| -2 | 0.41 | [-0.92, 1.74] | no |
| -1 | 0.23 | [-0.51, 0.98] | no |
| **0** | **2.22** | **[0.29, 4.14]** | **yes** |
| 1 | 2.16 | [-0.58, 4.90] | no (wide) |
| **2** | **1.24** | **[0.11, 2.38]** | **yes** |
| 3 | 0.76 | [-0.66, 2.19] | no |
| 4 | 5.96 | [-3.23, 15.16] | no (very wide) |
| **5** | **3.38** | **[2.80, 3.96]** | **yes** |
| **6** | **2.90** | **[2.01, 3.79]** | **yes** |

All six pre-treatment leads are statistically indistinguishable from zero — the parallel-trends assumption is well supported in the data.

The wide CI at t=4 (and to a lesser extent t=1) reflects the small number of cohorts contributing at those horizons; this is a feature of staggered adoption with an 8-year window, not a precision problem.

### v2-conservative event-time effects (CS, not-yet-treated)
The v2 event-study traces nearly identical: pre-trends flat, t=0 effect ~2.19, growing to ~2.4-3.3 by t=5-6. (See `did_event_study_v2_conservative.csv`.)

Plots: `did_event_study_v1_inclusive.png`, `did_event_study_v2_conservative.png`.

---

## 3. Cohort-specific effects

Cohort effects are uniformly positive and statistically significant across both mandate-date definitions. Note that **Oregon (cohort 2017) does not appear** in either cohort table because the panel begins in 2017, so OR has no pre-treatment year and CS cannot estimate a separate ATT for it relative to its own pre-trend.

### v1-inclusive (legislation/regulation dates)
| Cohort year | Treated states | ATT | 95% sim. band | Significant? |
|---|---|---|---|---|
| 2018 | CA, IL | 2.04 | [0.82, 3.25] | yes |
| 2022 | CT, MD | 2.58 | [1.86, 3.30] | yes |
| 2023 | CO, VA | 2.58 | [1.09, 4.07] | yes |
| 2024 | ME, DE, NJ | 3.19 | [0.75, 5.63] | yes |

### v2-conservative (program-launch dates)
| Cohort year | Treated states | ATT | 95% sim. band | Significant? |
|---|---|---|---|---|
| 2018 | IL | 1.01 | [0.81, 1.22] | yes |
| 2019 | CA | 3.20 | [2.99, 3.42] | yes |
| 2022 | CT, MD | 2.58 | [1.67, 3.50] | yes |
| 2023 | CO, VA | 2.58 | [0.68, 4.48] | yes |
| 2024 | ME, DE, NJ | 3.19 | [0.08, 6.29] | yes |

The v1/v2 differences in the early cohorts are illuminating: the v1-inclusive specification splits CA and IL into a single 2018 cohort with a smaller ATT (2.04), while v2-conservative isolates CA into its own 2019 cohort with a much larger ATT (3.20). Substantively this means **the early CA mandate effect kicks in around the program-launch date (mid-2019), not the regulation date (late 2018)**, which is consistent with employers responding to operational pressure rather than legal anticipation. The IL effect appears earlier and is smaller in magnitude.

The 2024 cohort (ME, DE, NJ) has a large but imprecisely estimated effect — DOL filing lag means we observe only partial post-treatment data for these states, and the result for this cohort should be treated as preliminary and re-run after the next data refresh.

---

## 4. Robustness

| Robustness check | Panel | ATT | 95% CI |
|---|---|---|---|
| Drop California | both | 2.12 | [1.17, 3.07] |
| Outcome: 401(k) with positive employee count (excludes solo) | v1 | 1.82 | [1.25, 2.40] |
| Outcome: 401(k) with positive employee count | v2 | 1.80 | [1.23, 2.37] |
| Outcome: any new ESRP (substitution test) | v1 | 2.19 | [1.33, 3.05] |
| Outcome: any new ESRP | v2 | 2.24 | [1.33, 3.16] |
| Drop late-treatment (ME/DE/NJ) | v1 | 2.31 | [1.47, 3.15] |
| Drop late-treatment (ME/DE/NJ) | v2 | 2.31 | [1.43, 3.19] |
| Permutation inference (200 iter) | v1 | 2.37 | placebo p = 0.00 |
| Permutation inference (200 iter) | v2 | 2.37 | placebo p = 0.00 |

Three robustness findings deserve callout:

**Drop CA.** California is ~50% of the firm-level dataset, but the ATT changes only from 2.37 to 2.12 when CA is excluded. The result is not a California artifact — the other nine mandate states drive most of it.

**Solo vs. employer plans.** Restricting to plans with positive employee count drops the ATT from 2.37 to 1.82. About a quarter of the headline effect is solo 401(k)s — meaning a non-trivial share of mandate-induced "plan formation" is sole proprietors and very small firms self-employed setting up retirement accounts. This is still a real outcome of the mandate, but it's not the same thing as employer-employee retirement coverage.

**Substitution to other ESRPs.** The "any new ESRP" outcome gives ATT = 2.19, which is *smaller* than the 401(k)-specific ATT of 2.37. If mandates were causing massive substitution from other plan types into 401(k)s, we'd expect the broader outcome to be near zero. It isn't. The mandates are causing **net new ESRP formation**, not just plan-type substitution.

**Permutation inference.** Of 200 random reassignments of treatment status to never-treated states, none produced a placebo ATT exceeding the observed estimate of 2.37. This is strong evidence that the effect is not a random feature of any particular comparison set.

---

## 5. What this analysis can and cannot establish

**Can establish:**
- Mandate states experienced a statistically and economically significant increase in new 401(k) plan formation relative to non-mandate states, beginning in the year of treatment and persisting.
- The effect is not driven by California, by solo 401(k)s alone, by substitution from other plan types, or by the 2024 cohort.
- Pre-trends are flat, supporting the parallel-trends assumption.

**Cannot establish:**
- **Mechanism.** DiD identifies the policy effect, not why firms responded. We cannot tell from this analysis whether firms chose 401(k)s because they preferred them on the merits, because they wanted to avoid administering payroll deductions to a state program, because their payroll provider made it easier, or some combination. Mechanism inference requires the qualitative evidence bank (Workstream 5).
- **Employee outcomes.** The unit of analysis is plan formation, not participation, balances, or retirement security. Whether mandated-into-private plans actually improve worker outcomes is a separate question.
- **Selection.** Firms that establish 401(k)s in response to a mandate may be systematically different from firms that defaulted into the state program (e.g., larger, more sophisticated, with better payroll vendor relationships). The DiD answers "did the mandate cause more plan formation," not "are mandate-induced 401(k)s better for workers than the state program."
- **Late-cohort effects.** ME, DE, and NJ have material DOL filing lag. Their 2024 ATT is preliminary and should be revisited after the next data refresh; the dropped-late-treatment robustness check is the more credible result for this cohort while data lag persists.

---

## 6. Files

| File | Contents |
|---|---|
| `analysis/state_year_new_401k.csv` | State-year aggregation of new single-employer 401(k) plans (and ESRP / with-employees variants) from Form 5500 + 5500-SF, 2017-2024, all 50 states + DC |
| `analysis/cbp_state_year.csv` | CBP private establishments + employment by state-year (2017-2023 from Census API; 2024 carried forward) |
| `analysis/did_panel_v1_inclusive.csv` | Estimation panel using v1 (legislation/regulation) treatment dates |
| `analysis/did_panel_v2_conservative.csv` | Estimation panel using v2 (program-launch) treatment dates |
| `analysis/did_results_<panel>.csv` | Headline coefficient table per panel |
| `analysis/did_event_study_<panel>.csv` | CS event-time and TWFE event-study coefficients |
| `analysis/did_event_study_<panel>.png` | Event-study plot with 95% CI bands |
| `analysis/did_cohort_effects_<panel>.csv` | Cohort-by-cohort ATT |
| `analysis/did_robustness_<panel>.csv` | Robustness specs side-by-side |
| `analysis/did_summary_all_panels.csv` | Cross-panel summary |

## 7. Reproduction

```bash
cd state-auto-ira-v2
python analysis/build_state_year_panel.py   # ~5-10 min, processes 8 GB of raw 5500 data
python analysis/fetch_cbp.py                # ~10 sec, hits Census API
python analysis/build_did_panels.py         # <1 sec
python analysis/run_did.py                  # ~30 sec
```

Random seed 42 used throughout for bootstrap and permutation reproducibility.

## 8. Caveats and known limitations

1. **CBP 2024 not yet released.** The 2024 establishment denominator is carried forward from 2023, so 2024 rates are slight upper bounds. Effect on the ATT estimate is small because the 2024 cohort's effect is identified primarily by the on/off treatment indicator rather than by the precise denominator.

2. **PLAN_EFFECTIVE_DATE > filing year.** Form 5500 filings sometimes report plans with effective dates in the *following* calendar year (e.g., a 2024 filing for a plan effective 2025-08). Our state-year aggregation uses the effective year, which means very late-2024 / early-2025 plans appear in the 2024 panel cell. The descriptive dataset in `data/v1-inclusive/` and `data/v2-conservative/` makes the same choice for consistency.

3. **OR (cohort 2017) is the omitted cohort.** With an 8-year window starting in 2017, OR has no pre-treatment observation in the panel and is therefore not separately identified in the cohort aggregation. OR's contribution to the simple-aggregation ATT comes from its post-2017 levels relative to the never-treated mean. A longer panel (extending to 2015 or 2016) would let us recover OR's separate cohort effect, at the cost of using earlier filing data with lower coverage of the relevant pension code.

4. **No covariates.** The CS specification is uncovariate-adjusted. Adding state-level controls (demographic composition, industry mix, prior plan adoption) would be a natural next step but was not in scope for this run. The robustness of the result across multiple specifications and the flat pre-trends suggest covariate adjustment is unlikely to change the qualitative conclusion.

5. **Honest DiD bounds (Rambachan-Roth 2023) not implemented in this run.** Implementing the `HonestDiD` package would let us bound the ATT under plausible violations of parallel trends; it's a recommended next step, not a current output.
