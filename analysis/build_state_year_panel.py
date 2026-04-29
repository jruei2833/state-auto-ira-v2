"""Build state-year panel of new 401(k) plan formations from Form 5500 + 5500-SF.

Mirrors the filters in ../build_dataset.py but keeps all 50 states (+ DC) so we
can use non-mandate states as a comparison group in the DiD design.

Outputs:
    analysis/state_year_new_401k.csv
        state, year, new_401k_plans, new_401k_with_employees,
        new_401k_with_contrib, new_esrp_plans  (any pension code, single-employer)

The "year" is the calendar year of the plan effective date (PLAN_EFF_DATE),
not the filing year of the 5500. Effective dates can be later than the filing
year (e.g., a 2024 filing for a plan effective 2025-08), which is why we
aggregate on the effective date.
"""

import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "form5500-raw-data")
OUT_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(OUT_DIR, exist_ok=True)

YEARS = range(2017, 2025)

F5500_COLS = {
    "pension": "TYPE_PENSION_BNFT_CODE",
    "entity": "TYPE_PLAN_ENTITY_CD",
    "entity_value": ["2", "2.0"],
    "date": "PLAN_EFF_DATE",
    "state": "SPONS_DFE_MAIL_US_STATE",
    "ein": "SPONS_DFE_EIN",
    "participants": "TOT_PARTCP_BOY_CNT",
}

F5500SF_COLS = {
    "pension": "SF_TYPE_PENSION_BNFT_CODE",
    "entity": "SF_PLAN_ENTITY_CD",
    "entity_value": ["1", "1.0"],
    "date": "SF_PLAN_EFF_DATE",
    "state": "SF_SPONS_US_STATE",
    "ein": "SF_SPONS_EIN",
    "participants": "SF_TOT_PARTCP_BOY_CNT",
}

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH",
    "NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT",
    "VT","VA","WA","WV","WI","WY",
}


def find_file(folder, pattern):
    if not os.path.exists(folder):
        return None
    for f in os.listdir(folder):
        if pattern.lower() in f.lower() and f.lower().endswith(".csv"):
            return os.path.join(folder, f)
    return None


def get_col(df, name):
    if name in df.columns:
        return name
    upper = name.upper()
    for c in df.columns:
        if c.upper() == upper:
            return c
    return None


def load_one(filepath, col_map, label):
    """Load + filter one Form 5500 / 5500-SF file. Returns df with columns:
    state, eff_date, ein, participants, is_401k, is_single_employer.
    """
    print(f"  Loading {label}... ", end="", flush=True)
    cols_needed = [col_map["pension"], col_map["entity"], col_map["date"],
                   col_map["state"], col_map["ein"], col_map["participants"]]
    # First read just header to find actual column names (case may differ)
    head = pd.read_csv(filepath, nrows=0, encoding="latin1")
    actual = {k: get_col(head, v) for k, v in col_map.items()
              if k not in ("entity_value",)}
    if not all([actual["pension"], actual["entity"], actual["date"],
                actual["state"], actual["ein"]]):
        print(f"  [SKIP] missing required columns: {actual}")
        return pd.DataFrame()

    use_cols = [v for v in actual.values() if v]
    df = pd.read_csv(filepath, usecols=use_cols, low_memory=False, encoding="latin1")
    print(f"{len(df):,} rows")

    pension = actual["pension"]
    entity = actual["entity"]
    date_c = actual["date"]
    state_c = actual["state"]
    ein_c = actual["ein"]
    part_c = actual["participants"]

    df[pension] = df[pension].astype(str)
    df[entity] = df[entity].astype(str).str.strip()
    df[state_c] = df[state_c].astype(str).str.strip().str.upper()
    df[date_c] = pd.to_datetime(df[date_c], errors="coerce")

    df = df[df[state_c].isin(VALID_STATES)]
    df = df.dropna(subset=[date_c])
    df = df.dropna(subset=[ein_c])

    is_401k = df[pension].str.contains("2J", na=False)
    is_se = df[entity].isin(col_map["entity_value"])

    out = pd.DataFrame({
        "state": df[state_c].values,
        "eff_date": df[date_c].values,
        "ein": df[ein_c].astype(str).str.strip()
                  .str.replace(".0", "", regex=False).str.zfill(9).values,
        "participants": pd.to_numeric(df[part_c], errors="coerce").values
                        if part_c else None,
        "is_401k": is_401k.values,
        "is_single_employer": is_se.values,
        "source": label,
    })
    return out


def main():
    print("=" * 60)
    print("Building state-year panel of new 401(k) formations")
    print("=" * 60)

    frames = []
    for year in YEARS:
        print(f"\n--- {year} ---")
        p = find_file(os.path.join(RAW_DIR, "form5500"), f"f_5500_{year}_all")
        if p:
            frames.append(load_one(p, F5500_COLS, f"F5500_{year}"))
        p = find_file(os.path.join(RAW_DIR, "form5500sf"), f"f_5500_sf_{year}_all")
        if p:
            frames.append(load_one(p, F5500SF_COLS, f"F5500SF_{year}"))

    if not frames:
        print("\n[ERROR] no data loaded")
        sys.exit(1)

    full = pd.concat(frames, ignore_index=True)
    print(f"\nCombined records (all single-employer + multi, all pension types): {len(full):,}")

    # Restrict to single-employer only (the policy-relevant population for
    # auto-IRA mandates — multiple-employer / DFE plans aren't decided by
    # individual firms).
    full = full[full["is_single_employer"]].copy()
    print(f"Single-employer only: {len(full):,}")

    # Keep first effective-date observation per EIN to count "new" plans.
    # Some EINs file multiple times per year; we want the entity-level
    # establishment event, not an annual filing.
    full = full.sort_values("eff_date")
    first_obs = full.drop_duplicates(subset=["ein"], keep="first").copy()
    print(f"Unique EINs (first effective date): {len(first_obs):,}")

    first_obs["eff_year"] = pd.to_datetime(first_obs["eff_date"]).dt.year

    # Restrict effective year to study window
    panel_window = first_obs[
        (first_obs["eff_year"] >= 2017) & (first_obs["eff_year"] <= 2024)
    ].copy()
    print(f"Effective year 2017-2024: {len(panel_window):,}")

    # ----- aggregations -----
    # 1. New 401(k) plans (pension code 2J, single-employer)
    k401 = panel_window[panel_window["is_401k"]]

    # 2. New 401(k) with positive employee count (excludes solo / 0-employee)
    k401_emp = k401[k401["participants"].fillna(0) > 0]

    # 3. New ESRP (any pension code, single-employer) — ESRP fallback uses the
    #    full single-employer universe since pension code is broad.
    esrp = panel_window  # already single-employer

    by_state_year = lambda d: (d.groupby(["state", "eff_year"]).size()
                                 .reset_index(name="n"))

    a = by_state_year(k401).rename(columns={"n": "new_401k_plans"})
    b = by_state_year(k401_emp).rename(columns={"n": "new_401k_with_employees"})
    c = by_state_year(esrp).rename(columns={"n": "new_esrp_plans"})

    # Build full state-year grid (so zeros are explicit, not missing)
    grid = pd.MultiIndex.from_product(
        [sorted(VALID_STATES), list(range(2017, 2025))],
        names=["state", "eff_year"],
    ).to_frame(index=False)

    panel = (grid.merge(a, on=["state", "eff_year"], how="left")
                 .merge(b, on=["state", "eff_year"], how="left")
                 .merge(c, on=["state", "eff_year"], how="left")
                 .fillna(0))
    for col in ["new_401k_plans", "new_401k_with_employees", "new_esrp_plans"]:
        panel[col] = panel[col].astype(int)
    panel = panel.rename(columns={"eff_year": "year"})

    out_path = os.path.join(OUT_DIR, "state_year_new_401k.csv")
    panel.to_csv(out_path, index=False)
    print(f"\nWrote {out_path}: {len(panel):,} state-year rows")

    # Quick sanity check
    mandate = ["OR","IL","CA","CT","MD","CO","VA","ME","DE","NJ"]
    print("\nMandate-state totals (2017-2024 effective dates, single-employer 401(k)):")
    for s in mandate:
        n = panel[panel["state"] == s]["new_401k_plans"].sum()
        print(f"  {s}: {n:,}")
    print(f"  All other states: {panel[~panel['state'].isin(mandate)]['new_401k_plans'].sum():,}")


if __name__ == "__main__":
    main()
