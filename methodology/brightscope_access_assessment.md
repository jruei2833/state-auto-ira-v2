# BrightScope Data Accessibility Assessment

**Date:** 2026-04-29
**Question:** Can the State Auto-IRA project obtain firm-level 401(k) match-formula data from BrightScope?
**Decision:** No — BrightScope is enterprise-licensed only. Pivoting to industry benchmarks (Path B in the task brief).

## What BrightScope is now

BrightScope was an independent 401(k) plan rating service founded in 2007 that maintained public plan-profile pages and publishable plan ratings. It was acquired by [Institutional Shareholder Services (ISS) in 2016](https://www.issmarketintelligence.com/) and folded into ISS Market Intelligence. The brand still exists as the data engine behind the **MarketPro Retirement** product (sometimes labeled "powered by BrightScope"), but the consumer-facing brightscope.com site is gone.

## What is publicly accessible

| Path | Status | Notes |
|---|---|---|
| brightscope.com homepage | ❌ Returns 301 redirect to issmarketintelligence.com | Confirmed 2026-04-29 |
| brightscope.com/401k-rating/ (legacy plan-profile pages) | ❌ HTTP 404 | All public plan profiles taken down post-acquisition |
| brightscope.com/robots.txt | ❌ HTTP 404 | No public robots policy because no public site |
| Public BrightScope API | ❌ Does not exist | The original v1/v2 API was deprecated; no successor public endpoint |
| ISS MarketPro Retirement (paid) | Sales-led only | Per [ISS MI MarketPro page](https://www.issmarketintelligence.com/solutions/marketpro/marketpro-retirement-powered-by-brightscope/): no self-service signup, no posted pricing, no API documentation visible to non-customers |
| ICI/BrightScope Defined Contribution Plan Profile (annual report) | ✅ Free PDF | [Latest available 2023 publication](https://www.ici.org/system/files/2023-09/23-rpt-dcplan-profile-401k.pdf); aggregate statistics only, not firm-level |

## Terms-of-service review

ISS Market Intelligence's [terms-of-use page](https://www.issmarketintelligence.com/terms-of-use/) does not contain explicit prohibitions on web-scraping or automated access. This is unsurprising because the underlying data is gated behind authenticated enterprise accounts — there is no public dataset to scrape. The legacy brightscope.com domain that did host public plan-profile pages no longer serves them. Any attempt to harvest data from former URLs returns 404, so the access question is moot at the technical level.

The MarketPro product and its derivatives (which embed BrightScope data) are licensed under standard ISS Market Intelligence subscription terms that an enterprise customer signs at contract execution. Those terms are not visible to non-customers and would presumably restrict redistribution and automated access by anything other than the licensed user. **For the State Auto-IRA project, which has no enterprise relationship with ISS MI, no relevant ToS applies — there is simply no permitted access path.**

## Pricing/trial path

To confirm there is no researcher-friendly path I would have missed, I traced the contact-sales workflow:

- "Request a Demo" form on the MarketPro page leads to `info@issmarketintelligence.com` and `sales@issmarketintelligence.com`
- Sales hotline: +1.212.217.6884
- No published pricing tier; no academic-research discount mentioned anywhere on the public site
- No 30-day or 14-day free-trial path advertised

For a research project like this one, the realistic minimum cost to obtain BrightScope data is a multi-thousand-dollar enterprise license negotiated through their sales team, with redistribution restrictions that would prohibit publishing firm-level plan-design figures in a policy memo. Even if AFPI procured a license, the data-redistribution restrictions would limit how the project could cite it.

## Comparable third-party plan databases

For completeness, I checked alternative firm-level 401(k) plan databases:

| Source | Accessibility | Useful for our purpose? |
|---|---|---|
| Form5500.com (ASPPA) | Free public profile pages | Yes for some plan-design fields, but match formula is rarely captured at firm level — they pull from Form 5500 which doesn't have a structured match-formula field |
| Department of Labor Form 5500 raw filings | Free, already in use for this project | Match formulas are described in plan-document attachments (PDFs filed with Form 5500), not in the structured CSV exports. Parsing the attachments is itself a major project |
| EBSA Research Files | Free | Aggregate statistics only |
| 401kHelpCenter | Free | Editorial, not data |
| ICI/BrightScope DC Plan Profile | Free annual PDF | Aggregate statistics; useful for benchmarks not firm-level |
| PSCA Annual Survey | Paid (~$500-$1,000 for non-members) | Aggregate by plan-size strata; useful for benchmarks not firm-level |
| Vanguard "How America Saves" | Free PDF | Aggregate from Vanguard recordkept plans (~5M participants); useful for benchmarks |

None of the free options provide firm-level match-formula data at scale. The best paths for the State Auto-IRA project are therefore:

1. **For benchmarks:** PSCA Annual Survey + Vanguard "How America Saves" (Path B in the task brief — pursued)
2. **For firm-level (future work):** Parse Form 5500 attachments (PDFs containing summary plan descriptions), an undertaking that is out of scope for this pilot

## Decision

**Do not pursue BrightScope.** The data is not accessible without an enterprise license, and an enterprise license would impose redistribution restrictions that would conflict with the project's policy-memo deliverables. Pivot to industry benchmarks via Vanguard's "How America Saves 2025" (downloaded) and PSCA Annual Survey (cite from public summaries).

Output: `deliverables/match_formula_industry_benchmarks.md`.

## Confirmation log

Commands run on 2026-04-29 to verify the conclusions above:

```
curl -sI https://www.brightscope.com/             # → 301 → issmarketintelligence.com
curl -sI https://brightscope.com/401k-rating/     # → 404
curl -sI https://www.brightscope.com/robots.txt   # → 404
WebFetch  https://www.issmarketintelligence.com/solutions/marketpro/marketpro-retirement-powered-by-brightscope/
                                                   # → enterprise sales only, no API
WebFetch  https://www.issmarketintelligence.com/terms-of-use/
                                                   # → no scraping clause (moot since no public data)
```
