# Difference-in-Differences Design Memo

**Project:** State Auto-IRA Research
**Purpose:** Specification for the causal-analysis component of the project. This document defines the research question, identification strategy, data construction, estimator choice, and robustness program in enough detail to be implemented by a coding agent without further design decisions.
**Date:** April 27, 2026

---

## 1. Research question

Did state auto-IRA mandates cause an increase in the rate of new 401(k) plan formation among private-sector employers, relative to what would have occurred in the absence of the mandate?

The dataset built in v3 establishes that 106,577–115,690 firms in mandate states established 401(k) plans after their state's mandate took effect. That is a descriptive fact, not a causal claim. The DiD design tests whether mandate-state 401(k) formation rates rose *relative to comparable non-mandate states* over the same period — the comparison that lets us interpret the post-mandate increase as caused by the mandate rather than by secular trends in retirement plan adoption.

## 2. Identification strategy

### Treatment

A state is "treated" beginning in the year its auto-IRA mandate first applies to private employers. We run two parallel specifications corresponding to the two mandate-date definitions already established in v3:

- **v1-inclusive:** treatment turns on in the year of legislation/final regulation
- **v2-conservative:** treatment turns on in the year the program launches

Both specifications must be reported. They are not robustness checks of each other — they are the two defensible answers to two different questions (anticipation effect vs. operational-pressure effect), exactly as in the count reconciliation memo.

### Estimator: Callaway-Sant'Anna, not vanilla TWFE

The 10 mandate states adopted at staggered times between 2017 (Oregon) and 2024 (Maine, Delaware, New Jersey). Under staggered adoption with treatment-effect heterogeneity across cohorts, the standard two-way fixed effects estimator produces a weighted average of group-time treatment effects in which some weights can be negative — meaning the TWFE coefficient can have the wrong sign even when every individual cohort effect is positive (Goodman-Bacon 2021; de Chaisemartin & d'Haultfœuille 2020; Borusyak, Jaravel & Spiess 2024).

The headline estimator is therefore **Callaway-Sant'Anna group-time average treatment effects on the treated (ATT(g,t))**, aggregated to:

- An overall ATT
- Event-time aggregations (effect by years-since-treatment)
- Group-specific aggregations (effect by adoption cohort)

Implementation: `did` package in R (Callaway & Sant'Anna), or `csdid` in Stata. Both implementations should produce numerically identical estimates given the same panel; cross-validation between them is recommended.

Vanilla TWFE is reported alongside as an *illustrative contrast*, not as a robustness check or stronger version. The framing in the writeup should be "TWFE produces X, but for the well-known reasons above it is biased under staggered adoption with heterogeneous effects; the credible estimate is the CS ATT, which produces Y."

### Comparison group

CS requires specifying who serves as the comparison for each treated cohort at each point in time. Two options:

- **Never-treated:** non-mandate states, used as the comparison for every treated cohort
- **Not-yet-treated:** non-mandate states *plus* mandate states that haven't yet been treated

We run **not-yet-treated as the primary specification** (it preserves more comparison-group observations and is generally more efficient) and **never-treated as a robustness check**. If the two diverge meaningfully, that's a substantive finding about cohort heterogeneity worth investigating, not a methodological problem to paper over.

## 3. Data construction

### Unit and frequency

State-year panel. Unit = state, time = calendar year. Years 2017–2024 to match the v3 dataset window.

### Outcome variable

`new_401k_plans_st` = count of newly established single-employer 401(k) plans in state *s* in year *t*. "New" = plan effective date falls within year *t*. Filters match v3 exactly: pension code 2J, single-employer entity, valid EIN.

### Normalization

Raw counts are noisy and confound state size with treatment. Three candidate denominators, in preference order:

1. **Private employer establishments** from Census County Business Patterns (CBP) — the most defensible denominator because it represents the population of firms that *could* establish a plan
2. Private-sector employment from BLS QCEW
3. Total covered employment from BLS

The primary specification uses CBP-normalized rates. Raw counts and the other two normalizations are run as sensitivity checks. The outcome reported in tables is **new 401(k) plans per 1,000 private establishments**.

### Control states

All US states *not* in the mandate-state list at any point during the study window. Note: "no mandate as of 2024" is the relevant criterion, since states that pass mandates after our data window are still untreated within-sample.

**Exclude from controls:**

- States with mandatory voluntary multiple-employer plan (MEP) programs that aren't auto-IRA but might contaminate the comparison (e.g., Massachusetts CORE Plan for nonprofits — narrow scope but worth noting)
- States that passed auto-IRA legislation during the study window but where it had not yet taken effect by 2024 (these are "not-yet-treated" rather than "never-treated" and should be coded as such, not dropped, when using the not-yet-treated comparison group)

**Document but include:** states with voluntary state-facilitated programs (e.g., Washington Retirement Marketplace, New Mexico Work and Save) — these are voluntary and shouldn't materially affect employer plan-formation decisions, but flag them for a sensitivity check that drops them.

### Panel construction

```
state | year | new_401k_plans | private_establishments | new_401k_per_1000_estabs |
treated | first_treatment_year | mandate_date_definition | controls
```

One row per state-year. `treated` = 1 in years on or after `first_treatment_year`. `first_treatment_year` is `Inf` (or coded as 0 in the `did` package convention) for never-treated control states.

Two versions of the panel: one using v1-inclusive treatment dates, one using v2-conservative dates. Stored as `analysis/did_panel_v1_inclusive.csv` and `analysis/did_panel_v2_conservative.csv`.

## 4. Specifications to run

Run all of the following on both panels (v1 and v2):

1. **Baseline CS:** ATT aggregated overall, by event time, and by cohort. Not-yet-treated comparison group. Outcome: new 401(k) plans per 1,000 establishments.
2. **CS with never-treated comparison:** same but never-treated only.
3. **TWFE for contrast:** standard two-way fixed effects, reported with explicit caveat about bias under staggered adoption.
4. **Event-study plot:** dynamic effects with leads (pre-treatment placebo years) and lags (post-treatment effects). The pre-treatment coefficients are the test for parallel pre-trends. Plot leads -4 to -1 and lags 0 to +5 where data permits.

## 5. Robustness checks

Required:

- **Drop California.** California is ~50%+ of the dataset by firm count and is the dominant driver of the v1/v2 gap. Results should not depend on it. If they do, that's a finding worth reporting plainly, not hiding.
- **Drop zero-employee plans.** Solo 401(k)s are a different decision than employer-sponsored plans for employees. Re-run on the subset with >0 reported employees.
- **Restrict to firms with positive employee count and positive employer contribution data.** Smaller sample, cleaner story about what mandates do to actual employer-employee retirement plans.
- **Alternative outcome: ESRP formation rate** (any new employer-sponsored retirement plan, not just 401(k)) to test whether firms substitute across plan types.
- **Drop late-treatment states (ME, DE, NJ).** These states have material filing lag; their post-treatment counts may be artificially low.

Recommended:

- **Honest DiD bounds (Rambachan & Roth 2023)** for the event-study estimates, to bound how much the post-treatment estimates can change under plausible violations of parallel trends.
- **Permutation/randomization inference:** randomly assign placebo treatment dates to control states and test whether the estimated ATT falls in the tail of the placebo distribution.

## 6. Outputs

Each of the two panel runs (v1 and v2) produces:

- `did_results_<panel>.csv` — coefficient table with point estimates, standard errors, confidence intervals
- `did_event_study_<panel>.png` — event-study plot with 95% CIs
- `did_cohort_effects_<panel>.csv` — cohort-by-cohort ATT table
- `did_robustness_<panel>.csv` — table of all robustness specifications side-by-side

A combined writeup `analysis/did_results.md` synthesizes all of the above.

## 7. What the analysis cannot establish

This is important to state clearly in the final writeup so the analysis isn't oversold:

- DiD identifies the *effect of the policy*, not the *mechanism*. It cannot tell us whether firms chose 401(k)s because they preferred them on the merits, because they wanted to avoid administering payroll deductions to a state program, or because their payroll provider made it easier. The qualitative evidence bank (Workstream 5) is the only path to mechanism.
- The unit of analysis is plan formation, not employee outcomes. Whether mandate-induced plans actually improve participation, balances, or retirement security is a separate question.
- Selection: firms that establish 401(k)s in response to a mandate may be systematically different from firms that defaulted into the state program. The DiD answers "did the mandate cause more plan formation," not "are mandated-into-private plans good plans."
- Filing lag in 2024 mandate states (ME, DE, NJ) means the estimated effect for those cohorts will be biased downward in the current data; the analysis should be re-run after the next DOL data refresh and the result for late cohorts treated as preliminary.

## 8. Implementation checklist for the coding agent

1. Pull non-mandate-state Form 5500 + 5500-SF data using the same filters as `build_dataset.py`
2. Pull Census CBP private establishment counts by state-year for 2017–2024
3. Build the two state-year panels (v1 and v2)
4. Install `did` (R) or `csdid` (Stata)
5. Run all four specifications on both panels
6. Run all required robustness checks
7. Produce the four output files per panel
8. Write `did_results.md` synthesizing
