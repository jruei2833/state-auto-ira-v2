"""Run CS-DiD on the QCEW-denominated outcome.

Reuses the helper functions in run_did.py (fit_cs, fit_twfe,
permutation_inference, attgt_aggrow, flatten_attgt) so the QCEW results are
directly comparable to the CBP headline.

Specifications mirror run_did.py:
    1. CS not-yet-treated, primary outcome           (headline)
    2. CS never-treated                              (robustness)
    3. TWFE                                          (biased contrast only)
    4. Drop California                               (robustness)
    5. Drop late-treatment states (ME, DE, NJ)       (robustness)
    6. Permutation inference                         (200 placebos)

Inputs:
    analysis/did_panel_qcew_v1_inclusive.csv
    analysis/did_panel_qcew_v2_conservative.csv

Outputs:
    analysis/did_results_qcew_v1_inclusive.csv
    analysis/did_results_qcew_v2_conservative.csv
    analysis/did_robustness_qcew_v1_inclusive.csv
    analysis/did_robustness_qcew_v2_conservative.csv

The headline outcome (mirroring rate_per_1000_estabs in the CBP runner) is
new_401k_per_1000_qcew_establishments — the same numerator (new 401(k) plan
formations from Form 5500), divided by QCEW annual-average private
establishments.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

# Reuse the existing CS / TWFE / permutation helpers.
from run_did import (
    fit_cs,
    fit_twfe,
    permutation_inference,
    attgt_aggrow,
    flatten_attgt,
)

BASE = os.path.dirname(os.path.abspath(__file__))

PANELS = {
    "v1_inclusive": "did_panel_qcew_v1_inclusive.csv",
    "v2_conservative": "did_panel_qcew_v2_conservative.csv",
}

# Use the QCEW-denominated outcomes (parallel structure to OUTCOMES in run_did.py).
OUTCOMES = {
    "rate": "new_401k_per_1000_qcew_establishments",
    "rate_with_emp": "with_employees_rate_per_1000_qcew_estabs",
    "rate_esrp": "esrp_rate_per_1000_qcew_estabs",
}


def run_panel(panel_name: str, panel_path: str):
    print(f"\n{'='*70}\nRunning QCEW DiD on panel: {panel_name}\n{'='*70}")
    df = pd.read_csv(os.path.join(BASE, panel_path))
    df["cohort"] = df["cohort"].astype(int)

    # Drop rows missing the QCEW denominator (defensive — in practice all
    # state-year rows should have it after fetch).
    initial_n = len(df)
    df = df.dropna(subset=[OUTCOMES["rate"]])
    if len(df) != initial_n:
        print(f"  Dropped {initial_n - len(df)} rows with missing QCEW denominator")

    out_rows: list[dict] = []
    rob_rows: list[dict] = []

    print("\n[1/6] CS not-yet-treated (primary)")
    cs_nyt = fit_cs(df, OUTCOMES["rate"], control_group="not_yet_treated")
    out_rows.append({**attgt_aggrow(cs_nyt.overall, "CS: not-yet-treated (primary)"),
                     "outcome": OUTCOMES["rate"]})

    print("[2/6] CS never-treated")
    cs_nt = fit_cs(df, OUTCOMES["rate"], control_group="never_treated")
    out_rows.append({**attgt_aggrow(cs_nt.overall, "CS: never-treated"),
                     "outcome": OUTCOMES["rate"]})

    print("[3/6] TWFE (biased — for contrast only)")
    twfe = fit_twfe(df, OUTCOMES["rate"])
    out_rows.append({"spec": "TWFE (biased — contrast only)",
                     "outcome": OUTCOMES["rate"], **twfe})

    print("[4/6] Robustness: drop California")
    df_noca = df[df["state"] != "CA"].copy()
    cs_noca = fit_cs(df_noca, OUTCOMES["rate"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_noca.overall, "Drop CA"),
                     "outcome": OUTCOMES["rate"]})

    print("[5/6] Robustness: outcome = 401(k) with positive employees")
    cs_emp = fit_cs(df, OUTCOMES["rate_with_emp"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_emp.overall, "Outcome: 401(k) w/ employees"),
                     "outcome": OUTCOMES["rate_with_emp"]})

    print("[6/6] Robustness: drop late-treatment states (ME, DE, NJ)")
    df_nolate = df[~df["state"].isin(["ME", "DE", "NJ"])].copy()
    cs_nolate = fit_cs(df_nolate, OUTCOMES["rate"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_nolate.overall, "Drop late-treatment (ME/DE/NJ)"),
                     "outcome": OUTCOMES["rate"]})

    print("Robustness: outcome = any ESRP (substitution test)")
    cs_esrp = fit_cs(df, OUTCOMES["rate_esrp"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_esrp.overall, "Outcome: any ESRP"),
                     "outcome": OUTCOMES["rate_esrp"]})

    print("Permutation inference (200 iterations)...")
    perm = permutation_inference(df, OUTCOMES["rate"],
                                  observed=out_rows[0]["coef"],
                                  n_iter=200)
    rob_rows.append({"spec": "Permutation 2-sided p (200 iter)",
                     "outcome": OUTCOMES["rate"],
                     "coef": perm["observed_att"],
                     "se": perm["placebo_sd"],
                     "ci_lo": np.nan, "ci_hi": np.nan,
                     "pval": perm["two_sided_p"],
                     "n_obs": perm["n_placebos"]})

    pd.DataFrame(out_rows).to_csv(
        os.path.join(BASE, f"did_results_qcew_{panel_name}.csv"), index=False
    )
    pd.DataFrame(rob_rows).to_csv(
        os.path.join(BASE, f"did_robustness_qcew_{panel_name}.csv"), index=False
    )

    print(f"Wrote results and robustness for QCEW {panel_name}")
    return {
        "panel": panel_name,
        "primary": out_rows[0],
        "drop_ca": next(r for r in rob_rows if r["spec"] == "Drop CA"),
        "perm": perm,
    }


def main():
    summaries = {}
    for name, path in PANELS.items():
        summaries[name] = run_panel(name, path)

    print("\n" + "=" * 70)
    print("QCEW DiD complete. Summary:")
    print("=" * 70)
    for name, s in summaries.items():
        primary = s["primary"]
        drop_ca = s["drop_ca"]
        print(f"\n{name}:")
        print(f"  Primary CS (not-yet-treated): "
              f"ATT={primary['coef']:.3f}, SE={primary['se']:.3f}, "
              f"95% CI=[{primary['ci_lo']:.3f}, {primary['ci_hi']:.3f}]")
        print(f"  Drop CA: ATT={drop_ca['coef']:.3f}, "
              f"95% CI=[{drop_ca['ci_lo']:.3f}, {drop_ca['ci_hi']:.3f}]")
        print(f"  Permutation 2-sided p: {s['perm']['two_sided_p']:.4f}")


if __name__ == "__main__":
    main()
