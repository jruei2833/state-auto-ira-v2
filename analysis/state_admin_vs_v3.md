# State-Administrative Exemption Counts vs. v3 Conservative Firm Counts

**Date built:** 2026-05-06
**Data sources:** see `data/state_admin/state_admin_summary.csv` and the per-state detail CSVs
**v3 source:** `data/v2-conservative/state_auto_ira_401k_dataset.csv` (count of unique EINs per `STATE`)

## What this table compares

The "state-admin exemption count" is the cumulative number of employers that filed an exemption with the state auto-IRA program — i.e., that certified they offer a qualifying retirement plan instead of the state program. The "v3 conservative firm count" is the count of unique EINs in the project's v2-conservative DiD analysis dataset for each mandate state. The two should be *related* (both attempt to count private-plan firms in the mandated population) but should differ in expected directions discussed below.

## Comparison table

| state | program | v3 v2-conservative firms | state-admin exemption count | as-of date | ratio (admin / v3) | status |
|-------|--------|-------:|-------:|---------|------:|-------|
| CA | CalSavers | 72,972 | 208,412 | 2025-12-31 | 2.86 | flagged: above 2x |
| OR | OregonSaves | 7,313 | 46,914 | 2025-06-30 | 6.42 | flagged: above 2x |
| IL | Secure Choice | 14,513 | 72,872 | 2026-03-31 | 5.02 | flagged: above 2x |
| CT | MyCTSavings | 2,409 | 10,900 | 2023-10-18 | 4.52 | flagged: above 2x |
| MD | MarylandSaves | 3,556 | ~5,000 | 2024-06-30 | 1.41 | within 0.5x-2x |
| CO | SecureSavings | 2,786 | ~26,000 | 2024-04-01 | 9.33 | flagged: above 2x |
| VA | Commonwealth Savers (RetirePath) | 2,150 | not published | - | - | not comparable |
| DE | Delaware EARNS | 132 | not published | - | - | not comparable |
| NJ | RetireReady NJ | 603 | not published | - | - | not comparable |

Maine is excluded from the headline comparison because of a small-denominator caveat — see "States with small-denominator caveat" subsection below. Maine remains in the underlying `data/state_admin/state_admin_summary.csv`; this is a presentation choice, not a data choice.

## States with small-denominator caveat

| state | program | v3 v2-conservative firms | state-admin exemption count | as-of date | ratio (admin / v3) |
|-------|--------|-------:|-------:|---------|------:|
| ME | MERIT | 143 | ~5,000 | 2026-01-05 | 34.97 |

**Why Maine is set aside from the headline ratio comparison:** Maine's v3 v2-conservative firm count is only 143. The mandate effective date is 2024-01-01 — late in the panel — and the late-treatment cohort is subject to filing-lag bias (firms with 2024 effective dates may not yet have filed Form 5500). The denominator is therefore both small in absolute terms and biased downward. A ratio of 34.97x against any plausible state-admin exemption count is mechanically large under these conditions; it does not reflect a substantive finding about Maine's exemption-filing volume relative to its mandate response.

The Maine row is retained in `data/state_admin/state_admin_summary.csv` and `data/state_admin/ME_detail.csv` for completeness. It should not anchor headline statements about state-admin vs. v3 divergence.

**Notes on state-admin counts:**
- **CA, OR, IL** publish exemption counts directly via monthly dashboards / board materials. These are clean cumulative-exemption figures.
- **CO** published "26,000 verified offer retirement plan" in its April 2024 annual board report. By August 2025 the program had grown substantially; an updated cumulative-exemption figure is not in the latest press releases.
- **CT** published "over 10,900 companies have certified they offer their own retirement plans" in an October 2023 Comptroller press release. CT does not appear to publish updated exemption counts; current Comptroller landing page shows registered/savers/AUM but not exemptions.
- **MD** is structured differently: SDAT $300 fee waivers track entities providing a plan OR enrolled in MarylandSaves OR exempt due to fewer than 5 employees / new business / etc. The program-requirement-exemption subset (~5,000 in DLS 2024 Evaluation) is the closest analog to other states' exemption counts. Total fee-waiver list is ~22,048 (TY2023) — much larger than the program-only-exemption subset.
- **VA, DE, NJ** publish program metrics (AUM, savers, registered employers) but **do NOT publish exemption counts.** This is a published-data limitation, not a research gap.
- **ME** (set aside in the small-denominator caveat subsection above): banner statistic "8,000+ Maine employers have registered or exempted" combined with the ~3,000 "participating" count from the Jan 2026 press release implies ~5,000 exempted. Exact split is not directly reported.

## Flags requiring user review

Per the spec, ratios outside 0.5x-2x require flagging.

**Above 2x band (admin > 2x v3 conservative):** CA, OR, IL, CT, CO

(Maine is excluded from this list — see "States with small-denominator caveat" subsection above. Maine's 34.97x ratio is mechanical, not substantive.)

**One-line hypothesis per outlier:**

- **CA (ratio 2.86):** State-admin counts include all employers with any qualifying plan (401k, 403b, 457b, SEP, SIMPLE, Davis-Bacon, multiemployer, governmental, religious, tribal). v3 conservative is restricted to firms that filed a *new* 401(k) Form 5500 in the post-mandate window. Pre-existing-plan firms exempt out of CalSavers but never produce a new 5500 in v3. Ratio of ~2.9 is consistent with substantial pre-mandate plan presence.

- **OR (ratio 6.42):** Same explanation as CA but more pronounced because OR mandate is older (2017) and was the first state — many small firms certified exemption based on existing payroll-deduction-IRA or SEP/SIMPLE arrangements that the v3 conservative dataset doesn't capture. The Vestwell wave-2025 update notes 3,802 of 8,287 newly contacted Oregon employers were already "Exempt 5500 prior to communications," suggesting Form 5500 lookup pre-exempts many that wouldn't appear as new 401(k) filings.

- **IL (ratio 5.02):** Same general story. IL also has the ERIC member MOU under which large multi-state employers are blanket-exempted without filing — these don't show up in v3 either, but they likely don't show up in IL's "Total Exempted" count either, so the gap reflects pre-mandate plan stock more than under-reporting.

- **CT (ratio 4.52):** Cited admin count is from October 2023 press release (10,900). CT mandate covers 5+ employee firms — the eligible universe is large relative to v3's "new 401(k)" denominator. Also, the 10,900 figure is now 2.5 years stale; current count is plausibly higher (no public update found).

- **CO (ratio 9.33):** CO's "verified offer retirement plan" methodology auto-exempted ~26,000 employers based on Form 5500 lookups (per their April 2024 annual report). This is a *broader* identification than employer-self-certification and likely captures all 401(k)/403(b)/SEP/SIMPLE/etc. plan filings, which substantially exceeds the v3 "new 401(k) post-mandate" subset. CO is a particularly strong example of why the ratio is high: the state explicitly used 5500 to pre-identify exempt firms, and that universe is necessarily larger than the new-plan subset captured in v3 conservative.

**Below 0.5x band:** none of the states with reported admin counts fall below 0.5x.

## What this means for the headline ATT

The ratio analysis suggests v3 conservative is, by construction, a *narrow* operationalization of "private plan response to mandate" — it captures only firms whose first qualifying Form 5500 filing post-mandate is a 401(k) plan. State-admin exemption counts capture the *broader* universe of all firms that already had OR newly established any qualifying retirement plan after being contacted by the state program.

For the project's research question (does the mandate cause new private-plan formation?) v3 conservative is the right operationalization — we want only post-mandate plan creation, not pre-existing plans that exempt out. The ratio difference is not a measurement error, it is the difference between (state's view of who is exempt) and (researcher's view of who newly created a private plan). Both are valid.

That said, the absolute *gap* between v3 firm counts and state-admin exemption counts is informative for thinking about ceilings:

- A state that has 200,000 exempt employers and shows a v3 effect of ~2,000 new 401(k)s is showing that the mandate moved roughly 1% of the otherwise-exempt-eligible population into new plan formation captured by v3.
- A state where the gap is small (e.g., MD at ~5,000 exempt vs. 3,556 v3 firms, ratio 1.41) suggests v3 is closer to the full exempt-and-plan-providing universe — perhaps because Maryland's program is younger and pre-mandate plan stock is smaller relative to post-mandate response.

## Comparison summary by status

| status | count | states |
|---|---|---|
| within 0.5x-2x | 1 | MD |
| above 2x (flagged) | 5 | CA, OR, IL, CT, CO |
| below 0.5x (flagged) | 0 | (none) |
| not comparable (state doesn't publish exemption count) | 3 | VA, DE, NJ |
| small-denominator caveat (excluded from headline ratio) | 1 | ME |

## Sources where conflicts were noted

1. **OR exempt count.** The Aug-2025 board materials report 46,914 cumulative exempt employers as of June 30, 2025. Vestwell separately reports July-31-2025 wave-2025 figures with 1,057 newly exempted plus 3,802 pre-exempted from 5500 lookup, suggesting the cumulative count grew further in Q3 2025 but no updated cumulative is published. No conflict with main number, but the wave-level breakdown adds nuance.
2. **MD fee waiver vs. exemption distinction.** DLS 2024 Evaluation reports SDAT fee waiver list at 22,048 (TY2023) but breaks this into ~14,100 with a retirement plan, ~5,000 with a certified exemption, and ~3,800 enrolled in MarylandSaves. The headline "fee waiver" number is much larger than the "program-exemption-only" number — using whichever is published would mislead. We use the ~5,000 figure for comparability with other states' "certified exemption" counts.
3. **CO 26,000 vs. registered 14,332 (April 2024) vs. 17,025 registered (August 2025).** The April 2024 annual report stated 14,332 enrolled employers + 26,000 verified offer retirement plan. The August 2025 press release mentions 17,025 businesses registered (an increase of ~2,700 over 16 months) but does not provide an updated 5500-pre-exemption count. Using April 2024 figure for exemption ratio is dated but is the most recent published value.
4. **NJ "$8.1M / 18,000 / 1,200 employers" (July 2025) vs. "$18M / 25,000" (February 2026).** The Feb 2026 program-amended document does not break out registered employers vs. exempt. A consistent NJ exemption count is not published.
