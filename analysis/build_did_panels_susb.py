"""Build SUSB-denominator DiD panels (v1-inclusive and v2-conservative).

This is a parallel pipeline to build_did_panels.py — the difference is that
the denominator switches from CBP establishments to SUSB firm counts.

Two new outcome columns are produced:

    new_401k_per_1000_firms        — denominator: SUSB total firms (all sizes)
    new_401k_per_1000_firms_5plus  — denominator: SUSB firms with 5+ employees
                                      (the policy-relevant population for most
                                       state mandates: CT/IL/MD/CO/OR-2023+/VA-25+)

For 2023 and 2024 (years SUSB has not yet released) we carry forward the 2022
firm count, matching how CBP handles the same release-lag issue. The
forward-fill is documented and the impact on the final ATT estimate is
typically small because most identifying variation comes from pre-2023.

Inputs:
    analysis/state_year_new_401k.csv
    analysis/cbp_state_year.csv  (kept for cross-reference and CBP-based outcomes)
    data/census_susb/state_year_firms_by_size.csv

Outputs:
    analysis/did_panel_susb_v1_inclusive.csv
    analysis/did_panel_susb_v2_conservative.csv
"""

import math
import os

import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
SUSB_PATH = os.path.join(os.path.dirname(BASE), "data", "census_susb",
                          "state_year_firms_by_size.csv")
CBP_PATH = os.path.join(BASE, "cbp_state_year.csv")
COUNTS_PATH = os.path.join(BASE, "state_year_new_401k.csv")

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
    if state not in mandate_dates:
        return math.inf
    return pd.Timestamp(mandate_dates[state]).year


def make_susb_wide(susb: pd.DataFrame) -> pd.DataFrame:
    """Pivot SUSB long -> wide with one row per state-year.

    Columns produced:
        susb_firms_all
        susb_firms_5plus  (sum of 5-9, 10-19, 20-99, 100-499, 500+)
        susb_firms_5_9, susb_firms_10_19, ... susb_firms_500plus
        susb_estabs_all  (cross-reference vs CBP)
    """
    BIN_SUFFIX = {
        "all": "all", "0-4": "0_4", "5-9": "5_9", "10-19": "10_19",
        "20-99": "20_99", "100-499": "100_499", "500+": "500plus",
    }

    firms = susb.pivot(index=["state", "year"], columns="size_class",
                        values="firm_count")
    estabs = susb.pivot(index=["state", "year"], columns="size_class",
                         values="establishment_count")

    out = pd.DataFrame(index=firms.index)
    for src, suf in BIN_SUFFIX.items():
        if src in firms.columns:
            out[f"susb_firms_{suf}"] = firms[src]
        if src in estabs.columns:
            out[f"susb_estabs_{suf}"] = estabs[src]

    # 5+ aggregate (sum of 5-9, 10-19, 20-99, 100-499, 500+)
    out["susb_firms_5plus"] = out[[
        "susb_firms_5_9", "susb_firms_10_19", "susb_firms_20_99",
        "susb_firms_100_499", "susb_firms_500plus",
    ]].sum(axis=1)
    out["susb_estabs_5plus"] = out[[
        "susb_estabs_5_9", "susb_estabs_10_19", "susb_estabs_20_99",
        "susb_estabs_100_499", "susb_estabs_500plus",
    ]].sum(axis=1)

    # Verify: susb_firms_all ~= susb_firms_0_4 + susb_firms_5plus.
    # SUSB doesn't always reconcile to the dollar (rounding), so allow 0.5%
    # tolerance.
    check = out["susb_firms_all"] - (out["susb_firms_0_4"] + out["susb_firms_5plus"])
    if (check.abs() / out["susb_firms_all"].clip(lower=1) > 0.005).any():
        bad = check[(check.abs() / out["susb_firms_all"].clip(lower=1) > 0.005)]
        print(f"WARNING: SUSB total != 0-4 + 5+ for {len(bad)} state-years; "
              f"largest deviation: {check.abs().max():.0f} firms")

    return out.reset_index()


def carry_forward_susb(susb_wide: pd.DataFrame, all_years: list[int]) -> pd.DataFrame:
    """Extend SUSB to cover all_years by carrying forward the last available year.

    SUSB lag means 2023+ are typically unavailable. We forward-fill within
    state. This matches how CBP handles its release lag.
    """
    states = sorted(susb_wide["state"].unique())
    grid = pd.MultiIndex.from_product([states, all_years],
                                        names=["state", "year"]).to_frame(index=False)
    out = grid.merge(susb_wide, on=["state", "year"], how="left")
    out = out.sort_values(["state", "year"])
    fill_cols = [c for c in out.columns if c.startswith("susb_")]
    out[fill_cols] = out.groupby("state")[fill_cols].ffill().bfill()
    return out


def main():
    susb = pd.read_csv(SUSB_PATH)
    cbp = pd.read_csv(CBP_PATH)
    counts = pd.read_csv(COUNTS_PATH)

    panel_years = sorted(counts["year"].unique())
    print(f"Panel years: {panel_years}")

    susb_wide = make_susb_wide(susb)
    susb_wide = carry_forward_susb(susb_wide, panel_years)

    # Drop DC: not present in main DiD panel (CBP carries it but state list
    # used downstream excludes it). We'll keep DC if it appears in the main
    # panel; otherwise drop.
    valid_states = set(counts["state"].unique())
    susb_wide = susb_wide[susb_wide["state"].isin(valid_states)].copy()

    base = counts.merge(cbp, on=["state", "year"], how="left")
    base = base.merge(susb_wide, on=["state", "year"], how="left")

    # CBP-based outcomes (kept for parallel sanity)
    base["rate_per_1000_estabs"] = (
        base["new_401k_plans"] / base["establishments"] * 1000
    )
    base["esrp_rate_per_1000_estabs"] = (
        base["new_esrp_plans"] / base["establishments"] * 1000
    )
    base["with_employees_rate_per_1000_estabs"] = (
        base["new_401k_with_employees"] / base["establishments"] * 1000
    )

    # SUSB-based outcomes
    base["new_401k_per_1000_firms"] = (
        base["new_401k_plans"] / base["susb_firms_all"] * 1000
    )
    base["new_401k_per_1000_firms_5plus"] = (
        base["new_401k_plans"] / base["susb_firms_5plus"] * 1000
    )
    base["new_401k_with_employees_per_1000_firms"] = (
        base["new_401k_with_employees"] / base["susb_firms_all"] * 1000
    )
    base["new_401k_with_employees_per_1000_firms_5plus"] = (
        base["new_401k_with_employees"] / base["susb_firms_5plus"] * 1000
    )
    base["esrp_rate_per_1000_firms"] = (
        base["new_esrp_plans"] / base["susb_firms_all"] * 1000
    )

    for version, mandate_dates in VERSIONS.items():
        v = base.copy()
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

        out_path = os.path.join(BASE, f"did_panel_susb_{version}.csv")
        v.to_csv(out_path, index=False)
        print(f"Wrote {out_path}: {len(v):,} rows, {v['state'].nunique()} states")

        treated_states = sorted(v.loc[is_mandate, "state"].unique())
        print(f"  Treated states: {treated_states}")
        print("  CBP rate vs SUSB rates (treated states, post-mandate average):")
        for st in treated_states:
            sub = v[(v["state"] == st) & (v["treated"] == 1)]
            if len(sub) == 0:
                continue
            print(f"    {st}: CBP={sub['rate_per_1000_estabs'].mean():.2f} | "
                  f"SUSB(all)={sub['new_401k_per_1000_firms'].mean():.2f} | "
                  f"SUSB(5+)={sub['new_401k_per_1000_firms_5plus'].mean():.2f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
