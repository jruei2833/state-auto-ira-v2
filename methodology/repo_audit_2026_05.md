# Repo Audit — Pre-Stakeholder Readability

**Date:** 2026-05-06
**Purpose:** Report current repo state ahead of cleanup. Read-only — no files touched. Cleanup decisions in a follow-up.

Headline summary up front, then eight sections. The repo has *substantively* strong content (DiD, qualitative evidence, three-denominator sensitivity, Honest bounds) but the front-door experience is stale and there is meaningful dev clutter.

**Top three things a stakeholder will trip over:**
1. **README still describes only the v3 firm dataset and lists DiD as a "next step"** — the DiD has been done and refined for a week, plus qualitative bank, plus denominator sensitivity. The README hasn't been touched since 2026-02-15.
2. **Empty zero-byte file named `git` at repo root** — accidental artifact, looks unprofessional on the GitHub front page.
3. **183 MB of raw QCEW CSVs and 25 MB of raw SUSB xlsx files committed** in `data/bls_qcew/raw/` and `data/census_susb/raw/` — these are bulk downloads that should be regenerable, not committed.

---

## Section 1: Top-level layout

```
.gitignore                  Apr 29  417 B
Makefile                    Apr 29  1.2 KB
README.md                   Feb 15  9.4 KB   ← stale
analysis/                            ↓
build_both.py               Feb 15  12 KB
build_both_2026_04.py       Apr 29  12 KB
build_dataset.py            Feb 15  14 KB
data/                                ↓
deliverables/                        ↓
form5500-raw-data/          Apr 29  (gitignored — bulk Form 5500 downloads)
git                         Feb 15  0 B      ← FLAG: empty zero-byte file
methodology/                         ↓
scripts/                             ↓
search.html                 Feb 15  34 KB    ← FLAG: orphan from initial exploration?
validation/                          ↓
```

Flags:
- **`git` (0 bytes)** at root — clearly an accidental file (someone probably typed `git` instead of `git status` and stdout went into a file).
- **`search.html` (34 KB, Feb 15)** — one-off artifact from initial work, no apparent reference from anything current. Likely safe to remove.
- **Three top-level build scripts (`build_both.py`, `build_both_2026_04.py`, `build_dataset.py`)** — overlapping functionality. `build_both.py` is probably superseded by `build_both_2026_04.py`. `build_dataset.py` (single-version) is referenced by README but appears unused since v1/v2 split.
- **`scripts/` directory** holds only `build_doc.py` (a docx builder). One-file dir with a generic name — easy to miss.
- **`validation/` directory** holds Feb 15 cross-validation work between Antigravity, Codex, and Claude Code. Pre-DiD era; not referenced by any current writeup.
- **`form5500-raw-data/`** is gitignored (correctly), but its presence in the working tree is fine — flagged here only because it's a name a stakeholder might wonder about.

Untracked at root: none. Working tree clean for tracked files; untracked items are listed under Section 4.

---

## Section 2: README state

**Last meaningful README commit:** `3185e4e` "Update README with research context" — **Feb 15, 2026** (~3 months stale).
Subsequent README touches: none.

**What the README currently describes:**
- The research question (firms choosing 401(k) vs. state auto-IRA)
- The v3 firm-level dataset (115,690 / 106,577 firms)
- v1 vs v2 mandate-date methodology
- State-by-state firm counts
- Repository structure (which is **out of date** — it doesn't mention `analysis/`, `deliverables/` enumeration, or `methodology/` content beyond two files)
- Validation chain (Antigravity / Claude / Codex audits) — Feb 15 era
- Known limitations
- "Recommended next steps" — explicitly lists "Difference-in-differences" as a *future* step

**What the README does NOT mention** (despite all of these being committed and current):
- The Callaway-Sant'Anna DiD pipeline (`analysis/run_did.py`, results from 2026-04-29) — the ~2.4 per 1k headline finding
- Honest DiD bounds (`analysis/did_honest_bounds.md`)
- The qualitative evidence bank (20 entries, committed today)
- The three-denominator sensitivity (CBP/QCEW/SUSB) committed today
- The state-administrative comparison work
- The CalSavers CPRA letter draft (deferred per the project owner, but still part of the repo)
- The stakeholder status update (`deliverables/stakeholder_status_update.md`)

**Does it tell a stakeholder where to look first?** Sort of, but to the wrong place. The README points to `data/v1-inclusive/state_auto_ira_401k_dataset.csv` as the headline output. For a stakeholder landing here today, the headline output should arguably be `analysis/did_results.md` or `deliverables/stakeholder_status_update.md`. The "Recommended next steps" section actively misleads by listing already-completed work as future work.

---

## Section 3: Deliverables directory contents

`ls -la deliverables/` — 14 files (excluding `.gitkeep`).

| File | Size | Last commit | Description | Status |
|---|---:|---|---|---|
| FINAL_SUMMARY.md | 532 B | 2026-02-15 | One-paragraph summary of the v3 firm dataset | **superseded** — predates everything since DiD |
| State_AutoIRA_Project_Report.md | 8.7 KB | 2026-02-15 | First project writeup, v3-dataset focused | **superseded** |
| summary_statistics.csv | 549 B | 2026-02-15 | Per-state firm counts | superseded — same content available in state_admin_summary etc. |
| calsavers_cpra_request.md | 7.4 KB | 2026-04-29 | Draft CPRA exemption-filing request to CalSavers | **on hold** by project owner (still in repo) |
| calsavers_cpra_request.docx | 15 KB | 2026-04-29 | docx version of above (gitignored — built by `make`) | derived |
| count_reconciliation_memo.md | 4.2 KB | 2026-04-29 | Memo on per-state count differences | active reference |
| match_formula_industry_benchmarks.md | 9.9 KB | 2026-04-29 | Industry benchmark match formulas (post-BrightScope pivot) | canonical |
| match_formula_pilot_summary.md | 11 KB | 2026-04-29 | Match formula pilot writeup | canonical |
| match_formula_tracker.csv | 15 KB | 2026-04-29 | Tracker of match formulas pulled | active reference |
| next_step_recommendation.md | 11 KB | 2026-04-29 | Recommendation to send CPRA letter (which is now on hold) | **stale** — recommendation paused |
| qualitative_evidence_bank.csv | 14 KB | 2026-05-06 | 20-entry qualitative evidence bank | **canonical** — committed today |
| qualitative_evidence_summary.md | 9.0 KB | 2026-05-06 | Synthesis writeup with Gusto +45% headline | **canonical** — committed today |
| stakeholder_status_update.docx | 20 KB | 2026-04-29 | docx version (gitignored) | derived |
| stakeholder_status_update.md | 17 KB | 2026-04-29 | Living stakeholder status doc | **canonical** |

Specific checks:
- Multiple versions of the same document: `FINAL_SUMMARY.md` and `State_AutoIRA_Project_Report.md` (Feb era) coexist with `stakeholder_status_update.md` (Apr era). The Feb files are conceptually superseded; they should either be archived or marked as historical.
- Markdown sources without docx: most are markdown-only. The two with docx (`stakeholder_status_update`, `calsavers_cpra_request`) have the docx gitignored — that's intentional per `.gitignore` ("derived artifacts").
- Files referenced in the project results memo: the memo isn't yet drafted, but the relevant deliverables (qualitative bank/summary, stakeholder update, count reconciliation, match formula docs) are all here.
- Qualitative evidence files committed today: **both present** (`qualitative_evidence_bank.csv`, `qualitative_evidence_summary.md`).
- `.gitkeep` is the original directory placeholder — no longer needed but harmless.

---

## Section 4: Analysis directory contents

`ls -la analysis/` — 60 tracked files + 1 untracked dir (`__pycache__/`) + 3 untracked logs.

**Breakdown by type:**

| Type | Count | Notes |
|---|---:|---|
| .py | 14 | DiD runners, data fetchers, build scripts |
| .R | 2 | Honest DiD bounds (`did_honest_bounds.R`), R-side validation (`did_r_validation.R`) |
| .csv | 26 | DiD results, robustness, panels, cohort effects, ratios |
| .md | 9 | Writeups (results, denominator sensitivity, comparisons) |
| .png | 3 | Event-study plots (v1, v2, honest bounds) |
| .log | 6 tracked + 3 untracked | Run logs |
| Subdirs | 3 | `__pycache__/` (untracked), `benchmark_sources/`, `tables/` |

**Files referenced in the project results memo's claims** (all present):
- DiD results: `did_results.md`, `did_results_v1_inclusive.csv`, `did_results_v2_conservative.csv` ✓
- Robustness: `did_robustness_v1_inclusive.csv`, `did_robustness_v2_conservative.csv` ✓
- Cohort effects: `did_cohort_effects_v{1,2}.csv` ✓
- Event study: `did_event_study_v{1,2}.{csv,png}` ✓
- Honest bounds: `did_honest_bounds.{md,R,log,csv,png}` ✓
- R cross-validation: `did_r_validation.{md,R,log}` and `did_r_*_v2_conservative.csv` ✓
- Three-denominator sensitivity: `did_denominator_sensitivity.md`, `did_results_susb_*.csv`, `did_results_qcew_*.csv` ✓
- QCEW vs CBP: `qcew_vs_cbp_levels.md`, `qcew_vs_cbp_state_year_ratios.csv` ✓
- SUSB vs CBP: `susb_vs_cbp_sensitivity.md` ✓
- State admin vs v3: `state_admin_vs_v3.md` ✓
- Aggregation choice: `did_aggregation_comparison.md` ✓ (committed today)
- Firm-level: `firm_level_analysis.{md,py}`, `firm_level_analysis_susb.py`, `firm_level_analysis_susb_normalized.md` ✓
- EDGAR pilot: `edgar_match_pilot.py`, `edgar_search.log` ✓ (a closed-out pilot)

**Dev clutter:**
- `__pycache__/run_did.cpython-314.pyc` — untracked, not in `.gitignore`. Should be ignored.
- 9 `.log` files in `analysis/` — `build_both_2026_04.log`, `build_panel.log`, `did_honest_bounds.log`, `did_r_validation.log`, `dol_refresh.log`, `edgar_search.log`, `fetch_cbp.log`, `fetch_susb.log` (untracked), `run_did_susb.log` (untracked). Most are tracked. None are referenced by any writeup. Strong gitignore candidates.
- No `test_`, `scratch_`, or `_old` files spotted. No half-finished scripts.

**Subdir contents:**
- `analysis/tables/` — 10 small per-table CSVs (firm-level analysis outputs, plus `susb_normalized_rates_by_state_size.csv` from today). Looks fine.
- `analysis/benchmark_sources/` — 2 PDFs: `ici_brightscope_dc_plan_profile_2023.pdf` (2 MB) and `vanguard_how_america_saves_2025.pdf` (9.2 MB). These are reference documents downloaded for the match-formula benchmarking work. 11 MB committed; could be regenerated by re-downloading from public URLs.

---

## Section 5: Methodology directory contents

`ls -la methodology/` — 18 files.

| File | Last touched | Role | Notes |
|---|---|---|---|
| `.gitkeep` | 2026-02-03 | original placeholder | stale, harmless |
| `04 exp.txt` | 2026-03-30 | stray notes from unrelated work | gitignored ✓ |
| `Claude Code Pre push Validation.txt` | 2026-02-03 | unclear — looks like a stray | **NOT gitignored** — flag |
| `MAC 2625-1-1.17 Is not defined as b.txt` | 2026-03-30 | stray notes | gitignored ✓ |
| `METHODOLOGY.md` | 2026-04-29 | brief methodology overview | canonical |
| `bls_qcew_collection_spec.md` | 2026-05-06 | QCEW pull spec (executed) | **completed, can be archived** |
| `bls_qcew_provenance_addendum.csv` | 2026-05-06 | QCEW per-state-year pull log | active reference |
| `brightscope_access_assessment.md` | 2026-04-29 | "Decision: No — BrightScope is enterprise-licensed only" | **completed assessment, not active** |
| `census_susb_collection_spec.md` | 2026-05-06 | SUSB pull spec (executed) | **completed, can be archived** |
| `census_susb_provenance_addendum.csv` | 2026-05-06 | SUSB pull log | active reference |
| `did_design_memo.md` | 2026-04-29 | DiD pre-registration memo | canonical (locks in CS over TWFE, v1+v2 as parallel specs) |
| `dol_refresh_delta_2026_04.md` | 2026-04-29 | DOL refresh delta report | active reference |
| `pre_memo_verification.md` | 2026-05-06 | Pre-memo year-range and ratio checks | canonical (committed today) |
| `source_provenance_log.csv` | 2026-04-29 | source-provenance master log | **mostly TBD — flag** |
| `state_admin_collection_log.md` | 2026-05-06 | state-admin per-state collection log | active reference |
| `state_admin_collection_spec.md` | 2026-05-06 | state-admin pull spec (executed) | **completed, can be archived** |
| `state_admin_provenance_addendum.csv` | 2026-05-06 | state-admin sources log | active reference |
| `state_auto_ira_prompts_log.md` | 2026-02-15 | early prompts log from initial dataset build | historical, stale |

**Source provenance log state (`source_provenance_log.csv`):**
- 22 rows total. Of the 16 Form 5500 / 5500-SF year rows, only **4 have actual data** (Form 5500 2024 + 2025; Form 5500-SF 2024 + 2025 — populated by the April 2026 refresh).
- The other 12 Form 5500 / 5500-SF year rows are still **TBD placeholders** for raw_rows, after_pension_code_2J_filter, and downstream filter columns.
- Schedule H, Schedule I, Schedule R rows are TBD by design (they're for derived fields).
- Two TOTAL_v1_inclusive / TOTAL_v2_conservative summary rows are populated.
- Net: the log is a partial scaffold, not a complete provenance record. A reader cannot trace any single firm's filing year back to its row count without the data being there.

**Three new provenance addendums** (BLS QCEW, Census SUSB, state admin) live in this dir as separate files rather than rows in `source_provenance_log.csv`. That's a deliberate parallel-write decision from the three-workstream batch (to avoid concurrent-write conflicts), but it means the source provenance is now fragmented across four files.

**Obsolete planning specs:**
- `brightscope_access_assessment.md` — explicitly closed (decision = No). Suitable to mark as archived/closed in a header.
- The three `*_collection_spec.md` (BLS QCEW, Census SUSB, state admin) — work is done; specs are now historical artifacts rather than active plans.

---

## Section 6: Data directory contents

`du -sh data/*`:

```
183M    data/bls_qcew/         ← FLAG: 408 raw CSVs committed
 26M    data/census_susb/      ← FLAG: 6 raw xlsx files committed
  0     data/claude-code/      ← empty placeholder dir
  0     data/codex/            ← empty placeholder dir
4.0K    data/data_README.md    canonical
9.7M    data/processed/        ← FLAG: looks superseded
 26M    data/refresh_2026_04/  ← FLAG: looks like a date-stamped backup
 48K    data/state_admin/      canonical (committed today)
 14M    data/v1-inclusive/     canonical
 13M    data/v2-conservative/  canonical
─────
268M    data/                  total
```

**Flagged items (gitignore / cleanup candidates):**

1. **`data/bls_qcew/raw/`** — 408 CSV files (51 states × 8 years) totaling **183 MB**. These are raw downloads from BLS's per-state-per-year API. The standardized panel `data/bls_qcew/state_year_private_establishments.csv` is the actual project deliverable; the raw files are reproducible by re-running `analysis/fetch_qcew.py`. Strong gitignore candidate.

2. **`data/census_susb/raw/`** — 6 SUSB xlsx files (one per year 2017–2022) totaling **25 MB**. Raw Census downloads. Reproducible by re-running `analysis/fetch_susb.py`. Strong gitignore candidate.

3. **`data/refresh_2026_04/v1-inclusive/`** and **`/v2-conservative/`** — appear to be a date-stamped backup of the canonical `data/v1-inclusive/` and `data/v2-conservative/` files, taken during the April 2026 DOL refresh. The `.csv` sizes differ slightly from the canonical files (13.8 MB vs 13.7 MB; 12.6 MB vs 12.6 MB) — so this is a snapshot, not an exact duplicate. ~26 MB total. If the `dol_refresh_delta_2026_04.md` writeup adequately documents the diff, the backup files can be removed.

4. **`data/processed/state_auto_ira_401k_dataset.csv`** — 9.7 MB, dated Feb 15. Looks like a pre-v1/v2-split single-version build artifact. The README's repo-structure listing references it as "Latest single build output" but the canonical outputs are now the v1/v2 split. Probably safe to remove.

5. **`data/claude-code/`** and **`data/codex/`** — empty dirs (0 bytes each). Probably created during the early multi-tool validation work but never used. Safe to remove (or `.gitkeep` and document).

6. **`data/state_admin/`** — 48 KB, committed today, canonical for the state-admin workstream.

The 268 MB total is dominated by the raw downloads (~210 MB across QCEW, SUSB, refresh backup, processed). Without those, the data dir would be ~28 MB — modest.

---

## Section 7: Git hygiene

**Recent activity:**
- 18 commits in the last 30 days (April 5 – May 6).
- Working tree is currently *clean* for tracked files, but has 3 untracked items: `analysis/__pycache__/`, `analysis/fetch_susb.log`, `analysis/run_did_susb.log`.

**Branches:**
- Local: only `master`.
- Remote: `remotes/origin/main` AND `remotes/origin/master`.
- `origin/main` is **behind** by all of the recent work — at minimum the three-workstream batch (commits `c9c8b5d`, `db7d2c1`, `21883a6`), the Maine edit (`7b02aa9`), the qualitative evidence (`f5ccee2`), and likely earlier commits as well. Local `master` and `origin/master` are in sync.
- This is a stakeholder-readability flag: GitHub's default-branch dropdown might point to `main`, which is much older than `master`. If the GitHub repo's default branch is `master`, it's fine. If `main` is the GitHub default, stakeholders see a stale repo.

**Large blobs in git history:**
- The CSV files in `analysis/` (DiD panels, results, etc.) are committed by design and small (typically < 150 KB).
- I didn't find evidence of committed-then-deleted bulk data files. The 183 MB QCEW raw and 25 MB SUSB raw appear to be currently committed (so they're in working tree, not just history) — no orphaned-history-blob problem, but they bloat the working tree and clones.

**`.gitignore` contents:**

```
form5500-raw-data/

# Stray notes from unrelated work (federal regulation analysis)
methodology/04 exp.txt
methodology/MAC 2625-1-1.17 Is not defined as b.txt

# Generated docx files are derived artifacts; the markdown is the source of truth
deliverables/stakeholder_status_update.docx
deliverables/calsavers_cpra_request.docx
```

**What `.gitignore` does NOT cover** (and probably should):
- `__pycache__/` — currently untracked but creates a `git status` noise line every session
- `*.log` — there are 9 log files in `analysis/`, mostly tracked
- `*.pyc`
- `.DS_Store` (no evidence any exist, but defensive)
- `analysis/benchmark_sources/*.pdf` — debatable; if the PDFs are downloaded references, gitignore + a `README.md` listing the URLs is cleaner
- `data/bls_qcew/raw/` and `data/census_susb/raw/` — bulk raw downloads
- `methodology/Claude Code Pre push Validation.txt` — stray, but `.gitignore` only covers two of the three stray methodology files
- The empty-zero-byte `git` file at root (currently tracked)

---

## Section 8: External-reader 90-second test

Putting on a stakeholder hat — never seen this repo, hits the GitHub front page, has 90 seconds.

**What I see at the GitHub root:**

The first thing my eye catches is the file list with `git`, `search.html`, `build_both.py`, `build_both_2026_04.py`, `build_dataset.py` — that's *three* build scripts and one zero-byte `git` file. My first impression is "this repo isn't tidy."

The README is 9.4 KB which is fine. I scroll through:
- I learn about firms that established 401(k)s in mandate states. ✓
- I see firm counts of 115,690 / 106,577. ✓
- I get a "Methodology" section that is filtering rules for Form 5500 — useful but feels low-level.
- I scroll to "Recommended Next Steps" which lists "Difference-in-differences" as a future step. **This makes me think the project hasn't done the DiD yet.**
- I never see the words "Callaway-Sant'Anna," "ATT," "qualitative evidence," "Gusto," or "Colorado Treasury" — none of the substance from the past two months.
- I don't see a clear "where to look first" pointer.

**Can I tell what the project is?** Yes, in broad strokes. I'd describe it as "a dataset of mandate-induced 401(k) plan firms."

**Can I find the headline result?** **No.** The README doesn't surface it. I'd have to know to click into `analysis/did_results.md` or `deliverables/stakeholder_status_update.md`. The headline ATT (~2.4 per 1k establishments) is not on the README.

**Can I find the canonical write-up?** Also no. The deliverables/ directory has 14 files of varying provenance. Without knowing which is current, I might click `FINAL_SUMMARY.md` (which sounds canonical but is from Feb 15 and only describes the dataset).

**What's confusing or unprofessional:**
- The empty `git` file is the worst single thing — it's the kind of artifact that signals "no one cleaned up before sharing." Easy fix.
- Three build scripts with overlapping names at root (`build_both.py`, `build_both_2026_04.py`, `build_dataset.py`) — I don't know which to run.
- `search.html` at root with no apparent purpose.
- The README's "Recommended Next Steps" lists work that is in fact done. This actively misleads.
- The data dir is large (268 MB) for a stats project; clones take a noticeable moment. Most of that is regenerable raw downloads.
- The `validation/` dir at root contains Feb-era audit files for the firm dataset; relative to current work (DiD, qualitative evidence) it looks like fossil.
- Provenance log mostly TBD reads as "audit trail not maintained" even though substantively the work was done.

**What would help in cleanup:**
1. Update the README to lead with the DiD headline and point to the canonical writeup.
2. Remove the empty `git` file, `search.html`, redundant build scripts, and the stray methodology/Claude Code Pre push Validation.txt.
3. Gitignore + remove the 183 MB of raw QCEW + 25 MB of raw SUSB downloads.
4. Decide what to do with `data/processed/`, `data/refresh_2026_04/`, `data/claude-code/`, `data/codex/`.
5. Either populate or de-scaffold the source provenance log so TBD rows don't look like neglect.
6. Mark the Feb-era deliverables (FINAL_SUMMARY.md, State_AutoIRA_Project_Report.md, summary_statistics.csv) as historical, or move to an `archive/` subdir.
7. Verify which GitHub branch (main vs master) is the default; bring whichever-is-default up to date.

None of this is needed for the analysis to be correct. It's purely about the front-door experience the stakeholder will get.

---

## What this audit does NOT do

- Does not modify, move, rename, or delete any files
- Does not update the README
- Does not change the .gitignore
- Does not commit any cleanup
- Does not make recommendations about which Feb-era deliverables to keep vs archive — that's a substantive call for the project owner

Cleanup decisions get made in the follow-up session.
