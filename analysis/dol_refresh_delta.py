"""Compute per-state and per-year deltas between v3 (Feb 2026) and the
refreshed (Apr 2026) descriptive datasets, and write a markdown report
to methodology/dol_refresh_delta_2026_04.md.

Inputs:
    data/v1-inclusive/state_auto_ira_401k_dataset.csv         (v3, baseline)
    data/v2-conservative/state_auto_ira_401k_dataset.csv      (v3, baseline)
    data/refresh_2026_04/v1-inclusive/state_auto_ira_401k_dataset.csv
    data/refresh_2026_04/v2-conservative/state_auto_ira_401k_dataset.csv

Output:
    methodology/dol_refresh_delta_2026_04.md
"""

from __future__ import annotations

import os
import datetime as dt
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3_PATHS = {
    "v1": os.path.join(REPO, "data", "v1-inclusive",
                        "state_auto_ira_401k_dataset.csv"),
    "v2": os.path.join(REPO, "data", "v2-conservative",
                        "state_auto_ira_401k_dataset.csv"),
}
REFRESH_PATHS = {
    "v1": os.path.join(REPO, "data", "refresh_2026_04", "v1-inclusive",
                        "state_auto_ira_401k_dataset.csv"),
    "v2": os.path.join(REPO, "data", "refresh_2026_04", "v2-conservative",
                        "state_auto_ira_401k_dataset.csv"),
}
OUT_PATH = os.path.join(REPO, "methodology", "dol_refresh_delta_2026_04.md")

LATE_TREATMENT = ["ME", "DE", "NJ"]
ALL_STATES = ["CA", "CO", "CT", "DE", "IL", "MD", "ME", "NJ", "OR", "VA"]


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["PLAN_EFFECTIVE_DATE"] = pd.to_datetime(df["PLAN_EFFECTIVE_DATE"])
    df["start_year"] = df["PLAN_EFFECTIVE_DATE"].dt.year
    return df


def state_counts(df: pd.DataFrame) -> pd.Series:
    return df.groupby("STATE").size().reindex(ALL_STATES, fill_value=0)


def year_counts(df: pd.DataFrame) -> pd.Series:
    return df.groupby("start_year").size()


def state_year_counts(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby(["STATE", "start_year"]).size()
              .unstack(fill_value=0)
              .reindex(ALL_STATES, fill_value=0))


def main():
    print("Loading datasets...")
    v3 = {k: load(p) for k, p in V3_PATHS.items()}
    new = {k: load(p) for k, p in REFRESH_PATHS.items()}

    pull_date = dt.date.today().isoformat()

    # state-level delta
    rows = []
    for k in ("v1", "v2"):
        v3_st = state_counts(v3[k])
        new_st = state_counts(new[k])
        for state in ALL_STATES:
            old = int(v3_st[state])
            cur = int(new_st[state])
            rows.append({
                "version": k,
                "state": state,
                "v3_count": old,
                "refresh_count": cur,
                "delta": cur - old,
                "pct_change": round((cur - old) / old * 100, 2)
                              if old > 0 else float("inf"),
            })

    state_delta = pd.DataFrame(rows)

    # year-level delta
    year_rows = []
    for k in ("v1", "v2"):
        v3_yr = year_counts(v3[k])
        new_yr = year_counts(new[k])
        all_years = sorted(set(v3_yr.index) | set(new_yr.index))
        for yr in all_years:
            old = int(v3_yr.get(yr, 0))
            cur = int(new_yr.get(yr, 0))
            year_rows.append({
                "version": k,
                "year": int(yr),
                "v3_count": old,
                "refresh_count": cur,
                "delta": cur - old,
            })
    year_delta = pd.DataFrame(year_rows)

    # state-year matrix for late-treatment focus
    sy_focus = {}
    for k in ("v1", "v2"):
        v3_sy = state_year_counts(v3[k])
        new_sy = state_year_counts(new[k])
        # union the columns
        all_yrs = sorted(set(v3_sy.columns) | set(new_sy.columns))
        v3_sy = v3_sy.reindex(columns=all_yrs, fill_value=0)
        new_sy = new_sy.reindex(columns=all_yrs, fill_value=0)
        sy_focus[k] = (v3_sy, new_sy)

    # totals
    v3_totals = {k: len(v3[k]) for k in ("v1", "v2")}
    new_totals = {k: len(new[k]) for k in ("v1", "v2")}
    total_deltas = {k: new_totals[k] - v3_totals[k] for k in ("v1", "v2")}

    # write report
    md = build_md(pull_date, v3_totals, new_totals, total_deltas,
                  state_delta, year_delta, sy_focus)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {OUT_PATH}")


def build_md(pull_date, v3_totals, new_totals, total_deltas,
              state_delta, year_delta, sy_focus) -> str:

    # Helper: filter by version
    def st_table(version):
        d = state_delta[state_delta["version"] == version].copy()
        d = d.sort_values("delta", ascending=False)
        cols = ["state", "v3_count", "refresh_count", "delta", "pct_change"]
        return d[cols].to_markdown(index=False, tablefmt="pipe")

    def yr_table(version):
        d = year_delta[year_delta["version"] == version].copy()
        d = d.sort_values("year")
        cols = ["year", "v3_count", "refresh_count", "delta"]
        return d[cols].to_markdown(index=False, tablefmt="pipe")

    # late-treatment-state focus tables
    def late_table(version):
        v3_sy, new_sy = sy_focus[version]
        out_rows = []
        for st in LATE_TREATMENT:
            for yr in v3_sy.columns:
                out_rows.append({
                    "state": st, "year": int(yr),
                    "v3_count": int(v3_sy.loc[st, yr])
                                if st in v3_sy.index else 0,
                    "refresh_count": int(new_sy.loc[st, yr])
                                       if st in new_sy.index else 0,
                })
        df = pd.DataFrame(out_rows)
        df["delta"] = df["refresh_count"] - df["v3_count"]
        df = df[(df["v3_count"] > 0) | (df["refresh_count"] > 0)]
        return df.to_markdown(index=False, tablefmt="pipe")

    # Headline interpretation
    big_state_v1 = state_delta[(state_delta["version"] == "v1")
                                & (state_delta["delta"].abs() > 0)]
    big_state_v2 = state_delta[(state_delta["version"] == "v2")
                                & (state_delta["delta"].abs() > 0)]

    pct_v1 = round(total_deltas["v1"] / v3_totals["v1"] * 100, 2)
    pct_v2 = round(total_deltas["v2"] / v3_totals["v2"] * 100, 2)

    # ME/DE/NJ delta totals
    me_de_nj_v1 = state_delta[(state_delta["version"] == "v1")
                                & (state_delta["state"].isin(LATE_TREATMENT))]
    me_de_nj_v2 = state_delta[(state_delta["version"] == "v2")
                                & (state_delta["state"].isin(LATE_TREATMENT))]
    late_delta_v1 = me_de_nj_v1["delta"].sum()
    late_delta_v2 = me_de_nj_v2["delta"].sum()

    # Materiality assessment
    def materiality(pct, late_pct):
        if abs(pct) < 1 and abs(late_pct) < 5:
            return ("**Not material.** Both the overall delta and the "
                    "late-treatment-state delta are within typical "
                    "month-to-month DOL refresh noise. Re-running the full "
                    "DiD analysis is unlikely to change the headline ATT.")
        if abs(pct) < 5:
            return ("**Potentially material for late-cohort estimates.** "
                    "The overall change is small, but the late-treatment "
                    "states (ME, DE, NJ) saw measurable filings catch up. "
                    "The Callaway-Sant'Anna ATT for the 2024 cohort would "
                    "shift; the headline simple ATT (which weights all "
                    "cohorts) would shift much less. Worth re-running.")
        return ("**Material — re-run recommended.** The dataset has "
                "changed by more than 5% overall. Anything built on the "
                "Feb 2026 dataset (firm-level analysis, descriptive tables, "
                "DiD panel) should be regenerated.")

    late_pct_v1 = (round(late_delta_v1 /
                          me_de_nj_v1["v3_count"].sum() * 100, 2)
                    if me_de_nj_v1["v3_count"].sum() > 0 else 0)
    late_pct_v2 = (round(late_delta_v2 /
                          me_de_nj_v2["v3_count"].sum() * 100, 2)
                    if me_de_nj_v2["v3_count"].sum() > 0 else 0)

    md = f"""# DOL Form 5500 Refresh — Delta Report (April 2026)

**Refresh pull date:** {pull_date}
**Prior pull date:** 2026-01-25 (Form 5500 + 5500-SF; the v3 dataset)
**Refresh source URLs:** `https://askebsa.dol.gov/FOIA%20Files/2024/All/F_5500_2024_All.zip`, `F_5500_SF_2024_All.zip`, `F_5500_2025_All.zip`, `F_5500_SF_2025_All.zip`
**Comparison build:** `data/refresh_2026_04/v1-inclusive/` and `data/refresh_2026_04/v2-conservative/`
**v3 reference:** `data/v1-inclusive/` (115,690) and `data/v2-conservative/` (106,577)

## Headline

| Version | v3 (Feb 2026) | Refresh (Apr 2026) | Δ count | Δ % |
|---|---|---|---|---|
| v1-inclusive | {v3_totals['v1']:,} | {new_totals['v1']:,} | {total_deltas['v1']:+,} | {pct_v1:+.2f}% |
| v2-conservative | {v3_totals['v2']:,} | {new_totals['v2']:,} | {total_deltas['v2']:+,} | {pct_v2:+.2f}% |

The refresh adds **{total_deltas['v1']:+,} firms** in v1-inclusive and **{total_deltas['v2']:+,} firms** in v2-conservative. These changes reflect a combination of (a) DOL monthly updates that added new filings to the 2024 plan year for plans that filed late, and (b) the inclusion of the partial 2025 plan-year file, which captures plans with effective dates after each state's mandate that filed Form 5500 for plan year 2025.

## State-by-state delta — v1-inclusive

{st_table("v1")}

## State-by-state delta — v2-conservative

{st_table("v2")}

## Year-by-year delta — v1-inclusive

(by plan effective year, not filing year — refresh adds filings for new effective years and corrections for prior effective years)

{yr_table("v1")}

## Year-by-year delta — v2-conservative

{yr_table("v2")}

## Late-treatment focus (ME, DE, NJ)

These three states had filing lag flagged in the prior DiD design memo: their 2024 cohort effects in the prior CS estimation were imprecise because their post-treatment data was only partial.

### v1-inclusive — ME, DE, NJ delta

{late_table("v1")}

ME / DE / NJ combined delta: **{late_delta_v1:+,} firms** ({late_pct_v1:+.2f}% relative to v3 figure for those three states).

### v2-conservative — ME, DE, NJ delta

{late_table("v2")}

ME / DE / NJ combined delta: **{late_delta_v2:+,} firms** ({late_pct_v2:+.2f}% relative to v3 figure for those three states).

## Materiality assessment

**v1-inclusive:** {materiality(pct_v1, late_pct_v1)}

**v2-conservative:** {materiality(pct_v2, late_pct_v2)}

## What this means for the DiD analysis

The DiD headline ATT (2.37 per 1,000 establishments) was estimated on the v3 dataset's underlying effective-year aggregations. The relevant question for re-running is whether the DiD panel — built from `analysis/build_state_year_panel.py` against the raw Form 5500 data, **not** from the descriptive v3 dataset — would change.

Two reasons the DiD panel is more stable than the headline counts:
1. The DiD panel aggregates ALL state-year new 401(k) plans (mandate + control), so changes are normalized by the (also growing) control population.
2. The CS estimator's bootstrap inference draws on the entire panel; one cohort's filings catching up changes that cohort's ATT but is averaged across the simple-aggregation weights.

If the late-treatment-state delta is meaningful (>5%), the cohort effect for cohort 2024 will shift and should be re-reported. If it's small, it's not worth a full re-run.

**Recommendation:** {materiality(pct_v1, late_pct_v1).split('**')[1]}

## Caveats

- The pull date for the v3 dataset is 2026-01-25 per file mtimes, not 2026-02-XX as commonly assumed in earlier memos. The "February 2026" framing in earlier writeups is approximate.
- 2025 plan-year coverage is partial: only filings DOL has received and posted as of {pull_date} are reflected. The 2025 file will continue to grow over the rest of 2026.
- The refresh was applied uniformly to all 10 mandate states; no special handling for any state.
- Files refreshed: F_5500 (Form 5500 main filings) and F_5500_SF (Form 5500-SF small-plan filings) for both 2024 and 2025. Schedule R / H / I were NOT re-pulled in this refresh; the contribution-rate join in build_dataset.py uses the existing pre-refresh schedules.

## Files

- `data/refresh_2026_04/v1-inclusive/state_auto_ira_401k_dataset.csv`
- `data/refresh_2026_04/v2-conservative/state_auto_ira_401k_dataset.csv`
- `data/refresh_2026_04/v1-inclusive/summary_statistics.csv`
- `data/refresh_2026_04/v2-conservative/summary_statistics.csv`
- `methodology/source_provenance_log.csv` — populated TBDs for 2024 and 2025
- `form5500-raw-data/refresh_2026_04/F_5500_2024_All.zip`, `F_5500_SF_2024_All.zip`,
  `F_5500_2025_All.zip`, `F_5500_SF_2025_All.zip`
- `form5500-raw-data/pre_refresh_backup_2026_04/` — preserved 2024 CSVs from v3
"""
    return md


if __name__ == "__main__":
    main()
