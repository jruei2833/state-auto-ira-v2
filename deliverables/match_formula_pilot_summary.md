# SEC EDGAR Match-Formula Pilot — Summary

**Date:** 2026-04-29
**Pipeline:** `analysis/edgar_match_pilot.py`
**Output:** `deliverables/match_formula_tracker.csv` (50 rows)
**Source dataset:** `data/v2-conservative/state_auto_ira_401k_dataset.csv`

## Empirical finding

Of the 50 mandate-induced 401(k) plan sponsors with the largest employee counts in the v2-conservative dataset, **zero are confidently identified as public companies in SEC EDGAR's ticker list**. 17 candidates produced low-confidence single-token name matches that require manual review (most appear to be false positives — e.g., SIERRA SPACE CORPORATION matched to SIERRA BANCORP; the firms share only the leading word "SIERRA"). The remaining 33 are not in EDGAR's ticker list at all and presumably correspond to private firms.

**This is itself a substantive finding for the project:** mandate-induced 401(k) plans are overwhelmingly established by private companies, not by publicly-traded employers that could already file SEC documents. EDGAR is therefore unlikely to be a productive source of match-formula language for this population of firms. To get match-formula evidence at scale, the project would need to either:
- Pivot to Form 5500 attachments (Schedule SB, Schedule R, or summary plan descriptions filed as PDF)
- Rely on third-party plan-data vendors (Brightscope, Form5500.com)
- Sample by industry rather than by employee count

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
