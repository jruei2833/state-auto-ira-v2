# State Auto-IRA Mandates and Private 401(k) Plan Formation

**A firm-level analysis of the policy mechanism identified by Bloomfield, Goodman, Rao & Slavov**

*America First Policy Institute*
*May 2026*

---

## Executive Summary

State auto-IRA mandates cause meaningful private 401(k) plan formation among small employers. Using federal Form 5500 filings across the ten states with active auto-IRA mandates, this analysis identifies approximately 106,577 firms that established new 401(k) plans after their state's mandate took effect. A staggered difference-in-differences design comparing mandate states to non-mandate controls produces an average treatment effect of approximately 2.37 additional new 401(k) plans per 1,000 private establishments per year. The result is robust to dropping California (which accounts for the largest share of the dataset), to dropping the most recently mandated states, and to alternative denominator definitions including the policy-relevant subset of mandate-eligible firms (~7.83 per 1,000 SUSB-defined firms with five or more employees).

The finding extends Bloomfield, Goodman, Rao and Slavov's NBER work on the firm-side "crowd-in" response to state mandates by providing firm-level identification, a difference-in-differences research design, and external corroboration from independent provider data. A separate analysis by Gusto using its own 300,000-firm small-business administrative dataset estimates a 45 percent increase in 401(k) adoption among Colorado firms subject to the SecureSavings mandate, with the largest gains in the same 5–9 employee firm-size band that this analysis identifies as the dominant source of new plan formation. The Colorado Department of Treasury officially cites this finding in its 2024 program announcement.

The mandate-induced response is concentrated in small employers. Sixty-two percent of mandate-induced plans are established by firms with nine or fewer participants. The headline finding is therefore best understood as: state auto-IRA mandates cause small private employers, who would otherwise have no retirement plan, to establish private 401(k) plans rather than enroll in the state-facilitated alternative.

This memo summarizes the dataset construction, identification strategy, headline findings, robustness program, and the analytical limits of the design.

---

## Background

In 2017, Oregon launched OregonSaves, the first state-facilitated automatic-enrollment retirement savings program for private-sector workers. Nine additional states have since enacted similar mandates: Illinois (2018), California (2019), Connecticut and Maryland (2022), Colorado and Virginia (2023), and Maine, Delaware, and New Jersey (2024). Each mandate requires private employers above a state-specific size threshold to either facilitate the state's auto-IRA program or offer their own qualified retirement plan, typically a 401(k).

The retirement-policy literature has historically debated whether state mandates would *crowd out* private plan formation (by creating a lower-administrative-burden alternative) or *crowd in* private plan formation (by raising the policy salience of retirement coverage and creating a forcing event for compliance decisions). Bloomfield, Goodman, Rao and Slavov (NBER) found evidence of crowd-in: roughly 17 percent of mandate-affected firms in their data established employer-sponsored retirement plans after the mandate took effect, with no corresponding crowd-out.

This analysis investigates the firm-side response identified by Bloomfield, Goodman, Rao and Slavov using a different research design and a more recent dataset. The contribution is threefold: (1) firm-level identification using federal Form 5500 filings rather than the aggregate state-level data their paper relies on; (2) a Callaway-Sant'Anna staggered difference-in-differences estimator applied to ten mandate states with non-mandate states as controls; and (3) firm-level descriptive analysis of which firms respond to mandates.

---

## Dataset

The underlying dataset consists of all single-employer 401(k) plans (Form 5500 pension code 2J) established in the ten mandate states between 2017 and 2024, with plan effective dates falling on or after the applicable mandate date. Data was extracted from Department of Labor Form 5500 and Form 5500-SF bulk filings, with cross-validation across multiple independent extraction tools producing 100 percent state-by-state agreement.

Two parallel firm counts are reported corresponding to two defensible definitions of "after the mandate":

| Definition | Firm count | Mandate date used |
|---|---|---|
| Inclusive | 115,690 | Date of legislation or final regulation |
| Conservative | 106,577 | Date the state-facilitated program launched |

The 9,113-firm gap between the two definitions is concentrated almost entirely in California (8,540 firms), reflecting the four-year window between California's 2018 enabling regulation and the 2019 CalSavers statewide rollout. The remaining 573 firms are spread across Illinois (280), New Jersey (213), and Delaware (83). For the headline analysis we use the conservative definition; the inclusive definition is reported alongside as a robustness specification.

The dataset was last refreshed in April 2026 against the most recent DOL bulk filings. The refresh produced a +0.35 percent change in headline counts, with late-mandate states (Maine, Delaware, New Jersey) showing the expected catch-up as filing lag resolved. Source provenance for every filing year is documented in the project repository.

---

## Identification Strategy

### Estimator

The mandate states adopted at staggered times between 2017 and 2024. Under staggered treatment adoption with heterogeneous treatment effects across cohorts, the standard two-way fixed effects estimator can produce biased estimates due to the well-documented forbidden-comparisons problem (Goodman-Bacon 2021; de Chaisemartin & d'Haultfœuille 2020). The headline estimator is therefore the Callaway-Sant'Anna group-time average treatment effect (ATT(g,t)), aggregated using the cohort-weighted simple aggregation that does not over-weight long-horizon event-time estimates identified by single cohorts.

The estimator was implemented in Python's `differences` package and cross-validated in R's `did` package. Headline ATT estimates agree to four decimal places across implementations.

### Comparison group

The Callaway-Sant'Anna design uses non-mandate states as the comparison group for each treated cohort, with not-yet-treated states (states that pass mandates after the analysis window or have not yet been treated at a given point in time) included in the comparison pool. Forty states without auto-IRA mandates serve as the primary comparison group.

### Outcome variable and denominator

The outcome variable is new 401(k) plan formations per state-year, normalized by a denominator representing the population of firms or establishments that could potentially establish a plan. The headline denominator is private establishments from Census County Business Patterns (CBP), giving a unit of "new 401(k) plans per 1,000 private establishments per year." This denominator is used because it matches the establishment-level convention in the existing literature on firm-side mandate responses.

Three alternative denominators are used as sensitivity checks: BLS Quarterly Census of Employment and Wages (QCEW), Census Statistics of US Businesses (SUSB) all firms, and SUSB firms with five or more employees. The SUSB-5+ denominator is conceptually the most policy-relevant — it normalizes by the population of firms that the mandate actually applies to in most states — and is reported alongside the CBP-based headline.

### Covariates

State and year fixed effects. No additional covariates are included in the baseline specification.

---

## Headline Findings

### Average treatment effect

The headline cohort-weighted simple ATT under the conservative mandate-date definition is **2.37 additional new 401(k) plans per 1,000 private establishments per year**, with a 95 percent confidence interval of approximately [1.5, 3.2]. The estimate under the inclusive definition is statistically and substantively identical (2.37). The result is robust across all four denominator specifications:

| Denominator | Source | Conceptual unit | ATT (conservative) | ATT (inclusive) |
|---|---|---|---|---|
| Census CBP | Establishment count | Physical location | 2.37 | 2.37 |
| BLS QCEW | UI-covered worksite | Employment-covered worksite | 1.62 | 1.59 |
| Census SUSB (all firms) | Legal entity | Firm | 2.90 | 2.89 |
| Census SUSB (5+ employees) | Legal entity, mandate-eligible | Mandate-eligible firm | 7.83 | 7.83 |

The variation across denominators reflects differences in what is being counted (physical locations vs. legal entities vs. employment-covered worksites), not differences in the underlying causal effect. The qualitative conclusion — that mandates cause meaningful new 401(k) plan formation — holds under all four specifications. The SUSB-5+ specification, normalizing by mandate-eligible firms, gives the most policy-relevant magnitude: roughly eight additional 401(k) plans per 1,000 firms in the directly affected population, per year.

### Robustness

The headline result survives every preregistered robustness check:

| Specification | ATT |
|---|---|
| Headline (CBP, conservative, cohort-weighted simple) | 2.37 |
| Drop California | 2.12 |
| Drop late-treatment states (ME, DE, NJ) | 2.31 |
| Restrict to plans with positive employee count | 1.82 |
| Alternative outcome: any new ESRP, not just 401(k) | 2.19 |

Dropping California — which accounts for the largest single share of the dataset — reduces the ATT only modestly, from 2.37 to 2.12. The estimate is not driven by any one state.

### Pre-trends and sensitivity

The Callaway-Sant'Anna event-study shows flat pre-treatment trends across all six pre-treatment leads, supporting the parallel-trends assumption that underlies the design. Under Rambachan-Roth honest difference-in-differences sensitivity analysis, the headline estimate is robust to plausible smoothness restrictions on parallel-trend deviations. Long-horizon event-time aggregations widen substantially under sensitivity analysis, but this is driven by individual event-time coefficients being identified by single cohorts rather than by substantive concerns about parallel trends. The cohort-weighted simple aggregation does not over-weight these noisy long-horizon estimates and is the more defensible headline.

A permutation test that randomly reassigns treatment dates to control states places the observed ATT outside the entire placebo distribution (p ≈ 0.00).

---

## External Corroboration

The headline result is independently corroborated by a separate analysis using completely different data and a different research design. In June 2025, Gusto's Government Affairs and Economic Research teams published an analysis of state auto-IRA mandate effects using their proprietary administrative data on 300,000 small-business customers. They estimate that the share of Colorado firms with five or more employees offering a 401(k) plan increased 45 percent in the year leading up to the SecureSavings registration deadline (from 25.3 percent to 38.0 percent). Across five neighboring non-mandate states (Arizona, Utah, Nevada, Kansas, Nebraska), the comparable share was essentially flat (20.4 percent to 21.2 percent). The same pattern holds for California and Oregon under their respective mandate deadlines.

The Gusto analysis is notable for two reasons. First, it is essentially a separate natural experiment using completely different data and a different research design (state-vs-neighboring-state simple difference-in-differences), arriving at the same qualitative conclusion as our staggered Callaway-Sant'Anna estimator on Form 5500 data. Independent quantitative studies converging on the same conclusion is the strongest possible form of cross-validation for the headline causal claim.

Second, Gusto's firm-size breakdown matches our firm-level descriptive findings exactly. Their largest mandate effect appears in 5–9 employee firms (+52 percent), with smaller proportional effects in 10–24 employee firms (+37 percent) and 25+ employee firms (+43 percent). Firms with 1–4 employees, which are not subject to the Colorado mandate, show essentially no change. Our descriptive analysis finds that 62 percent of mandate-induced plans in the v3 dataset are established by firms with fewer than ten participants. Two independent analyses on different data sources identifying the same firm-size composition is unusually strong corroboration of the substantive finding.

The Colorado Department of Treasury officially cites the Gusto analysis in its December 2024 program announcement, with State Treasurer Dave Young noting the +45 percent figure when urging continued employer compliance. Independent corroboration of this kind — covering provider data, official state communications, and our own federal-data analysis — supports the conclusion that the mandate-to-401(k) mechanism is real, measurable, and concentrated in the small-employer population.

---

## Firm-Level Findings

The mandate-induced 401(k) population skews heavily toward small employers. In the v2-conservative dataset of 106,577 firms:

- 62 percent of plans are established by firms with 0–9 participants
- 0.7 percent are established by firms with 250 or more participants
- Median plan size is in the micro-firm range

Normalizing against the SUSB firm-size distribution sharpens this picture. Per-firm response rates rise monotonically with firm size up to the 20–99 employee band before declining, but the absolute count of mandate-induced plans is dominated by the smallest firm-size bands simply because those bands contain the most firms. The substantive interpretation: the mandate produces a higher *response rate* per firm in the 20–99 size band, but the largest *absolute number* of new plans comes from the 5–9 size band.

This finding is consistent with the qualitative evidence collected from independent sources. Gusto's Colorado analysis identifies the 5–9 employee band as the largest source of mandate-induced 401(k) adoption. Provider commentary from Guideline, Human Interest, ForUsAll, and Vestwell consistently identifies small-firm mandate-deadline pressure as the proximate driver of new 401(k) plan formation. A 20-employee Bend, Oregon construction firm cited by Deschutes Investment Consulting and a Denver restaurant featured in the Colorado Treasurer's press release provide named firm-level examples of the choice between the state program and a private 401(k).

The substantive policy implication: the population that responds to state auto-IRA mandates by establishing private 401(k) plans is largely the small-employer population that the mandates are nominally designed to bring into the retirement system in the first place. Mandates appear to function as a forcing event that converts firms-without-plans into firms-with-private-plans, with the state program serving as the alternative for firms that prefer not to administer their own.

---

## Limitations and Open Questions

The analysis has four limitations worth stating directly:

**Mechanism is not decomposed.** The design identifies a policy effect but cannot distinguish among the several plausible mechanisms by which a mandate causes plan formation: firms preferring 401(k)s on the merits (employer matching, higher contribution limits), firms wanting to avoid administering payroll deductions to a state program, payroll providers steering firms toward 401(k) options at the moment of compliance, or some combination. Qualitative evidence from the project's source bank supports all three mechanisms operating simultaneously, but we do not test their relative magnitudes.

**Employee-side outcomes are not measured.** The outcome variable is plan formation, not participation, contribution, or retirement-security outcomes for the employees of mandate-affected firms. Whether mandate-induced 401(k) plans actually improve retirement security is a separate question that this dataset cannot address.

**Late-mandate states are preliminary.** Maine, Delaware, and New Jersey enacted mandates effective in 2024 and have material Form 5500 filing lag in the most recent data. The April 2026 DOL refresh shows late-mandate firm counts continuing to grow as filings catch up. Any conclusions specific to those three states should be treated as preliminary and revisited after one to two additional data refresh cycles.

**Firm-level external validation is partial.** State auto-IRA program exemption-filing counts substantially exceed our v3 firm counts in most states, but this reflects a definitional difference rather than a measurement discrepancy. State exemption counts include all employers offering any qualifying plan (including pre-mandate plans, 403(b)s, SEPs, defined benefit plans, and SIMPLE IRAs), while our dataset captures only firms whose first qualifying Form 5500 post-mandate is a new 401(k). The ratio between the two — ranging from approximately 1.4x in Maryland to roughly 9x in Colorado — itself reveals useful information about the size of the pre-existing private retirement plan stock by state, but it does not constitute direct firm-level validation. A targeted records request to the CalSavers program for firm-level exemption data was scoped but not pursued.

---

## Conclusion

State auto-IRA mandates cause meaningful private 401(k) plan formation among small employers. The headline causal estimate from a Callaway-Sant'Anna staggered difference-in-differences design is approximately 2.37 additional new 401(k) plans per 1,000 private establishments per year (roughly 7.83 per 1,000 mandate-eligible firms), robust across denominator specifications, robust to dropping the largest treated state, and corroborated by an independent natural experiment in Gusto's small-business administrative data that produces a +45 percent increase in 401(k) adoption among mandate-eligible Colorado firms.

The substantive finding is consistent with the firm-side "crowd-in" effect documented by Bloomfield, Goodman, Rao and Slavov, and provides firm-level identification with a cleaner research design than the aggregate analyses that have characterized the state-mandate retirement-policy literature to date. The policy-relevant population is small private employers, and the mechanism — though not fully decomposed — appears to involve mandate deadlines functioning as forcing events for firms to make a private-vs-state-program retirement plan decision, with a substantial share choosing the private route.

The dataset, methodology, and analysis files are maintained in a public repository to support replication and extension.

---

## Methodology Notes

**Aggregation choice.** The headline ATT is the cohort-weighted simple aggregation of group-time treatment effects (the `aggte(..., type = "simple")` output in R `did`). The equal-weight event-time aggregation produces a slightly higher number (2.66 under the conservative specification) but is more sensitive to single-cohort identification at long event-time horizons; the cohort-weighted simple aggregation is the more defensible headline.

**Denominator carry-forward.** SUSB data is published with approximately a two-year lag. SUSB values for 2023 and 2024 are carried forward from 2022 via standard interpolation. CBP has approximately one year of carry-forward (2024 from 2023). Because most identifying variation comes from pre-2023 cohort treatment effects, this asymmetry has minimal impact on the headline estimate.

**QCEW vs CBP unit definitions.** QCEW counts UI-covered worksites; CBP counts Business Register establishments. The two diverge for multi-establishment firms, with the gap widening over time as multi-establishment firms have grown as a share of the economy. Median QCEW/CBP ratio is 0.79; the ratio is statistically indistinguishable between mandate states and non-mandate states (Welch t = -1.11, p = 0.284), confirming the gap is methodological rather than driven by mandate-state-specific sectoral composition. The QCEW-based ATT is therefore approximately 33 percent lower than the CBP-based ATT for the same underlying causal effect.

**Mandate threshold uniformity.** The SUSB-5+ specification applies a uniform 5+ employee threshold across all mandate states. Most state mandates use a 5+ threshold (Connecticut, Illinois, Maryland, Colorado, Oregon-2023+), but California and Oregon-original extend to firms with 1+ employees and Virginia applies only to firms with 25+ employees. The 5+ threshold is the modal choice; per-state-threshold sensitivity is an open robustness check.

**Honest DiD bounds.** Long-horizon event-time aggregations are sensitive to plausible parallel-trends violations under Rambachan-Roth sensitivity analysis. This sensitivity is concentrated in noisy long-horizon coefficients identified by one or two cohorts (e.g., t=3 in v2-conservative, t=4 in v1-inclusive). The cohort-weighted simple aggregation, used as the headline, does not over-weight these noisy estimates and has substantially tighter sensitivity bounds.
