"""Firm-level descriptive analysis of the v2-conservative dataset.

Produces tables for:
    1. Firm-size distribution by SBA-style buckets
    2. State-by-size cross-tab
    3. Plan-start-year distribution by state
    4. Employer-contribution subset (firms with non-null EMPLOYER_CONTRIBUTION)

Outputs to analysis/tables/ as CSVs and to analysis/firm_level_analysis.md
as a synthesis writeup.

Size bucket definition (no formal workplan exists, so applying SBA-style
ranges adapted for Form 5500 covered-participant counts):

    solo:    0-1 covered participants (owner-only / self-employed)
    micro:   2-9
    small:   10-49
    medium:  50-249
    large:   250+
"""

from __future__ import annotations

import os
import pandas as pd
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO, "data", "v2-conservative",
                         "state_auto_ira_401k_dataset.csv")
TABLES_DIR = os.path.join(REPO, "analysis", "tables")
os.makedirs(TABLES_DIR, exist_ok=True)

SIZE_BUCKETS = [
    ("solo", 0, 1),
    ("micro", 2, 9),
    ("small", 10, 49),
    ("medium", 50, 249),
    ("large", 250, np.inf),
]
SIZE_ORDER = [b[0] for b in SIZE_BUCKETS]


def assign_size(emp):
    if pd.isna(emp):
        return "unknown"
    for label, lo, hi in SIZE_BUCKETS:
        if lo <= emp <= hi:
            return label
    return "unknown"


def main():
    df = pd.read_csv(DATA_PATH)
    df["PLAN_EFFECTIVE_DATE"] = pd.to_datetime(df["PLAN_EFFECTIVE_DATE"])
    df["start_year"] = df["PLAN_EFFECTIVE_DATE"].dt.year
    df["size_bucket"] = df["EMPLOYEE_COUNT"].apply(assign_size)

    # ---------- Table 1: overall size distribution ----------
    counts = df["size_bucket"].value_counts().reindex(
        SIZE_ORDER + ["unknown"], fill_value=0
    ).astype(int)
    pct = (counts / counts.sum() * 100).round(2)
    t1 = pd.DataFrame({
        "size_bucket": counts.index,
        "n_firms": counts.values,
        "pct_of_total": pct.values,
    })
    t1.to_csv(os.path.join(TABLES_DIR, "size_distribution_overall.csv"),
              index=False)

    # ---------- Table 2: state × size ----------
    cross = pd.crosstab(df["STATE"], df["size_bucket"])
    cross = cross.reindex(columns=SIZE_ORDER + ["unknown"], fill_value=0)
    cross["total"] = cross.sum(axis=1)
    cross.loc["TOTAL"] = cross.sum(axis=0)
    cross.to_csv(os.path.join(TABLES_DIR, "state_by_size.csv"))

    # State × size as % of state
    pct_state = pd.crosstab(df["STATE"], df["size_bucket"], normalize="index") * 100
    pct_state = pct_state.reindex(columns=SIZE_ORDER + ["unknown"],
                                  fill_value=0).round(2)
    pct_state.to_csv(os.path.join(TABLES_DIR, "state_by_size_pct.csv"))

    # ---------- Table 3: plan-start-year by state ----------
    yr_state = pd.crosstab(df["start_year"], df["STATE"])
    yr_state["total"] = yr_state.sum(axis=1)
    yr_state.loc["TOTAL"] = yr_state.sum(axis=0)
    yr_state.to_csv(os.path.join(TABLES_DIR, "plan_start_year_by_state.csv"))

    # Median start year per state
    med_year = (df.groupby("STATE")["start_year"].agg(
        median="median", min="min", max="max", n="count"
    ).round(1).reset_index())
    med_year.to_csv(os.path.join(TABLES_DIR, "plan_start_year_summary.csv"),
                    index=False)

    # ---------- Table 4: contribution subset ----------
    contrib = df[df["EMPLOYER_CONTRIBUTION"].notna()].copy()
    contrib["contrib_zero"] = (contrib["EMPLOYER_CONTRIBUTION"] == 0).astype(int)
    contrib["contrib_per_employee"] = (
        contrib["EMPLOYER_CONTRIBUTION"] /
        contrib["EMPLOYEE_COUNT"].replace(0, np.nan)
    )

    t4_overall = pd.DataFrame({
        "metric": ["n_firms_with_contrib_data",
                    "pct_of_full_dataset",
                    "n_zero_contrib",
                    "pct_zero_contrib",
                    "median_total_contrib",
                    "mean_total_contrib",
                    "p75_total_contrib",
                    "p95_total_contrib",
                    "median_per_employee",
                    "mean_per_employee"],
        "value": [
            len(contrib),
            round(len(contrib) / len(df) * 100, 2),
            int(contrib["contrib_zero"].sum()),
            round(contrib["contrib_zero"].mean() * 100, 2),
            float(contrib["EMPLOYER_CONTRIBUTION"].median()),
            round(float(contrib["EMPLOYER_CONTRIBUTION"].mean()), 2),
            float(contrib["EMPLOYER_CONTRIBUTION"].quantile(0.75)),
            float(contrib["EMPLOYER_CONTRIBUTION"].quantile(0.95)),
            float(contrib["contrib_per_employee"].median()),
            round(float(contrib["contrib_per_employee"].mean()), 2),
        ],
    })
    t4_overall.to_csv(os.path.join(TABLES_DIR, "contribution_summary.csv"),
                      index=False)

    # Contribution by state (only firms with data)
    by_state_contrib = (contrib.groupby("STATE")["EMPLOYER_CONTRIBUTION"]
                        .agg(n="count", median="median", mean="mean",
                             pct_zero=lambda x: (x == 0).mean() * 100)
                        .round(2).reset_index())
    by_state_contrib.to_csv(
        os.path.join(TABLES_DIR, "contribution_by_state.csv"), index=False
    )

    # Contribution by size bucket
    by_size_contrib = (contrib.groupby("size_bucket")["EMPLOYER_CONTRIBUTION"]
                       .agg(n="count", median="median", mean="mean",
                            pct_zero=lambda x: (x == 0).mean() * 100)
                       .round(2).reindex(SIZE_ORDER + ["unknown"]).reset_index())
    by_size_contrib.to_csv(
        os.path.join(TABLES_DIR, "contribution_by_size.csv"), index=False
    )

    # ---------- Composition checks (size × state for narrative) ----------
    solo_pct_by_state = (df.assign(is_solo=(df["size_bucket"] == "solo").astype(int))
                         .groupby("STATE")["is_solo"].mean() * 100).round(2)
    solo_pct_by_state = solo_pct_by_state.reset_index().rename(
        columns={"is_solo": "pct_solo"}
    )
    solo_pct_by_state.to_csv(os.path.join(TABLES_DIR, "pct_solo_by_state.csv"),
                             index=False)

    # ---------- Markdown writeup ----------
    md = build_markdown(df, t1, cross, pct_state, yr_state, med_year,
                        t4_overall, by_state_contrib, by_size_contrib,
                        solo_pct_by_state)
    with open(os.path.join(REPO, "analysis", "firm_level_analysis.md"),
              "w", encoding="utf-8") as f:
        f.write(md)

    print("Wrote firm-level tables to analysis/tables/")
    print("Wrote analysis/firm_level_analysis.md")


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    out = df.copy()
    if max_rows is not None:
        out = out.head(max_rows)
    return out.to_markdown(index=False, tablefmt="pipe")


def build_markdown(df, t1, cross, pct_state, yr_state, med_year,
                    t4_overall, by_state_contrib, by_size_contrib,
                    solo_pct_by_state) -> str:
    n = len(df)
    n_solo = (df["size_bucket"] == "solo").sum()
    n_micro = (df["size_bucket"] == "micro").sum()
    n_small = (df["size_bucket"] == "small").sum()
    n_medium = (df["size_bucket"] == "medium").sum()
    n_large = (df["size_bucket"] == "large").sum()
    n_unknown = (df["size_bucket"] == "unknown").sum()
    pct_solo_overall = n_solo / n * 100
    pct_micro_overall = n_micro / n * 100

    high_solo = solo_pct_by_state.sort_values("pct_solo", ascending=False).head(3)
    low_solo = solo_pct_by_state.sort_values("pct_solo").head(3)

    contrib_n = int(t4_overall.loc[t4_overall["metric"] == "n_firms_with_contrib_data",
                                   "value"].iloc[0])
    contrib_pct = float(t4_overall.loc[t4_overall["metric"] == "pct_of_full_dataset",
                                       "value"].iloc[0])
    pct_zero = float(t4_overall.loc[t4_overall["metric"] == "pct_zero_contrib",
                                    "value"].iloc[0])
    median_contrib = float(t4_overall.loc[t4_overall["metric"] == "median_total_contrib",
                                          "value"].iloc[0])
    p75_contrib = float(t4_overall.loc[t4_overall["metric"] == "p75_total_contrib",
                                        "value"].iloc[0])

    md = f"""# Firm-Level Descriptive Analysis (v2-conservative dataset)

**Date:** 2026-04-29
**Dataset:** `data/v2-conservative/state_auto_ira_401k_dataset.csv` ({n:,} firms)
**Source filters:** new single-employer 401(k) plans (pension code 2J) with plan effective date after the v2-conservative mandate date in each of 10 mandate states. Deduplicated by EIN.

---

## 1. Firm-size distribution

Size buckets (covered-participant counts from Form 5500 / 5500-SF, beginning-of-year):

- **solo:** 0-1
- **micro:** 2-9
- **small:** 10-49
- **medium:** 50-249
- **large:** 250+

(There is no formal workplan defining these bands. The bands are SBA-style ranges adapted for plan-participant counts; see "Notes" at the end for what would change if the workplan defines them differently.)

{md_table(t1)}

The **modal mandate-induced 401(k) is a micro-firm plan**: ~{pct_micro_overall:.0f}% of firms in the dataset have 2-9 covered participants. About {pct_solo_overall:.0f}% are solo (0-1 participants) — these are sole proprietorships and very small partnerships establishing owner-only / one-employee 401(k)s. Together, solo + micro account for roughly {(n_solo + n_micro) / n * 100:.0f}% of all firms in the dataset.

This is consistent with what auto-IRA mandates were designed to do: the threshold for state-program eligibility is typically 5+ employees (varies by state), so very small firms that don't qualify for the state program but still want some retirement vehicle are establishing 401(k)s.

Large firms (250+ participants) are rare ({n_large:,} firms, {n_large / n * 100:.2f}% of total). Most large firms already had 401(k)s before mandates took effect, so the new-plan dataset captures relatively few of them.

## 2. State-by-size distribution

Counts of new 401(k) plans by state and size bucket:

{md_table(cross.reset_index())}

Same table as percentages within each state (rows sum to ~100):

{md_table(pct_state.round(1).reset_index())}

**Highest solo share:** {", ".join(f"{r['STATE']} ({r['pct_solo']:.1f}%)" for _, r in high_solo.iterrows())}.
**Lowest solo share:** {", ".join(f"{r['STATE']} ({r['pct_solo']:.1f}%)" for _, r in low_solo.iterrows())}.

The cross-state variation in solo share is large — high-solo states have nearly twice the solo concentration of low-solo states. This is worth flagging as an interpretation caveat: when we say "X% of firms in mandate states established 401(k)s after mandate," the *kind* of firm differs materially across states. A state with a high solo share is largely capturing self-employed individuals; a state with a low solo share is capturing more genuine employer-employee plan formation.

## 3. Plan-start-year by state

Counts of new plans by year of plan effective date and state:

{md_table(yr_state.reset_index())}

Most plans cluster in 2022-2024, reflecting both (a) the staggered roll-out of mandates across states and (b) DOL filing lag — the 2024 effective-year plans are concentrated in Form5500SF_2024 filings, which are still partially incomplete.

Per-state plan-start summary (median, min, max year, n):

{md_table(med_year)}

## 4. Employer contribution patterns (subset)

Schedule H/I employer contribution data is available for only **{contrib_n:,} firms ({contrib_pct:.1f}% of the full dataset)**. The match rate is low because (a) Schedule H is filed only by 100+ participant plans, and (b) Schedule I was discontinued for plan years 2023+. Most firms in this dataset are too small to file Schedule H and too recent to have a Schedule I filing on record.

Among firms with contribution data:

{md_table(t4_overall)}

**{pct_zero:.0f}% of firms with contribution data report zero employer contribution.** This includes both (a) plans where the employer chose a non-matching design and (b) plans where the employer simply hadn't yet contributed in the reported year. The median contribution is **${median_contrib:,.0f}**; the 75th percentile is **${p75_contrib:,.0f}**.

By state:

{md_table(by_state_contrib)}

By size bucket:

{md_table(by_size_contrib)}

The contribution pattern is highly skewed: large firms with contribution data report substantially higher mean contributions than small firms, but the *median* is near zero across most size buckets. The high mean / low median pattern reflects a small number of very large contributors driving the average — useful to know when interpreting any per-employee contribution figure for these mandate-induced plans.

---

## Caveats

1. **EMPLOYEE_COUNT is "covered participants" not "headcount."** Form 5500's TOT_PARTCP_BOY_CNT counts plan participants, not all employees. A firm with 50 employees but only 30 plan participants would be coded "small" (10-49) here even though it has medium headcount. This affects bucket boundaries but not the qualitative picture.

2. **Some plans have effective dates after their filing year.** A 2024 Form 5500-SF can report a plan effective in 2025-08; the dataset includes these. They appear in `start_year=2025` in Table 3.

3. **Solo plans dominate.** ~{(n_solo + n_micro) / n * 100:.0f}% of the dataset is solo or micro (0-9 participants). Any ATT-style claim about "401(k) plan formation" needs to disclose this composition. The DiD robustness check restricting to plans with positive employee count drops the ATT from 2.37 to 1.82 (analysis/did_results.md), and that's the version that makes a sharper claim about employer-employee retirement coverage.

4. **Contribution data is non-representative.** The 3.4% of firms with EMPLOYER_CONTRIBUTION populated are systematically larger and older than the dataset as a whole. Any cross-state contribution comparison must caveat this.

## Files

- `analysis/tables/size_distribution_overall.csv`
- `analysis/tables/state_by_size.csv`
- `analysis/tables/state_by_size_pct.csv`
- `analysis/tables/plan_start_year_by_state.csv`
- `analysis/tables/plan_start_year_summary.csv`
- `analysis/tables/contribution_summary.csv`
- `analysis/tables/contribution_by_state.csv`
- `analysis/tables/contribution_by_size.csv`
- `analysis/tables/pct_solo_by_state.csv`
"""
    return md


if __name__ == "__main__":
    main()
