"""Build the two state-year DiD panels (v1-inclusive and v2-conservative).

Inputs (must already exist):
    analysis/state_year_new_401k.csv  (from build_state_year_panel.py)
    analysis/cbp_state_year.csv       (from fetch_cbp.py)

Outputs:
    analysis/did_panel_v1_inclusive.csv
    analysis/did_panel_v2_conservative.csv

Each output row is one state-year observation with:
    state, year, new_401k_plans, new_401k_with_employees, new_esrp_plans,
    establishments, employment, rate_per_1000_estabs, esrp_rate_per_1000_estabs,
    treated, first_treatment_year (Inf for never-treated controls),
    event_time (year - first_treatment_year, NaN for never-treated)
"""

import os
import math
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

# Mandate-date definitions copied verbatim from ../build_both.py to keep the
# DiD treatment dummies exactly aligned with the descriptive dataset.
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


def first_treatment_year(state, mandate_dates):
    """Calendar year a state is considered first treated.

    Convention: a state is "treated" beginning in the calendar year of its
    mandate date (so a 2024-06-30 mandate counts 2024 as treated). This
    matches how the descriptive dataset uses 'plan effective date AFTER
    mandate date' — a plan effective in Q3 2024 in NJ counts as post.
    """
    if state not in mandate_dates:
        return math.inf
    return pd.Timestamp(mandate_dates[state]).year


def main():
    counts = pd.read_csv(os.path.join(BASE, "state_year_new_401k.csv"))
    cbp = pd.read_csv(os.path.join(BASE, "cbp_state_year.csv"))

    panel = counts.merge(cbp, on=["state", "year"], how="left")
    panel["rate_per_1000_estabs"] = (
        panel["new_401k_plans"] / panel["establishments"] * 1000
    )
    panel["esrp_rate_per_1000_estabs"] = (
        panel["new_esrp_plans"] / panel["establishments"] * 1000
    )
    panel["with_employees_rate_per_1000_estabs"] = (
        panel["new_401k_with_employees"] / panel["establishments"] * 1000
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
        # event_time: years since treatment (negative for pre-treatment)
        # NaN for never-treated states.
        is_mandate = v["first_treatment_year"] != math.inf
        v["event_time"] = pd.NA
        v.loc[is_mandate, "event_time"] = (
            v.loc[is_mandate, "year"] - v.loc[is_mandate, "first_treatment_year"]
        )
        # cohort encoded as 0 for never-treated (differences package convention)
        v["cohort"] = v["first_treatment_year"].replace(math.inf, 0).astype(int)

        out = os.path.join(BASE, f"did_panel_{version}.csv")
        v.to_csv(out, index=False)
        print(f"Wrote {out}: {len(v):,} rows")
        print(f"  Treated states: {sorted(v.loc[is_mandate, 'state'].unique())}")
        cohort_counts = v[is_mandate].drop_duplicates("state")[
            "first_treatment_year"
        ].value_counts().sort_index()
        print(f"  Cohort sizes (first-treatment-year): "
              f"{dict(cohort_counts.astype(int))}")
        print(f"  Never-treated controls: "
              f"{(~is_mandate).groupby(v['state']).any().sum()}")

    print("\nDone.")


if __name__ == "__main__":
    main()
