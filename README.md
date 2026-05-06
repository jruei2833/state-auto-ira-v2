# State Auto-IRA Research

A firm-level analysis of private 401(k) plan formation in response to state auto-IRA mandates.

## Headline Finding

**State auto-IRA mandates cause approximately 2.37 additional new 401(k) plans per 1,000 private establishments per year, robust across multiple denominator specifications.** The result is corroborated by an independent natural experiment in Gusto's small-business administrative data showing a 45 percent increase in 401(k) adoption among Colorado firms subject to the SecureSavings mandate.

## Canonical Deliverable

The full project results memo is in [`deliverables/project_results_memo.md`](deliverables/project_results_memo.md). The formatted version is at [`deliverables/project_results_memo.docx`](deliverables/project_results_memo.docx).

## Project Context

This work extends the firm-side "crowd-in" effect documented by Bloomfield, Goodman, Rao and Slavov (NBER) by providing firm-level identification, a Callaway-Sant'Anna staggered difference-in-differences research design, and external corroboration. The dataset uses Department of Labor Form 5500 filings to identify approximately 106,577 firms across the ten states with active auto-IRA mandates that established new 401(k) plans after their state's mandate took effect, with the analysis covering 2017–2024.

## Repository Structure

```
deliverables/   project deliverables (memo, evidence bank, status updates)
analysis/       DiD outputs, robustness tables, firm-level analysis, Honest bounds
methodology/    design memos, planning specs, source provenance
data/           dataset versions (v1-inclusive, v2-conservative) plus
                external denominators (BLS QCEW, Census SUSB) and state-admin data
archive/        superseded earlier-version files (validation/, scripts/)
build_both.py   end-to-end build script (April 2026 refresh)
scripts/        docx-generation script for derived deliverables
Makefile        targets to regenerate derived docx artifacts
```

## Quick Navigation

| What | Where |
|---|---|
| Headline ATT (cohort-weighted simple) | [`analysis/did_results_v2_conservative.csv`](analysis/did_results_v2_conservative.csv) |
| Robustness (drop-CA, drop-late, ESRP, with-employees) | [`analysis/did_robustness_v2_conservative.csv`](analysis/did_robustness_v2_conservative.csv) |
| Three-denominator sensitivity (CBP/QCEW/SUSB) | [`analysis/did_denominator_sensitivity.md`](analysis/did_denominator_sensitivity.md) |
| Honest DiD bounds (Rambachan-Roth) | [`analysis/did_honest_bounds.md`](analysis/did_honest_bounds.md) |
| DiD design memo | [`methodology/did_design_memo.md`](methodology/did_design_memo.md) |
| Aggregation choice writeup | [`analysis/did_aggregation_comparison.md`](analysis/did_aggregation_comparison.md) |
| External validation (qualitative evidence) | [`deliverables/qualitative_evidence_summary.md`](deliverables/qualitative_evidence_summary.md) |
| Source provenance | [`methodology/source_provenance_log.csv`](methodology/source_provenance_log.csv) |
| Pre-memo verification (year-range, ratio checks) | [`methodology/pre_memo_verification.md`](methodology/pre_memo_verification.md) |

## Reproducibility

All DiD analyses are cross-validated between Python's `differences` package and R's `did` package; results agree to four decimal places. The estimator is the Callaway-Sant'Anna group-time average treatment effect (ATT(g,t)) with not-yet-treated states as the primary comparison group. Source provenance for the Form 5500 raw files is documented in [`methodology/source_provenance_log.csv`](methodology/source_provenance_log.csv); QCEW, SUSB, and state-administrative source provenance are recorded in the same log.

The Form 5500 raw files (~6 GB) are not committed; they are downloaded from the DOL EFAST2 system. Build steps:

1. Download Form 5500, Form 5500-SF, and Schedules H/I/R for 2017–2025 to `form5500-raw-data/` (gitignored).
2. Run `python build_both.py` to produce both `data/v1-inclusive/` and `data/v2-conservative/` datasets.
3. Run the analysis scripts in `analysis/` (`build_state_year_panel.py`, `fetch_cbp.py`, `build_did_panels.py`, `run_did.py`).

## Data Refresh

Last DOL Form 5500 data refresh: April 2026 (covers filings through 2024 plus partial 2025).
