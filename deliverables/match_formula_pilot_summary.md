# Match-Formula Pilot — Summary

**Date:** 2026-04-29 (updated 2026-04-29 with BrightScope assessment and pivot to industry benchmarks)
**Pipelines:** `analysis/edgar_match_pilot.py` (EDGAR pilot, original); benchmark reports under `analysis/benchmark_sources/` (industry-benchmark pivot)
**Outputs:** `deliverables/match_formula_tracker.csv` (50 rows from EDGAR pilot); `deliverables/match_formula_industry_benchmarks.md` (industry benchmarks)
**Source dataset:** `data/v2-conservative/state_auto_ira_401k_dataset.csv`

## Status

| Pilot phase | Source | Status | Decision |
|---|---|---|---|
| Phase 1 | SEC EDGAR | Run, **null** finding | EDGAR confirmed wrong source for this population |
| Phase 2 | BrightScope | Access investigated, **not accessible** | See `methodology/brightscope_access_assessment.md` |
| Phase 3 | Vanguard + PSCA + ICI/BrightScope (aggregate) | Delivered as benchmark substitute | See `deliverables/match_formula_industry_benchmarks.md` |

The deliverable for "match formula data" is now a two-source product: (1) the EDGAR tracker CSV captures the pilot's null finding for documentation; (2) the industry benchmarks markdown captures the aggregate context that substitutes for unobtainable firm-level data. Neither is firm-level data on the State Auto-IRA dataset specifically — the project does not yet have that, and getting it requires either parsing Form 5500 attachment PDFs or licensing an enterprise dataset, both out of scope for this pilot.

## Phase 1: EDGAR null finding

Of the 50 mandate-induced 401(k) plan sponsors with the largest employee counts in the v2-conservative dataset, **zero are confidently identified as public companies in SEC EDGAR's ticker list**. 17 candidates produced low-confidence single-token name matches that require manual review (most appear to be false positives — e.g., SIERRA SPACE CORPORATION matched to SIERRA BANCORP; the firms share only the leading word "SIERRA"). The remaining 33 are not in EDGAR's ticker list at all and presumably correspond to private firms.

**Substantive interpretation:** mandate-induced 401(k) plans are overwhelmingly established by private companies, not by publicly-traded employers that could already file SEC documents. This is consistent with the firm-level descriptive analysis (`analysis/firm_level_analysis.md`) finding that 62% of dataset firms are solo or micro (0-9 participants) and only 0.7% are large (250+ participants); public firms cluster in the latter group, and the latter group is too small a slice of the dataset to drive aggregate findings. **EDGAR is therefore not a productive source of match-formula language for this population.**

## Phase 2: BrightScope access investigation

Investigated 2026-04-29. Conclusion: **not accessible to this project**.

- BrightScope was acquired by ISS in 2016; legacy public site (brightscope.com/401k-rating/) returns HTTP 404
- Data now licensed only via ISS Market Intelligence's MarketPro Retirement product, sales-led enterprise contracts only
- No public API; no published pricing; no academic / research tier
- Even if licensed, redistribution restrictions would conflict with publishing firm-level match formulas in policy memos

Full memo: `methodology/brightscope_access_assessment.md`.

## Phase 3: Pivot to industry benchmarks

In place of firm-level data, the project now has aggregate match-formula benchmarks from three credible sources:

1. **Vanguard *How America Saves 2025*** — 2024 plan-year data on ~5M Vanguard recordkept participants. Most common formula: 50% on first 6% of pay (13% of plans). Average promised match: 4.6% of pay; median 4.0%.
2. **PSCA 68th Annual Survey of 401(k) Plans** — 2024 plan-year self-reports from 755 plans. 81.3% of plans offer a match; average employer contribution 4.8% of pay; 44.1% offer immediate vesting.
3. **ICI/BrightScope DC Plan Profile** — 2020 plan-year tabulations of ~65,000 large 401(k) plans (≥100 participants). Single most common simple-match formula: 50% on first 6% of pay (21.9% of large plans with simple matches).

Full benchmarks: `deliverables/match_formula_industry_benchmarks.md`.

**These are aggregate industry benchmarks, not firm-specific data.** They describe what match formulas look like in the broader 401(k) market — not the specific match formulas of the firms in the State Auto-IRA dataset, most of which are too small to appear in any of these source samples (all three skew toward larger plans). The benchmarks support claims about "what a typical employer 401(k) match looks like" but do **not** support claims like "mandate-induced firms offered richer matches than other small firms" or "X% of mandate-induced plans use safe-harbor designs." Those would require firm-specific data the project does not currently have.

## What we'd want next

The realistic path to firm-level match-formula data at scale, if the project chose to pursue it:

- **Form 5500 attachment PDFs.** Plan sponsors file Summary Plan Descriptions and other plan-document attachments alongside Form 5500. These are stored on EFAST2 and contain the formal match formula text. Parsing them at scale (~106k attachments) is itself a multi-week project but is the only free firm-level source.
- **Industry-stratified sampling.** Rather than sampling the 50 largest firms by employee count (which yielded 0 public firms), sample 25 firms per industry sector. Some industries (financial services, professional services, tech) have a much higher public-company share. This would still yield few public matches in absolute numbers but might produce a non-zero result for specific industries worth pulling out.
- **Form5500.com cross-reference.** Free public profile pages with some plan-design fields, but match formula is rarely captured at firm level there either.

## Pipeline behavior (validated)

The pipeline successfully extracted match-formula language when it found a real public-company filing:

> SIERRA BANCORP, 10-K (2026-02-27): "safe harbor; 100% match up to 2% of comp"

This was technically a false-positive name match (Sierra Space ≠ Sierra Bancorp) but it confirms the regex-based extraction logic works against actual SEC 10-K text. For genuine public-company candidates, the pipeline would correctly extract the formula.

## Ambiguous matches worth manual review

The 17 ambiguous matches that share at least one distinctive token between the Form 5500 sponsor name and a SEC ticker entry. Rough manual scan:

| Form 5500 firm | EDGAR candidate | Likely status |
|---|---|---|
| UPSTART NETWORK, INC. | UPSTART HOLDINGS, INC. (UPST) | **Plausibly correct** — Upstart Holdings is the public parent; Upstart Network may be a subsidiary entity |
| DELUXE MEDIA INC. | DELUXE CORP (DLX) | Uncertain — Deluxe Corp's subsidiaries include some media business but Deluxe Media is also a separate former entity |
| All others (15) | Various | Almost certainly false positives — Sierra/Sierra, Summit/Summit, Community/Community, Premier/Premier, etc. share only generic leading words |

The user should manually review the UPSTART case and possibly DELUXE; the rest can be safely dismissed.

## Tracker schema

(No formal schema in the workplan; the schema below was defined by the pipeline. If the workplan defines a different one, update `SCHEMA` in `analysis/edgar_match_pilot.py:339`.)

| Column | Description |
|---|---|
| search_index | Order in which the firm was processed (1-50) |
| ein | Firm EIN from v2-conservative |
| firm_name | Plan sponsor name from Form 5500 |
| normalized_name | Cleaned name used for EDGAR search |
| state | Firm state |
| employee_count | Plan participants from Form 5500 |
| plan_effective_date | Date plan was established |
| search_status | found / ambiguous / not_found / error |
| edgar_cik | SEC CIK (when matched) |
| edgar_company_name | Official SEC entity name |
| filing_form | 10-K, 10-K/A, 20-F, DEF 14A |
| filing_accession | SEC accession number |
| filing_date | Date of the filing |
| filing_doc_url | Direct URL to primary document |
| match_text_excerpt | 1,000-char excerpt around the 401(k) mention |
| match_formula_summary | Human-readable formula (e.g., "100% on first 3%, 50% on next 2%") |
| has_match | Boolean — match formula detected |
| has_safe_harbor | Boolean — "safe harbor" mentioned |
| has_profit_sharing | Boolean — profit-sharing component |
| has_discretionary | Boolean — discretionary contribution mentioned |
| search_query | The actual EDGAR query used |
| searched_at | ISO timestamp of search |
| notes | Errors, low-confidence flags, etc. |

## Selection methodology (also not in workplan, documented here)

Candidates are selected from `state_auto_ira_401k_dataset.csv` (v2-conservative) with these filters:

1. EMPLOYEE_COUNT ≥ 250 (covered participants — public companies are typically much larger, but using a lower bound to capture plausibly-public smaller firms)
2. FIRM_NAME contains a public-company hint token (INC, CORP, HOLDINGS, GROUP, INDUSTRIES, etc.)
3. FIRM_NAME does NOT contain a non-public token (PC, MD, DDS, DENTAL, LAW OFFICE, CHURCH, etc.)
4. Sorted by EMPLOYEE_COUNT descending
5. Top 50 retained

Adjust `SELECTION_FILTERS` block in the script (lines 75-88) if you want a different sample.

## Matching rules

EDGAR matching uses a two-step pipeline:

1. **Ticker-list match** — download SEC's `company_tickers.json` (~12,000 active public companies); fuzzy-match candidate name to ticker entries with these strict rules:
    - Tokenize names; drop stop words (HOLDINGS, GROUP, MANAGEMENT, etc. — full list at `analysis/edgar_match_pilot.py:55`)
    - Require the FIRST distinctive token of both names to match
    - **High-confidence "found"**: ≥2 distinctive tokens shared
    - **Low-confidence "ambiguous"**: only 1 distinctive token shared (often a false positive — manual review recommended)

2. **Full-text fallback** — if the ticker list has no candidate at all, hit EDGAR's full-text search with the quoted firm name. Used for firms that may have filed 10-Ks under a different parent name. (In practice this rarely produces good matches and is mostly used to detect "really not in EDGAR.")

## Next steps if expanding this pilot

- **Manually verify UPSTART NETWORK / UPSTART HOLDINGS**, then add to a curated whitelist that bypasses the strict matcher
- **Sample by industry** rather than by size — financial services and tech firms in the dataset are more likely public than restaurant or labor-staffing firms
- **Consider Form 5500 attachments** (5500-SF doesn't have schedules, but full Form 5500 attaches Schedule SB / R; also some firms file Summary Plan Descriptions as PDF) for non-public firms
- **Brightscope / Form5500.com cross-reference** for paid plan-design data that doesn't depend on SEC filings
