"""Run all DiD specifications on both panels.

For each panel (v1-inclusive, v2-conservative) this produces:

    did_results_<panel>.csv          coefficient table for all specs
    did_event_study_<panel>.csv      event-time aggregation
    did_event_study_<panel>.png      event-study plot with 95% CIs
    did_cohort_effects_<panel>.csv   per-cohort ATT
    did_robustness_<panel>.csv       robustness specifications side-by-side

Specifications run on every panel:
    1. CS — not-yet-treated comparison group  (primary)
    2. CS — never-treated comparison group    (robustness)
    3. TWFE — biased under staggered adoption with heterogeneity, reported as contrast
    4. Event study — dynamic effects, leads & lags

Robustness:
    - Drop California
    - Outcome: 401(k) with positive employees (excludes solo)
    - Outcome: any new ESRP (substitution test)
    - Drop late-treatment states (ME, DE, NJ)

Permutation inference:
    - Randomize treatment assignment among never-treated states; recompute
      simple ATT 200 times; report fraction of placebos exceeding |observed|.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from differences import ATTgt

BASE = os.path.dirname(os.path.abspath(__file__))

PANELS = {
    "v1_inclusive": "did_panel_v1_inclusive.csv",
    "v2_conservative": "did_panel_v2_conservative.csv",
}

OUTCOMES = {
    "rate": "rate_per_1000_estabs",
    "rate_with_emp": "with_employees_rate_per_1000_estabs",
    "rate_esrp": "esrp_rate_per_1000_estabs",
}

ALPHA = 0.05
BOOT = 999  # bootstrap iterations for cluster-robust inference


# ------------------------- helpers -------------------------

@dataclass
class CSFit:
    overall: pd.DataFrame
    event: pd.DataFrame
    cohort: pd.DataFrame
    raw_gt: pd.DataFrame  # group-time ATTs (pre-aggregation)


def fit_cs(df: pd.DataFrame, outcome: str, control_group: str) -> CSFit:
    """Fit Callaway-Sant'Anna group-time ATT and return aggregations.

    Inference is from the wild bootstrap inside `differences` (the package
    bootstraps over the entity dimension by default, which is the
    state-level cluster we want).
    """
    d = df.copy()
    # `differences` requires NaN (not 0) for never-treated cohorts.
    d["cohort"] = d["cohort"].replace(0, np.nan)
    d = d.set_index(["state", "year"])
    model = ATTgt(data=d, cohort_column="cohort")
    model.fit(
        formula=outcome,
        control_group=control_group,
        boot_iterations=BOOT,
        random_state=42,
        progress_bar=False,
    )
    overall = model.aggregate(
        type_of_aggregation="simple",
        boot_iterations=BOOT,
        random_state=42,
    )
    event = model.aggregate(
        type_of_aggregation="event",
        boot_iterations=BOOT,
        random_state=42,
    )
    cohort = model.aggregate(
        type_of_aggregation="cohort",
        boot_iterations=BOOT,
        random_state=42,
    )
    raw_gt = model.results.copy() if isinstance(model.results, pd.DataFrame) else pd.DataFrame()
    return CSFit(overall=overall, event=event, cohort=cohort, raw_gt=raw_gt)


def fit_twfe(df: pd.DataFrame, outcome: str) -> dict:
    """Two-way fixed effects with state + year FE, treatment dummy, clustered SE."""
    formula = f"{outcome} ~ treated + C(state) + C(year)"
    res = smf.ols(formula, data=df).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["state"]},
    )
    return {
        "coef": float(res.params["treated"]),
        "se": float(res.bse["treated"]),
        "ci_lo": float(res.conf_int().loc["treated"][0]),
        "ci_hi": float(res.conf_int().loc["treated"][1]),
        "pval": float(res.pvalues["treated"]),
        "n_obs": int(res.nobs),
    }


def event_study_twfe(df: pd.DataFrame, outcome: str,
                      lead_max: int = 4, lag_max: int = 5) -> pd.DataFrame:
    """TWFE event study with leads/lags (used for the dynamic plot beside CS).

    Includes leads -lead_max..-1 and lags 0..lag_max. Lead -1 is the omitted
    reference category. Never-treated controls have all leads/lags = 0.
    """
    d = df.copy()
    d["et"] = d["event_time"]
    rows = []
    cols_to_add = []
    # Construct dummies for each leads/lags except -1 (reference)
    for k in range(-lead_max, lag_max + 1):
        if k == -1:
            continue
        col = f"et_{'m' if k < 0 else 'p'}{abs(k)}"
        d[col] = ((d["et"].notna()) & (d["et"] == k)).astype(int)
        cols_to_add.append((k, col))
    formula = (f"{outcome} ~ "
               + " + ".join(c for _, c in cols_to_add)
               + " + C(state) + C(year)")
    res = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["state"]}
    )
    for k, col in cols_to_add:
        rows.append({
            "event_time": k,
            "coef": float(res.params.get(col, np.nan)),
            "se": float(res.bse.get(col, np.nan)),
            "ci_lo": float(res.conf_int().loc[col][0]) if col in res.conf_int().index else np.nan,
            "ci_hi": float(res.conf_int().loc[col][1]) if col in res.conf_int().index else np.nan,
        })
    rows.append({"event_time": -1, "coef": 0.0, "se": 0.0,
                 "ci_lo": 0.0, "ci_hi": 0.0})
    return pd.DataFrame(rows).sort_values("event_time").reset_index(drop=True)


def permutation_inference(df: pd.DataFrame, outcome: str, observed: float,
                           n_iter: int = 200, seed: int = 13) -> dict:
    """Randomize treatment among never-treated states; recompute TWFE ATT."""
    rng = np.random.default_rng(seed)
    real_treated = df.loc[df["cohort"] != 0, ["state", "cohort"]].drop_duplicates()
    cohort_pattern = real_treated["cohort"].value_counts().to_dict()
    never_treated_states = sorted(df.loc[df["cohort"] == 0, "state"].unique())
    placebo_atts = []
    for _ in range(n_iter):
        sampled = rng.choice(never_treated_states,
                             size=sum(cohort_pattern.values()),
                             replace=False)
        assignment = {}
        i = 0
        for cohort_year, n in cohort_pattern.items():
            for _ in range(n):
                assignment[sampled[i]] = int(cohort_year)
                i += 1
        d = df.copy()
        # Wipe real treatment
        d = d[~d["state"].isin(real_treated["state"])].copy()
        d["cohort_p"] = d["state"].map(assignment).fillna(0).astype(int)
        d["treated_p"] = ((d["cohort_p"] != 0)
                           & (d["year"] >= d["cohort_p"])).astype(int)
        try:
            res = smf.ols(f"{outcome} ~ treated_p + C(state) + C(year)", data=d).fit()
            placebo_atts.append(float(res.params["treated_p"]))
        except Exception:
            placebo_atts.append(np.nan)
    placebo_atts = np.array([x for x in placebo_atts if not np.isnan(x)])
    p_two_sided = float(np.mean(np.abs(placebo_atts) >= abs(observed)))
    return {
        "observed_att": observed,
        "placebo_mean": float(np.mean(placebo_atts)),
        "placebo_sd": float(np.std(placebo_atts)),
        "two_sided_p": p_two_sided,
        "n_placebos": int(len(placebo_atts)),
    }


def flatten_attgt(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape a `differences` aggregation result to plain DataFrame.

    `differences` returns a 3-level MultiIndex on the columns of every
    aggregation; we keep only the innermost label (ATT, std_error, lower,
    upper, zero_not_in_cband) for downstream use, and flatten any row
    MultiIndex to a single 'event_time' / 'cohort' / index column.
    """
    out = df.copy()
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [c[-1] for c in out.columns.to_flat_index()]
    if isinstance(out.index, pd.MultiIndex):
        out.index = out.index.to_flat_index()
    out = out.reset_index()
    return out


def attgt_aggrow(agg_result: pd.DataFrame, label: str) -> dict:
    """Pull a single point estimate from an ATTgt simple aggregation."""
    r = flatten_attgt(agg_result)
    row = r.iloc[0]
    return {
        "spec": label,
        "coef": float(row.get("ATT", np.nan)),
        "se": float(row.get("std_error", np.nan)),
        "ci_lo": float(row.get("lower", np.nan)),
        "ci_hi": float(row.get("upper", np.nan)),
        "n_obs": None,
    }


# ------------------------- main per-panel pipeline -------------------------

def run_panel(panel_name: str, panel_path: str):
    print(f"\n{'='*70}\nRunning DiD on panel: {panel_name}\n{'='*70}")
    df = pd.read_csv(os.path.join(BASE, panel_path))
    df["cohort"] = df["cohort"].astype(int)

    out_rows: list[dict] = []
    rob_rows: list[dict] = []

    # ----- Spec 1: CS, not-yet-treated, primary outcome -----
    print("\n[1/8] CS not-yet-treated, primary outcome (rate per 1k estabs)")
    cs_nyt = fit_cs(df, OUTCOMES["rate"], control_group="not_yet_treated")
    out_rows.append({**attgt_aggrow(cs_nyt.overall, "CS: not-yet-treated (primary)"),
                     "outcome": OUTCOMES["rate"]})

    # ----- Spec 2: CS, never-treated -----
    print("[2/8] CS never-treated")
    cs_nt = fit_cs(df, OUTCOMES["rate"], control_group="never_treated")
    out_rows.append({**attgt_aggrow(cs_nt.overall, "CS: never-treated"),
                     "outcome": OUTCOMES["rate"]})

    # ----- Spec 3: TWFE -----
    print("[3/8] TWFE (biased under staggered adoption — for contrast only)")
    twfe = fit_twfe(df, OUTCOMES["rate"])
    out_rows.append({"spec": "TWFE (biased — contrast only)", "outcome": OUTCOMES["rate"],
                     **twfe})

    # ----- Spec 4: TWFE Event study -----
    print("[4/8] TWFE event study (-4..+5)")
    es_twfe = event_study_twfe(df, OUTCOMES["rate"])

    # ----- Spec 5: Drop CA -----
    print("[5/8] Robustness: drop California")
    df_noca = df[df["state"] != "CA"].copy()
    cs_noca = fit_cs(df_noca, OUTCOMES["rate"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_noca.overall, "Drop CA"),
                     "outcome": OUTCOMES["rate"]})

    # ----- Spec 6: Outcome restricted to plans with positive employees -----
    print("[6/8] Robustness: outcome = 401(k) with positive employees")
    cs_emp = fit_cs(df, OUTCOMES["rate_with_emp"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_emp.overall, "Outcome: 401(k) w/ employees"),
                     "outcome": OUTCOMES["rate_with_emp"]})

    # ----- Spec 7: Outcome = ESRP (any pension code, single-employer) -----
    print("[7/8] Robustness: outcome = any ESRP (substitution test)")
    cs_esrp = fit_cs(df, OUTCOMES["rate_esrp"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_esrp.overall, "Outcome: any ESRP"),
                     "outcome": OUTCOMES["rate_esrp"]})

    # ----- Spec 8: Drop late-treatment states (ME, DE, NJ) -----
    print("[8/8] Robustness: drop late-treatment states (ME, DE, NJ)")
    df_nolate = df[~df["state"].isin(["ME", "DE", "NJ"])].copy()
    # If the state had cohort 2024, drop it; remaining cohorts retained.
    cs_nolate = fit_cs(df_nolate, OUTCOMES["rate"], control_group="not_yet_treated")
    rob_rows.append({**attgt_aggrow(cs_nolate.overall, "Drop late-treatment (ME/DE/NJ)"),
                     "outcome": OUTCOMES["rate"]})

    # ----- Permutation inference on the primary CS estimate -----
    print("Running permutation inference (200 iterations)...")
    perm = permutation_inference(df, OUTCOMES["rate"],
                                  observed=out_rows[0]["coef"],
                                  n_iter=200)
    rob_rows.append({"spec": "Permutation 2-sided p (200 iter)",
                     "outcome": OUTCOMES["rate"],
                     "coef": perm["observed_att"],
                     "se": perm["placebo_sd"],
                     "ci_lo": np.nan, "ci_hi": np.nan,
                     "pval": perm["two_sided_p"], "n_obs": perm["n_placebos"]})

    # ----- Persist results -----
    pd.DataFrame(out_rows).to_csv(
        os.path.join(BASE, f"did_results_{panel_name}.csv"), index=False
    )
    pd.DataFrame(rob_rows).to_csv(
        os.path.join(BASE, f"did_robustness_{panel_name}.csv"), index=False
    )

    cs_event = flatten_attgt(cs_nyt.event).rename(
        columns={"relative_period": "event_time"}
    )
    cs_event["spec"] = "CS not-yet-treated"
    es_twfe = es_twfe.copy()
    es_twfe["spec"] = "TWFE event study"
    es_combined = pd.concat([cs_event, es_twfe], ignore_index=True, sort=False)
    es_combined.to_csv(
        os.path.join(BASE, f"did_event_study_{panel_name}.csv"), index=False
    )

    cohort_out = flatten_attgt(cs_nyt.cohort)
    cohort_out.to_csv(
        os.path.join(BASE, f"did_cohort_effects_{panel_name}.csv"), index=False
    )

    # ----- Plot event study -----
    plot_event_study(cs_nyt.event, es_twfe, panel_name)

    print(f"Wrote results, robustness, event study, cohort effects, and plot for {panel_name}")
    return {
        "panel": panel_name,
        "cs_primary": out_rows[0],
        "cs_never": out_rows[1],
        "twfe": out_rows[2],
        "robust": rob_rows,
        "permutation": perm,
        "cohort": cs_nyt.cohort,
        "event_cs": cs_nyt.event,
        "event_twfe": es_twfe,
    }


def plot_event_study(cs_event: pd.DataFrame, twfe_event: pd.DataFrame,
                      panel_name: str):
    fig, ax = plt.subplots(figsize=(9, 5.5))

    cs = flatten_attgt(cs_event).rename(columns={"relative_period": "event_time"})
    cs_et = pd.to_numeric(cs.get("event_time"), errors="coerce")
    cs_coef = pd.to_numeric(cs.get("ATT"), errors="coerce")
    cs_lo = pd.to_numeric(cs.get("lower"), errors="coerce")
    cs_hi = pd.to_numeric(cs.get("upper"), errors="coerce")

    ax.errorbar(cs_et, cs_coef, yerr=[cs_coef - cs_lo, cs_hi - cs_coef],
                fmt="o-", color="#1f77b4", capsize=3,
                label="Callaway-Sant'Anna (not-yet-treated)")

    tw = twfe_event.copy()
    ax.errorbar(tw["event_time"] + 0.15, tw["coef"],
                yerr=[tw["coef"] - tw["ci_lo"], tw["ci_hi"] - tw["coef"]],
                fmt="s--", color="#d62728", capsize=3, alpha=0.6,
                label="TWFE (biased — contrast only)")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(-0.5, color="grey", linewidth=0.8, linestyle=":",
               label="Treatment timing")
    ax.set_xlabel("Years since mandate took effect")
    ax.set_ylabel("Change in new 401(k) plans / 1,000 establishments")
    ax.set_title(f"Event study — {panel_name.replace('_', '-')}")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)

    out = os.path.join(BASE, f"did_event_study_{panel_name}.png")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"  Saved plot: {out}")


def main():
    summaries = {}
    for name, path in PANELS.items():
        summaries[name] = run_panel(name, path)

    # ----- Final cross-panel summary table -----
    rows = []
    for name, s in summaries.items():
        rows.append({"panel": name, **{f"primary_{k}": v
                                         for k, v in s["cs_primary"].items()}})
        rows.append({"panel": name, **{f"never_{k}": v
                                         for k, v in s["cs_never"].items()}})
        rows.append({"panel": name, **{f"twfe_{k}": v
                                         for k, v in s["twfe"].items()}})
    pd.DataFrame(rows).to_csv(os.path.join(BASE, "did_summary_all_panels.csv"),
                              index=False)

    print("\n" + "=" * 70)
    print("DiD analysis complete. Outputs in analysis/.")
    print("=" * 70)


if __name__ == "__main__":
    main()
