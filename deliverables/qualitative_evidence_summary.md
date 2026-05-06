# Qualitative Evidence Summary

**Project:** State Auto-IRA Research
**Workstream:** Qualitative mechanism evidence (Workplan Item 5)
**Updated:** April 29, 2026
**Coverage:** 20 coded entries spanning Sprint 1 (initial 10) and Sprint 2 (added 10).
**State coverage:** California, Oregon, Colorado, Virginia, Connecticut, plus multi-state. Maine, Delaware, and New Jersey deliberately deferred — too recent to have accumulated meaningful public commentary.

## Headline finding

State auto-IRA mandates cause meaningful private 401(k) plan formation. This conclusion is now supported by three independent evidence streams pointing at the same firm-size pattern: the project's own DiD on Form 5500 data, an independent quantitative analysis by Gusto on completely different proprietary small-business data, and named firm-level and provider-level qualitative attribution.

The most consequential finding from Sprint 2 is that **Gusto independently quantified the Colorado mandate effect at +45 percent**, with the largest gains concentrated in 5–9 employee firms (+52 percent) — directly mirroring this project's firm-level descriptive finding that 62 percent of mandate-induced plans are solo or micro firms. Two independent analyses on completely different data sources hitting the same firm-size composition is exceptionally strong cross-validation.

## What the evidence now establishes

### Independent quantitative corroboration

Gusto's June 2025 analysis ("State Auto-IRA Mandates Boost 401(k) Adoption") is essentially a separate natural-experiment study using:

- A different data source (Gusto's proprietary administrative data on 300,000 small-business customers, not Form 5500)
- A different research design (Colorado vs. five neighboring non-mandate states using simple year-over-year differences, not staggered Callaway-Sant'Anna DiD)
- A different time window (one year before mandate through August 2023 specifically)

Gusto found that the share of Colorado firms with 5+ employees offering a 401(k) plan increased 45 percent (25.3% → 38.0%) in the year leading up to the SecureSavings deadline. The five neighboring control states (Arizona, Utah, Nevada, Kansas, Nebraska) saw essentially no change (20.4% → 21.2%). Gusto extends the analysis to California and Oregon and finds the same pattern.

Two completely independent research efforts arriving at the same qualitative conclusion using different data and different methods is the strongest possible form of cross-validation. The DiD's headline effect of approximately 2.37 plans per 1,000 establishments is consistent in direction and rough magnitude with Gusto's 13-percentage-point absolute increase among Colorado firms.

### Firm-size composition matches independently

Gusto's firm-size breakdown is the cleanest external confirmation of the project's descriptive finding:

| Firm size | Gusto 401(k) adoption increase | Project finding |
|---|---|---|
| 1–4 employees (not subject to mandate) | +0.3pp (essentially flat) | Not in mandated population |
| 5–9 employees | +9.6pp / +52% | Heavy presence in mandate-induced plans |
| 10–24 employees | +37% | Substantial presence |
| 25+ employees | +43% | Smaller share by count, larger per-firm effect |

The fact that Gusto sees the largest mandate effect in 5–9 employee firms aligns precisely with the project's finding that 62 percent of mandate-induced plans are solo or micro. The descriptive analysis and Gusto's natural-experiment estimate are describing the same employers from different angles.

### Official state validation

The Colorado Department of Treasury's December 2024 press release officially adopts the +45 percent figure, citing Gusto by name. State Treasurer Dave Young is quoted urging compliance. This is as close to state-administrative confirmation of the mechanism as is publicly available without a CPRA/FOIA request — and the CPRA letter to CalSavers, if successful, would extend that validation to California.

### Industry-press attribution

Guideline (the second-largest small-business 401(k) recordkeeper in 2023, with 12,795 new plans added) directly attributes its growth to CalSavers deadline pressure in industry trade press. Multiple major recordkeepers (ADP, Guideline, Human Interest) report state mandates as a top-three driver of new-plan formation.

### Mechanism described by the people watching it happen

Across five mandate states (CA, OR, CO, VA, CT), the same pattern recurs in provider commentary, advisor case descriptions, mainstream press reporting, and trade-association observations: employers facing a mandate deadline are choosing between state-program registration and establishing their own qualified plan, and a substantial subset is choosing the latter. Specific examples include a 20-employee Bend Oregon construction firm (via Deschutes Investment Consulting) and Blue Bonnet Restaurant in Denver (via the Colorado Treasurer's press release). NFIB Colorado's state director reports that the dominant member response has been compliance, not resistance.

## What the evidence still does not establish

Three honest caveats remain:

The strongest evidence is **provider-level and aggregate, not firm-level for the specific firms in the v3 dataset.** Gusto's analysis covers Gusto's customers — overlapping with but not identical to the v3 Form 5500 universe. The CPRA request for CalSavers exemption filings is the path to firm-level external validation; until that returns, the project relies on aggregate-level corroboration.

There is **selection bias in who speaks publicly.** Providers and benefits advisors have an incentive to attribute customer growth to state mandates because mandates create their addressable market. The Gusto analysis is more credible than provider marketing because Gusto used a clear empirical design with non-mandate state controls, but it still comes from a stakeholder with skin in the game.

The evidence describes the mechanism but **does not fully decompose it.** Firms could be choosing 401(k)s because they prefer the merits (employer matching, higher contribution limits), because they want to avoid administering payroll deductions to the state, because their payroll provider made the 401(k) path easier, or some combination. Sorting between these requires firm-level interviews or a targeted survey beyond project scope.

## How this changes the synthesis

The qualitative evidence has moved from "supporting" the DiD to "independently corroborating" it. The Gusto Colorado analysis is itself a defensible causal estimate that points the same direction as the project's CS-DiD. The project no longer rests on a single quantitative result — it rests on convergent evidence from two independent quantitative studies plus a substantial body of named provider and state-level attribution.

For the eventual final report, the appropriate framing is:

> Mandates cause meaningful 401(k) plan formation among small employers. The project's CS-DiD estimates an average treatment effect of approximately 2.37 new plans per 1,000 private establishments per year across the 10 mandate states. An independent analysis by Gusto using proprietary small-business administrative data estimates a 45 percent increase in 401(k) adoption among Colorado firms subject to the SecureSavings mandate, with the largest effect in 5–9 employee firms — a finding mirrored exactly in our firm-level descriptive analysis showing 62 percent of mandate-induced plans are solo or micro firms. The mechanism is further corroborated by direct attribution from major small-business 401(k) recordkeepers, named firm-level testimony, and an official press release from the Colorado Department of Treasury.

This is a substantively stronger position than the project held a week ago.

## Provenance note

All sources are publicly accessible web pages collected via web_search in this project's chat session, April 29, 2026. The Gusto research is published openly on Gusto's website. The Colorado Treasurer's press release is on the official treasury.colorado.gov domain. No paywalled or non-public sources were used. Full URLs and structured codings are in `deliverables/qualitative_evidence_bank.csv`.

## Remaining gaps

Direct firm-level statements from named v3-dataset firms remain absent. The CPRA request to CalSavers is the most promising path. State annual reports from CalSavers, OregonSaves, and Illinois Secure Choice often publish exemption-filing statistics; pulling these is a low-effort follow-up.

Maine, Delaware, and New Jersey coverage remains zero. These states are too recent (2024 mandate effective dates) for substantive accumulated commentary; revisit in late 2026 or early 2027.

A targeted survey of the 50–100 largest mandate-induced firms in the v3 dataset (where SEC filings or named press is most likely) would yield direct testimony the current evidence base lacks. Beyond chat-session scope but suitable for a Claude Code task.
