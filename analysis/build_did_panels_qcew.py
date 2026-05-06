"""Build state-year DiD panels with the BLS QCEW denominator added.

Extends the existing CBP-based panels (built by build_did_panels.py) with
QCEW-based outcomes so the headline ATT can be re-estimated under a different
establishment denominator. QCEW is BLS's UI-covered worksite count (annual
average); CBP is the Census March snapshot. Both are private-sector
establishment counts but from different administrative sources.

Inputs (must already exist):
    analysis/state_year_new_401k.csv
    analysis/cbp_state_year.csv
    data/bls_qcew/state_year_private_establishments.csv

Outputs:
    analysis/did_panel_qcew_v1_inclusive.csv
    analysis/did_panel_qcew_v2_conservative.csv

Each output row mirrors the existing did_panel_*.csv schema, plus:
    qcew_establishments
    qcew_employment
    new_401k_per_1000_qcew_establishments
    esrp_rate_per_1000_qcew_estabs
    with_employees_rate_per_1000_qcew_estabs
"""

from __future__ import annotations

import math
import os

import pandas as pd

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = os.path.dirname(os.path.abspath(__file__))

VERSIONS = {
    "v1_inclusive": {
        "OR": "2017-11-01", "IL": "2018-05-01", "CA": "2018-11-01",
        "CT": "2022-04-01", "MD": "2022-09-01", "CO": "2023-01-01",
        "VA": "2023-07-01", "ME": "2024-01-01", "DE": "2024-01-01",
        "NJ": "2024-03-01",
    },
    "v2_conservative": {
        "OR": "2017-11-01", "IL": "2018-11-01", "CA": "2019-07-01",
        "CT": "2022-04-01", "MD": "2022-09-01", "CO": "2023-01-01",
        "VA": "2023-07-01", "ME": "2024-01-01", "DE": "2024-07-01",
        "NJ": "2024-06-30",
    },
}


def first_treatment_year(state: str, mandate_dates: dict) -> float:
    if state not in mandate_dates:
        return math.inf
    return pd.Timestamp(mandate_dates[state]).year


def main():
    counts = pd.read_csv(os.path.join(BASE, "state_year_new_401k.csv"))
    cbp = pd.read_csv(os.path.join(BASE, "cbp_state_year.csv"))
    qcew = pd.read_csv(os.path.join(REPO_ROOT, "data", "bls_qcew",
                                     "state_year_private_establishments.csv"))

    # Restrict QCEW to columns we need; rename to make merges unambiguous.
    qcew_panel = qcew.rename(columns={
        "private_establishments": "qcew_establishments",
        "private_employment": "qcew_employment",
    })[["state", "year", "qcew_establishments", "qcew_employment"]]

    panel = counts.merge(cbp, on=["state", "year"], how="left")
    panel = panel.merge(qcew_panel, on=["state", "year"], how="left")

    # CBP-based rates (kept identical to build_did_panels.py).
    panel["rate_per_1000_estabs"] = (
        panel["new_401k_plans"] / panel["establishments"] * 1000
    )
    panel["esrp_rate_per_1000_estabs"] = (
        panel["new_esrp_plans"] / panel["establishments"] * 1000
    )
    panel["with_employees_rate_per_1000_estabs"] = (
        panel["new_401k_with_employees"] / panel["establishments"] * 1000
    )

    # QCEW-based rates (new outcome — primary deliverable).
    panel["new_401k_per_1000_qcew_establishments"] = (
        panel["new_401k_plans"] / panel["qcew_establishments"] * 1000
    )
    panel["esrp_rate_per_1000_qcew_estabs"] = (
        panel["new_esrp_plans"] / panel["qcew_establishments"] * 1000
    )
    panel["with_employees_rate_per_1000_qcew_estabs"] = (
        panel["new_401k_with_employees"] / panel["qcew_establishments"] * 1000
    )

    for version, mandate_dates in VERSIONS.items():
        v = panel.copy()
        v["first_treatment_year"] = v["state"].apply(
            lambda s: first_treatment_year(s, mandate_dates)
        )
        v["treated"] = (
            (v["first_treatment_year"] != math.inf)
            & (v["year"] >= v["first_treatment_year"])
        ).astype(int)
        is_mandate = v["first_treatment_year"] != math.inf
        v["event_time"] = pd.NA
        v.loc[is_mandate, "event_time"] = (
            v.loc[is_mandate, "year"] - v.loc[is_mandate, "first_treatment_year"]
        )
        v["cohort"] = v["first_treatment_year"].replace(math.inf, 0).astype(int)

        out = os.path.join(BASE, f"did_panel_qcew_{version}.csv")
        v.to_csv(out, index=False)
        n_qcew = v["qcew_establishments"].notna().sum()
        n_total = len(v)
        print(f"Wrote {out}: {n_total:,} rows  ({n_qcew} non-null qcew_establishments)")
        print(f"  Treated states: {sorted(v.loc[is_mandate, 'state'].unique())}")
        cohort_counts = v[is_mandate].drop_duplicates("state")[
            "first_treatment_year"
        ].value_counts().sort_index()
        print(f"  Cohort sizes: {dict(cohort_counts.astype(int))}")
        years_seen = sorted(v["year"].unique())
        print(f"  Years: {years_seen[0]}..{years_seen[-1]}")

    print("\nDone.")


if __name__ == "__main__":
    main()
