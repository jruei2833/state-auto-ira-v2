# Next-Step Recommendation

**Date:** 2026-04-29
**Decision requested from:** project owner
**Status (updated 2026-04-29):** project owner approved drafting; CPRA letter has been drafted at `deliverables/calsavers_cpra_request.md`. Awaiting send-off review (see send-off checklist at the bottom of the letter file). Letter has NOT been sent.

The project board has five candidate workstreams remaining from the original plan. This memo evaluates them and recommends the highest-value next action, with reasoning. The recommendation is for the project owner to confirm or override before any work begins.

## TL;DR

**Recommended next step: file the CalSavers CPRA exemption-filing request.**

It is the only remaining candidate that produces *new evidence* rather than synthesizing existing evidence. CA is ~70% of the v3 dataset, and the CalSavers exemption-filing data is an *independent measurement* of the same underlying population — firms that have a private retirement plan and therefore claim exemption from CalSavers. Either the two datasets agree (validating v3) or they diverge (a major finding either way). Marginal effort: drafting and sending one CPRA request letter. Wait time: 2-8 weeks for agency response. High leverage, low immediate effort.

## Candidates evaluated

The five candidate workstreams from the original plan:

### 1. Expand qualitative evidence to 25-50 entries (Sprint 2 target)

**Effort:** medium (5-15 hours of search and write-up per batch of ~10)
**Value:** medium-high (mechanism inference is *only* available through this workstream; DiD identifies effect, not mechanism)
**Risk:** low

Current batch is California/Oregon-heavy. Additional coverage needed for CT, MD, CO, VA, ME, DE, NJ. Without these the qualitative bank is regionally biased, which weakens any cross-state claim about why mandate-induced firms chose private 401(k)s instead of the state program.

**Why not first:** This is incremental. The existing 10 entries (Guideline + Gusto independent corroboration) probably establishes the headline mechanism story; doubling the entry count refines but doesn't transform the picture.

### 2. CalSavers CPRA exemption-filing request

**Effort:** very low (one letter; ~1-2 hours of drafting)
**Value:** very high (independent state-administrative crosscheck on ~70% of dataset)
**Risk:** low (CPRA can deny or require fee, but the request itself is no-cost)
**Wait time:** 2-8 weeks for the agency to respond

CalSavers is required by California law to track exemption claims by employers. An employer in CA who has its own qualified retirement plan files an exemption — this is an administrative act. The list of exemption-filed employers is a public record subject to CPRA disclosure. **This is exactly the same population as the California portion of our v3 dataset (firms with post-mandate 401(k)s).**

The matching is not perfect:
- CalSavers exemption filings include employers who established their plan *before* the mandate as well as after; need to filter by plan-creation date
- Some firms in our dataset may not yet have filed for exemption (administrative lag)
- Our dataset captures plans by EIN; CalSavers may use a different identifier

But the cross-validation potential is huge:
- **If the CalSavers list and our v3 dataset agree at 90%+ overlap:** v3's CA count of 72,972 is independently corroborated by state administrative data. This is the strongest possible validation short of firm surveys.
- **If they disagree:** that's the most important finding the project could surface. Either we're missing firms (the v3 dataset is undercounting), they're missing firms (CalSavers exemption administration has gaps), or both populations are real but different in some way that needs explaining.

**Why this is the highest-value next step:** every other workstream extends or interprets existing evidence. This one tests whether existing evidence is correct, against an independent source. If the project ever gets challenged on its central count claim, the CalSavers CPRA result is the bulletproofing.

### 3. Census CBP 2024 release watch + DiD re-run

**Effort:** low when it triggers (auto-rerun); zero otherwise
**Value:** low-medium
**Risk:** none
**Wait time:** Census CBP 2024 expected mid-late 2026

Currently the DiD denominator for 2024 is carried forward from 2023. Replacing it with actual 2024 establishment counts would change rates by 1-2% (CBP grows roughly that much year-over-year), which is well within current confidence intervals. The headline ATT direction will not change.

**Why not first:** passive (waiting on Census). Worth doing when the data drops, not before.

### 4. Re-run DiD on Apr-2026 refreshed panel

**Effort:** low (pipeline already built; ~30 min runtime + interpretation)
**Value:** low-medium
**Risk:** none

The April 2026 DOL refresh added +400 firms in v2-conservative (+0.38%), with late-treatment states growing the most (NJ +6.3%). Re-running the DiD on the refreshed panel:
- The headline simple ATT (cohort-weighted) probably moves <0.1 — too small to materially change conclusions
- The 2024 cohort effect (currently 3.19 with wide CI [0.08, 6.29] in v2) likely tightens because NJ now has more post-treatment data

**Why not first:** the refresh delta report (`methodology/dol_refresh_delta_2026_04.md`) gives enough of a preview to know the headline doesn't move. Re-running is a defensible refresh of secondary results, not a value-add against the CPRA request.

### 5. Final report synthesis per Section 9 of the workplan

**Effort:** high (the eventual deliverable; a 30-50 page report)
**Value:** high (the eventual deliverable, by definition)
**Risk:** medium — premature

The final report has to happen eventually. But:

1. **Honest DiD bounds just showed the headline result has fragility issues that should be examined more deeply.** The fragility comes from one noisy event-time horizon (t=4) — fixing that (e.g., by re-weighting or restricting the event window) would tighten the bounds and make the report's central claim more defensible. Best to do that before locking in a final write-up.
2. **Qualitative evidence is still being built up.** The mechanism story relies on this; finalizing the report before Sprint 2 (25-50 entries with cross-state coverage) means the mechanism section is necessarily thin.
3. **The CalSavers CPRA result, if pursued, would land in a final report as a major validation chapter.** Pursuing it now and waiting for the response gives ~6-12 weeks during which other workstreams can run in parallel, then the report integrates everything.

**Why not first:** premature. Better to harden the analytical foundation and gather one more piece of evidence (CPRA) before locking in a synthesis.

### 6. (Implied) Pull firm-level + DiD into unified narrative for final paper

**Effort:** medium
**Value:** medium
**Risk:** low

This is essentially editing the existing memos into a continuous narrative. Useful when the final paper is being drafted, but until the analysis is locked in (see #5), unifying them is busy work.

**Why not first:** secondary to having the analysis locked.

## Recommended sequence

1. **Now:** Draft and send the CalSavers CPRA request letter. (~2 hours of work; agency response in 2-8 weeks.)
2. **In parallel during the CPRA wait:** Sprint 2 of qualitative evidence — expand to 25-50 entries with CT/MD/CO/VA/ME/DE/NJ coverage.
3. **In parallel:** investigate the t=4 noise issue in the DiD event study — restrict event window or re-weight to tighten honest bounds.
4. **When CPRA returns:** integrate the validation result. Either chapter-1-of-final-report celebrating cross-source agreement, or a disclosed discrepancy memo investigating divergence.
5. **When Census CBP 2024 drops:** auto-rerun DiD with refreshed denominator.
6. **Final report synthesis:** after CPRA + Sprint 2 + Census refresh.

## What I need from the project owner to start

- **Approval to draft the CPRA request letter.** Suggested addressee: California State Treasurer's Office, CalSavers Retirement Savings Investment Board (the program's governing board). The letter should request: (a) the list of employers who have filed CalSavers exemption claims, (b) date of each exemption filing, (c) the basis claimed for exemption (i.e., presence of a qualified plan), and (d) any standard identifiers (EIN, FEIN, business legal name) sufficient to cross-match to the project dataset.
- **Confirmation of the requesting party.** AFPI is the project sponsor; the CPRA request would presumably be filed under AFPI's name. Confirming the right entity name and a contact for return correspondence will avoid back-and-forth.
- **Decision on parallel work during the wait.** Whether to also start Sprint 2 of qualitative evidence and/or the t=4 noise investigation while the CPRA is in flight, or sequence them.

I am explicitly NOT starting the request letter without this confirmation, per the prompt instruction "bring back to me before doing." Awaiting decision.

---

## Update — 2026-04-29: letter drafted

The project owner approved drafting. The CPRA request letter is at [`deliverables/calsavers_cpra_request.md`](calsavers_cpra_request.md) (markdown source) and [`deliverables/calsavers_cpra_request.docx`](calsavers_cpra_request.docx) (derived; regenerate via `make cpra-letter` or `python scripts/build_doc.py deliverables/calsavers_cpra_request.md deliverables/calsavers_cpra_request.docx`).

The letter is **drafted and saved, but has NOT been sent.** Per the send-off checklist at the end of the letter file, the project owner should:

1. Confirm the AFPI letterhead address and main phone number against current institutional standards (drafted from the public AFPI website).
2. Confirm the signatory (Janyjor or someone else with formal records-request authority).
3. Email a PDF/Word copy to `CalSavers@sto.ca.gov` with subject "CPRA Request — CalSavers Exemption-Filing Records".
4. Optionally CC AFPI legal/communications.
5. Optionally mail a paper copy to P.O. Box 942809, Sacramento, CA 94209-0001.
6. Log the send date and calendar reminders (14-day acknowledgment; 60-day production).

Outstanding decisions for the project owner (not blocking the send):

- **Sprint 2 of qualitative evidence (CT/MD/CO/VA/ME/DE/NJ coverage):** start in parallel during the CPRA wait, or sequence after?
- **t=4 noise investigation in the DiD event study:** start in parallel, or wait for CPRA result?
- **Census CBP 2024 release watch:** passive — no decision needed; will be triggered when Census releases.
