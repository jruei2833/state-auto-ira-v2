# Count Reconciliation Memo

**Project:** State Auto-IRA Research
**Dataset:** v3 (final, validated)
**Date:** April 27, 2026

## Headline

The v3 dataset reports two firm counts, both produced by the same final pipeline (`build_dataset.py`) against the same source data (DOL Form 5500 bulk filings, 2017–2024). The two numbers reflect a deliberate analytical choice about how to define "after the mandate," not a data quality issue or version-to-version drift.

| Definition | Firm count | Mandate date used |
|---|---|---|
| v1-inclusive | 115,690 | Date legislation/final regulation was enacted |
| v2-conservative | 106,577 | Date the state auto-IRA program actually launched |

The 9,113-firm gap between the two definitions is concentrated almost entirely in California (8,540 firms, ~94% of the gap), where roughly four years separated the 2018 enabling regulation from the 2019 CalSavers statewide rollout. The remaining 573 firms are spread mostly across Illinois (280), New Jersey (213), and Delaware (83). In states with shorter legislation-to-launch windows (typically 12–24 months), the two definitions produce very similar counts.

## Why two numbers

Each definition answers a slightly different policy question.

The **inclusive figure (115,690)** is appropriate when the mechanism of interest is *anticipation*: once a state has passed an auto-IRA law, employers can begin establishing private 401(k) plans in advance of the program's actual launch in order to be in compliance from day one. This captures the broader policy effect.

The **conservative figure (106,577)** is appropriate when the mechanism of interest is *operational pressure*: firms are responding to the actual existence of a state-facilitated alternative they would otherwise need to enroll in. This is the narrower causal story and most closely matches the framing in Bloomfield, Goodman, Rao & Slavov.

For headline reporting we recommend the conservative figure (106,577), with the inclusive figure presented alongside as a robustness check.

## Why earlier intermediate counts are not reported

During development the project produced several intermediate counts as different tools (Google Antigravity, Claude Code, Codex) were used to build and cross-check the dataset. Those intermediate counts are no longer the subject of analysis. The v3 build supersedes them, and Claude Code and Codex independently produced state-by-state firm counts that agree at 100% across all 10 mandate states. The v3 figures are validated and final.

This means the relevant variation in firm counts going forward is not temporal (which version was run when) but definitional (which mandate-date rule applies). That is the reconciliation that matters for the analysis.

## Source tracking going forward

DOL refreshes its Form 5500 bulk datasets monthly and has now begun posting partial 2025 files. To make any future count change cleanly attributable, every dataset build from v3 forward is accompanied by a source provenance log (`methodology/source_provenance_log.csv`) that records, per filing year and per source file: pull date, source URL, raw row count, row counts after each filter stage, and final unique-EIN count.

This means that any future change in firm count can be classified into one of three causes:

1. **New DOL data**: filings posted to the bulk datasets since the prior build, including monthly DOL refreshes and any 2024–2025 filings catching up to filing-lag states (ME, DE, NJ).
2. **Filter or pipeline changes**: any modification to the filtering logic in `build_dataset.py`, recorded in version control.
3. **Mandate-date definition change**: the inclusive/conservative choice described above.

No count change should be attributable to unspecified pipeline drift.

## Validation summary

| Check | Result |
|---|---|
| Claude Code vs Codex, state-by-state firm counts | 100% agreement across 10 states |
| Plan effective dates fall after applicable mandate date | Pass |
| EIN format and sponsor-name handling | Pass |
| Pension code 2J (401(k)) filter applied consistently | Pass |
| Single-employer entity filter applied consistently | Pass |
