"""Run CS-DiD on the SUSB-denominator panels.

This is a parallel run to run_did.py, with two new outcomes:
    new_401k_per_1000_firms        — denominator: SUSB total firms (all sizes)
    new_401k_per_1000_firms_5plus  — denominator: SUSB firms with 5+ employees

For each panel (v1-inclusive, v2-conservative) the same Callaway-Sant'Anna
specification is fit on both denominators, plus robustness checks
(drop-CA, with-employees outcome, drop late-treatment).

The helpers (fit_cs, fit_twfe, permutation_inference, flatten_attgt,
attgt_aggrow) are imported from run_did to keep the spec exactly aligned.

Outputs (per panel):
    analysis/did_results_susb_<panel>.csv
    analysis/did_robustness_susb_<panel>.csv
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

# Import helpers from the existing CBP runner so the methodology is
# identical (same bootstrap iterations, same control_group conventions, same
# random seeds for permutation inference).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_did import (
    fit_cs,
    fit_twfe,
    permutation_inference,
    attgt_aggrow,
    flatten_attgt,
)

BASE = os.path.dirname(os.path.abspath(__file__))

PANELS = {
    "v1_inclusive": "did_panel_susb_v1_inclusive.csv",
    "v2_conservative": "did_panel_susb_v2_conservative.csv",
}

# Two SUSB outcomes — one with all firms as denominator, one with 5+ only.
SUSB_OUTCOMES = {
    "rate_susb_all":   "new_401k_per_1000_firms",
    "rate_susb_5plus": "new_401k_per_1000_firms_5plus",
}

WITH_EMP_OUTCOMES = {
    "rate_susb_all":   "new_401k_with_employees_per_1000_firms",
    "rate_susb_5plus": "new_401k_with_employees_per_1000_firms_5plus",
}


def run_one_outcome(df: pd.DataFrame, outcome_label: str, outcome_col: str,
                     panel_name: str) -> tuple[list, list, dict]:
    """Run CS primary, CS never-treated, TWFE, and robustness for one outcome.

    Returns (out_rows, rob_rows, primary_dict).
    """
    out_rows: list[dict] = []
    rob_rows: list[dict] = []

    print(f"  CS not-yet-treated, primary ({outcome_col})")
    cs_nyt = fit_cs(df, outcome_col, control_group="not_yet_treated")
    primary = {**attgt_aggrow(cs_nyt.overall, f"CS: not-yet-treated ({outcome_label})"),
                "outcome": outcome_col}
    out_rows.append(primary)

    print(f"  CS never-treated ({outcome_col})")
    cs_nt = fit_cs(df, outcome_col, control_group="never_treated")
    out_rows.append({**attgt_aggrow(cs_nt.overall, f"CS: never-treated ({outcome_label})"),
                      "outcome": outcome_col})

    print(f"  TWFE ({outcome_col})")
    twfe = fit_twfe(df, outcome_col)
    out_rows.append({"spec": f"TWFE biased ({outcome_label})", "outcome": outcome_col,
                      **twfe})

    # Robustness 1: drop CA
    print(f"  Drop CA ({outcome_col})")
    df_noca = df[df["state"] != "CA"].copy()
    cs_noca = fit_cs(df_noca, outcome_col, control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_noca.overall, f"Drop CA ({outcome_label})"),
                      "outcome": outcome_col})

    # Robustness 2: with-employees outcome on same denominator
    we_outcome = WITH_EMP_OUTCOMES.get(outcome_label)
    if we_outcome and we_outcome in df.columns:
        print(f"  With-employees ({we_outcome})")
        cs_we = fit_cs(df, we_outcome, control_group="not_yet_treated")
        rob_rows.append({**attgt_aggrow(cs_we.overall,
                                          f"With-employees ({outcome_label})"),
                          "outcome": we_outcome})

    # Robustness 3: drop late-treatment cohort (ME, DE, NJ)
    print(f"  Drop late-treatment ME/DE/NJ ({outcome_col})")
    df_nolate = df[~df["state"].isin(["ME", "DE", "NJ"])].copy()
    cs_nolate = fit_cs(df_nolate, outcome_col, control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_nolate.overall,
                                      f"Drop late-treatment ME/DE/NJ ({outcome_label})"),
                      "outcome": outcome_col})

    # Permutation inference (200 iter) on primary
    print(f"  Permutation inference (200 iter, {outcome_col})")
    perm = permutation_inference(df, outcome_col,
                                  observed=primary["coef"],
                                  n_iter=200)
    rob_rows.append({"spec": f"Permutation 2-sided p ({outcome_label})",
                      "outcome": outcome_col,
                      "coef": perm["observed_att"],
                      "se": perm["placebo_sd"],
                      "ci_lo": np.nan, "ci_hi": np.nan,
                      "pval": perm["two_sided_p"], "n_obs": perm["n_placebos"]})

    return out_rows, rob_rows, {**primary, "perm_p": perm["two_sided_p"]}


def run_panel(panel_name: str, panel_path: str):
    print(f"\n{'='*70}\nSUSB DiD on panel: {panel_name}\n{'='*70}")
    df = pd.read_csv(os.path.join(BASE, panel_path))
    df["cohort"] = df["cohort"].astype(int)

    all_out: list[dict] = []
    all_rob: list[dict] = []

    summaries: dict[str, dict] = {}
    for outcome_label, outcome_col in SUSB_OUTCOMES.items():
        print(f"\n--- Outcome: {outcome_label} ({outcome_col}) ---")
        out_rows, rob_rows, summary = run_one_outcome(
            df, outcome_label, outcome_col, panel_name
        )
        all_out.extend(out_rows)
        all_rob.extend(rob_rows)
        summaries[outcome_label] = summary

    pd.DataFrame(all_out).to_csv(
        os.path.join(BASE, f"did_results_susb_{panel_name}.csv"), index=False
    )
    pd.DataFrame(all_rob).to_csv(
        os.path.join(BASE, f"did_robustness_susb_{panel_name}.csv"), index=False
    )
    print(f"\nWrote did_results_susb_{panel_name}.csv "
          f"and did_robustness_susb_{panel_name}.csv")

    return summaries


def main():
    cross_panel: dict[str, dict] = {}
    for name, path in PANELS.items():
        cross_panel[name] = run_panel(name, path)

    # Cross-panel summary
    print("\n" + "=" * 70)
    print("SUMMARY: SUSB-denominator headline ATTs")
    print("=" * 70)
    rows = []
    for panel_name, panel_summary in cross_panel.items():
        for outcome_label, summary in panel_summary.items():
            rows.append({
                "panel": panel_name,
                "denominator": outcome_label,
                "outcome_col": summary["outcome"],
                "coef": summary["coef"],
                "se": summary["se"],
                "ci_lo": summary["ci_lo"],
                "ci_hi": summary["ci_hi"],
                "perm_p": summary["perm_p"],
            })
            print(f"  {panel_name} | {outcome_label}: "
                  f"ATT={summary['coef']:.3f} "
                  f"({summary['ci_lo']:.3f}, {summary['ci_hi']:.3f}) "
                  f"perm-p={summary['perm_p']:.4f}")
    pd.DataFrame(rows).to_csv(
        os.path.join(BASE, "did_susb_summary.csv"), index=False
    )


if __name__ == "__main__":
    main()
