# State Auto-IRA Research — Stakeholder Status Update

**This is a living document.** It is updated in place as findings come in. Previous status drafts (`FINAL_SUMMARY.md`, the original `State_AutoIRA_Project_Report.md` from February) are superseded by this file but kept in the repo for history.

**Last updated:** 2026-04-29
**Document maintained by:** project team
**Source-of-truth file:** [deliverables/stakeholder_status_update.md](deliverables/stakeholder_status_update.md) (markdown). The `.docx` version is regenerated from this markdown via `make stakeholder-doc`.

---

## What's new since the prior status draft (Feb 2026)

The February 2026 report (`deliverables/State_AutoIRA_Project_Report.md`) closed out the descriptive-dataset workstream with a validated count of **115,690 firms** under the v1-inclusive mandate-date rule. Since then:

- **The descriptive count was reconciled to two figures, not one.** The 115,690 figure remains correct under the v1-inclusive (legislation/regulation date) rule; under the v2-conservative (program-launch date) rule the figure is 106,577. Both are valid answers to two different policy questions. See [count reconciliation memo](count_reconciliation_memo.md).
- **A causal analysis was completed.** Difference-in-Differences using the Callaway-Sant'Anna estimator gives a headline ATT of 2.37 additional new 401(k) plans per 1,000 private establishments per year in mandate states relative to non-mandate states — a 35-40% increase over the pre-mandate baseline. Independently cross-validated in R. See [DiD results](../analysis/did_results.md) and [R validation](../analysis/did_r_validation.md).
- **Firm-level composition characterized.** 62% of mandate-induced 401(k) plans are solo or micro firms (≤9 covered participants); only 0.7% are large (250+). See [firm-level analysis](../analysis/firm_level_analysis.md).
- **Match-formula evidence pivoted from firm-level to industry benchmarks.** SEC EDGAR pilot returned a null finding (firms in the dataset are predominantly private); BrightScope is enterprise-licensed only and not accessible. Pivoted to Vanguard / PSCA / ICI/BrightScope aggregate benchmarks. See [match formula pilot summary](match_formula_pilot_summary.md).
- **DOL Form 5500 data refreshed (Apr 2026).** Re-pull added +400 firms in v2-conservative; late-treatment states (ME, DE, NJ) grew by ~5%. The DiD is not yet re-run on the refreshed panel — pending decision based on the [delta report](../methodology/dol_refresh_delta_2026_04.md).
- **Honest DiD bounds (Rambachan-Roth) computed.** The DiD result is fragile to plausible parallel-trend violations under the most policy-relevant honest restriction; primarily driven by a single noisy event-time horizon, not by pre-trend evidence. See [honest bounds memo](../analysis/did_honest_bounds.md).
- **CalSavers CPRA exemption-filing request drafted.** The letter at [`deliverables/calsavers_cpra_request.md`](calsavers_cpra_request.md) requests California's administrative list of employers claiming exemption from CalSavers on the basis of having a private retirement plan. CA represents ~70% of the v3 dataset, so the exemption-filing list is a near-direct independent crosscheck. **Drafted but not yet sent;** awaiting project-owner review of the send-off checklist.

---

## Question 1: Count growth — what the dataset shows

The descriptive dataset answers the question "how many firms in mandate states established 401(k) plans after their state's mandate took effect?" Two defensible counts, both validated:

| Mandate-date rule | Firm count | Rationale |
|---|---|---|
| **v1-inclusive** (date of legislation / final regulation) | **115,690** | Captures anticipation effects: firms responding to a known coming mandate |
| **v2-conservative** (date the program launches) | **106,577** | Captures operational-pressure effects: firms responding to the actual existence of an alternative they would otherwise need to enroll in |

The 9,113-firm gap is concentrated in California (8,540 firms, ~94% of the gap), where roughly four years separated the 2018 enabling regulation from the 2019 CalSavers statewide rollout. Other states with shorter legislation-to-launch windows produce nearly identical counts under both rules.

**For headline reporting we recommend the conservative figure (106,577)**, with the inclusive figure presented alongside.

### State breakdown (v2-conservative)

| State | Program | Mandate (v2) | Firms |
|---|---|---|---|
| CA | CalSavers | 2019-07-01 | 72,972 |
| IL | Secure Choice | 2018-11-01 | 14,513 |
| OR | OregonSaves | 2017-11-01 | 7,313 |
| MD | MarylandSaves | 2022-09-01 | 3,556 |
| CO | SecureSavings | 2023-01-01 | 2,786 |
| CT | MyCTSavings | 2022-04-01 | 2,409 |
| VA | RetirePath | 2023-07-01 | 2,150 |
| NJ | RetireReady NJ | 2024-06-30 | 603 |
| ME | Maine Retirement Savings | 2024-01-01 | 143 |
| DE | EARNS | 2024-07-01 | 132 |
| **Total** | | | **106,577** |

(California alone is ~68% of the dataset; this concentration is documented and stress-tested in the DiD analysis.)

### Has the count changed since the last refresh?

The April 2026 DOL refresh added +400 firms in v2-conservative (+0.38%), driven primarily by:
- New 2024-effective filings the DOL received between January and March 2026
- 2025-effective filings (a year not previously in scope) — +668 firms with effective dates in 2025

**Late-treatment states grew the most in percentage terms:** NJ +6.3%, DE +3.0%, ME +4.2%. This is the filing-lag catch-up that was a known issue. NJ now sits at 641 firms (was 603), still small but materially less imprecise.

**Validation status:** Two independent AI tools (Claude Code and Codex) reproduced the v3 dataset state-by-state with 100% agreement. An R independent re-implementation of the DiD on the same panel reproduced the headline ATT to four decimal places. The dataset's underlying integrity is solid.

---

## Question 2: Status on three priority items

> ⚠️ **Structural note:** This section is organized around what we believe were the three originally-stated priority items: (1) the causal claim, (2) firm-level descriptive characterization, (3) match formula / employee outcomes. If a different breakdown was intended, this section should be re-keyed accordingly — the underlying findings don't change, only the framing.

### Priority Item 1: Causal claim — did mandates *cause* the additional 401(k) formation?

**Status: completed; result is robust on the headline but fragile to weak assumptions.**

Difference-in-Differences using the Callaway-Sant'Anna group-time ATT estimator (the modern best practice for staggered adoption with heterogeneous treatment effects):

| Specification | Panel | ATT | 95% CI |
|---|---|---|---|
| **CS, not-yet-treated (primary)** | v1-inclusive | **2.37** | [1.53, 3.20] |
| **CS, not-yet-treated (primary)** | v2-conservative | **2.37** | [1.51, 3.23] |
| CS, never-treated comparison | both | 2.42 | [1.55, 3.32] |
| TWFE (biased contrast) | both | 3.03–3.07 | [1.58, 4.48] |

**Interpretation:** Mandate states experienced approximately 2.4 additional new 401(k) plans per 1,000 private establishments per year, relative to comparable non-mandate states, beginning in the year of treatment. The pre-trend leads (event times -6 through -1) are statistically indistinguishable from zero — the parallel-trends assumption is well supported in the pre-period data.

**Robustness — passed:**
- Drop California → 2.12 (still robust)
- Restrict to plans with positive employees only → 1.82 (smaller but still substantial)
- Use any-ESRP outcome (substitution test) → 2.19 (rules out plan-type substitution)
- Drop late-treatment states (ME/DE/NJ) → 2.31 (not late-cohort artifact)
- Permutation inference, 200 placebo re-assignments → observed ATT well outside placebo distribution (p ≈ 0)

**Cross-validation — passed:** R `did` package reproduced the Python `differences` headline to four decimal places (R: 2.3717, Python: 2.3717).

**Honest DiD bounds (Rambachan-Roth 2023) — caveat.** Under the most policy-relevant honest restriction (DeltaRM with Mbar = 1, "post-treatment violations no larger than the largest pre-treatment violation"), the bounds for the average post-treatment ATT are [−3.32, 8.49], crossing zero. The fragility is driven primarily by one noisy event-time horizon (t=4), where only a single cohort contributes — a feature of the panel structure, not evidence of pre-trend violations. A targeted re-analysis dropping or down-weighting that horizon would tighten the bounds materially. Full discussion in [analysis/did_honest_bounds.md](../analysis/did_honest_bounds.md).

**Bottom line we recommend for external audiences:** the causal claim is well-supported under standard assumptions; the headline ATT is reproducible and robust to most stress tests. Honest sensitivity analysis suggests the result should not be over-interpreted as point-identified — there's a defensible range that includes possible null effects under weaker assumptions, though the data does not support that null.

### Priority Item 2: Firm-level descriptive characterization — *who* are these firms?

**Status: completed.**

Headline finding: **the modal mandate-induced 401(k) is a micro-firm plan with 2-9 employees.**

| Size bucket | Definition (covered participants) | Firms | % of dataset |
|---|---|---|---|
| Solo | 0-1 | 21,148 | 19.8% |
| **Micro** | **2-9** | **45,459** | **42.7%** |
| Small | 10-49 | 32,960 | 30.9% |
| Medium | 50-249 | 6,260 | 5.9% |
| Large | 250+ | 742 | 0.7% |

**Solo + micro = 62% of the dataset.** This is exactly what auto-IRA mandates were designed to do: state-program enrollment thresholds are typically 5+ employees, so very small firms that don't qualify (or want to avoid) the state program are the ones most likely to set up a private 401(k) instead.

**Solo composition varies by state:** highest solo share in CO (32.0%), lowest in ME (18.9%). High-solo states are largely capturing self-employed individuals; low-solo states are capturing more genuine employer-employee plan formation. Worth flagging as an interpretation caveat.

**Large firms are rare** (0.7%), which is intuitive: most large firms already had 401(k)s before mandates took effect. This composition is also why the SEC EDGAR match-formula pilot returned a null finding — public firms cluster in the large bucket.

Full detail: [analysis/firm_level_analysis.md](../analysis/firm_level_analysis.md).

### Priority Item 3: Match formula and employee outcomes

**Status: pivoted from firm-level to industry benchmarks; firm-level data not feasible at scale within current sources.**

| Source attempted | Outcome |
|---|---|
| **DOL Form 5500 Schedule H/I** (already in our build) | Only 3.4% of firms have employer-contribution data populated; aggregate dollar amounts only, no match formulas. |
| **SEC EDGAR pilot** (50 largest firms by participant count) | **0/50 high-confidence matches.** Mandate-induced 401(k) firms are overwhelmingly private; EDGAR is the wrong source. Pipeline validated on a real public-firm 10-K (correctly extracted "100% match up to 2% of comp; safe harbor"). |
| **BrightScope direct access** | **Not accessible.** Acquired by ISS in 2016; legacy public profile pages now return HTTP 404. ISS MarketPro Retirement is enterprise-licensed only with no API or research tier. See [methodology/brightscope_access_assessment.md](../methodology/brightscope_access_assessment.md). |
| **Vanguard / PSCA / ICI/BrightScope aggregate benchmarks** | **Substituted in.** Benchmarks for what match formulas look like in the broader 401(k) industry. Most common formula across all three sources: 50% on first 6% of pay (used by 13-22% of plans, depending on source). Average promised match: 4.0-4.6% of pay. See [deliverables/match_formula_industry_benchmarks.md](match_formula_industry_benchmarks.md). |

**Important framing for the policy memo:** the industry benchmarks describe what 401(k) match formulas look like *broadly*, not the specific match formulas of the firms in the State Auto-IRA dataset. Most firms in the dataset are too small to appear in any of those source samples (Vanguard, PSCA, and BrightScope all skew toward larger plans). Use the benchmarks for context, not as a substitute for firm-specific evidence.

**Qualitative-evidence workstream:** Initial entries (target: ~10 in batch 1, expanding to 25-50) are being collected from press releases, payroll-vendor case studies, and public statements. *(This section will be expanded with specifics once the qualitative evidence bank file is added to the repo. Initial batch is being prepared in a separate chat session and is expected to include independent corroboration from Guideline and Gusto on the operational-pressure mechanism.)*

---

## Open issues and what's coming next

The project board has five candidate workstreams remaining. Highest-value next-step recommendation is in [`deliverables/next_step_recommendation.md`](next_step_recommendation.md): **the CalSavers CPRA exemption-filing request.** The letter has been drafted ([deliverables/calsavers_cpra_request.md](calsavers_cpra_request.md)) and is awaiting project-owner send-off review.

| Candidate | Effort | Value | Status |
|---|---|---|---|
| **CalSavers CPRA exemption-filing request** | low (request letter; 2-8 wk wait) | high (independent state-administrative crosscheck on ~70% of dataset) | **Drafted; awaiting send** |
| Expand qualitative evidence to 25-50 entries | medium | medium-high (mechanism inference; Workstream 5 explicitly required for mechanism) | Sprint 2 |
| Census CBP 2024 data release watch + DiD re-run | low | low-medium (refines denominator; doesn't change ATT direction) | Passive (waiting on Census) |
| Re-run DiD on Apr-2026 refreshed panel | medium | low (only +0.4% data change; late-cohort effect would shift modestly) | Optional |
| Final report synthesis | high | high (eventual deliverable) | Premature |
| Pull firm-level + DiD into unified narrative for final paper | medium | medium | After CPRA returns |

---

## Caveats and uncertainties

What this analysis can establish:

- The **descriptive count** (115,690 / 106,577) is solid and validated by two independent tools.
- The **causal claim** is supported under standard parallel-trends assumptions, robust to most stress tests, and cross-validated in R.
- The **composition** of the affected population (62% small firms) is clear from the microdata.

What this analysis cannot establish:

- **Mechanism.** DiD identifies the policy effect, not the reason firms chose 401(k)s over enrolling in the state program. This requires the qualitative evidence bank.
- **Employee outcomes.** The unit of analysis is plan formation, not participation, balances, or retirement security.
- **Selection.** Firms that establish 401(k)s in response to a mandate may be systematically different from firms that defaulted into the state program.
- **Honest-DiD upper-bound.** Under weak assumptions about parallel-trend violations, a null effect cannot be ruled out, though the data does not support that null.
- **Filing lag for late-treatment states (ME, DE, NJ).** Substantially improved in the Apr-2026 refresh (NJ +6.3%) but still imperfect; expect another ~12 months for full convergence.

---

## Source-of-truth files

This document synthesizes the following primary sources. Always link to the source file rather than restating its content here, and keep this document in sync as those files update.

| Topic | Primary source |
|---|---|
| DiD design | [methodology/did_design_memo.md](../methodology/did_design_memo.md) |
| DiD results | [analysis/did_results.md](../analysis/did_results.md) |
| R cross-validation | [analysis/did_r_validation.md](../analysis/did_r_validation.md) |
| Honest DiD bounds | [analysis/did_honest_bounds.md](../analysis/did_honest_bounds.md) |
| Firm-level descriptive | [analysis/firm_level_analysis.md](../analysis/firm_level_analysis.md) |
| Count reconciliation | [deliverables/count_reconciliation_memo.md](count_reconciliation_memo.md) |
| EDGAR match formula pilot | [deliverables/match_formula_pilot_summary.md](match_formula_pilot_summary.md) |
| BrightScope access | [methodology/brightscope_access_assessment.md](../methodology/brightscope_access_assessment.md) |
| Industry match-formula benchmarks | [deliverables/match_formula_industry_benchmarks.md](match_formula_industry_benchmarks.md) |
| DOL refresh delta (Apr 2026) | [methodology/dol_refresh_delta_2026_04.md](../methodology/dol_refresh_delta_2026_04.md) |
| Source provenance log | [methodology/source_provenance_log.csv](../methodology/source_provenance_log.csv) |
| Next-step recommendation | [deliverables/next_step_recommendation.md](next_step_recommendation.md) |

## How to update this document

1. Edit `deliverables/stakeholder_status_update.md` directly.
2. Run `make stakeholder-doc` from the repo root to regenerate the `.docx`.
3. Commit the updated `.md` (the `.docx` is gitignored as a derived artifact).
4. **Do not create a new versioned status doc.** This is the canonical location.
