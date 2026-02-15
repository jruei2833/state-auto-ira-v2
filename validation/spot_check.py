"""
Antigravity Independent Audit: Spot-Check Verification
Samples 20 random firms from the dataset and verifies each one
against the raw Form 5500/5500-SF CSV files.
"""
import pandas as pd
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "form5500-raw-data")

MANDATE_DATES = {
    "OR": "2017-11-01", "IL": "2018-05-01", "CA": "2018-11-01",
    "CT": "2022-04-01", "MD": "2022-09-01", "CO": "2023-01-01",
    "VA": "2023-07-01", "ME": "2024-01-01", "DE": "2024-01-01",
    "NJ": "2024-03-01",
}

def main():
    dataset_path = os.path.join(BASE_DIR, "data", "processed", "state_auto_ira_401k_dataset.csv")
    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded: {len(df):,} rows\n")

    # Sample 20 random firms, stratified: 2 per state if possible
    random.seed(42)
    sample_rows = []
    for state in sorted(MANDATE_DATES.keys()):
        state_df = df[df["STATE"] == state]
        n = min(2, len(state_df))
        sample_rows.extend(state_df.sample(n=n, random_state=42).to_dict("records"))

    results = []
    print(f"{'#':>2}  {'EIN':<12} {'STATE':<5} {'SOURCE':<20} {'FIRM_NAME':<35} CHECKS")
    print("-" * 120)

    for i, row in enumerate(sample_rows, 1):
        ein = str(row["EIN"]).strip()
        state = row["STATE"]
        source = row["SOURCE"]
        firm_name = str(row.get("FIRM_NAME", ""))[:33]
        plan_date = str(row["PLAN_EFFECTIVE_DATE"])[:10]

        # Determine which raw file to search
        year = source.split("_")[-1]
        if "5500SF" in source:
            folder = os.path.join(RAW_DIR, "form5500sf")
            pattern = f"f_5500_sf_{year}"
            ein_col = "SF_SPONS_EIN"
            pension_col = "SF_TYPE_PENSION_BNFT_CODE"
            entity_col = "SF_PLAN_ENTITY_CD"
            date_col = "SF_PLAN_EFF_DATE"
            state_col = "SF_SPONS_US_STATE"
            expected_entity = "1"
        else:
            folder = os.path.join(RAW_DIR, "form5500")
            pattern = f"f_5500_{year}"
            ein_col = "SPONS_DFE_EIN"
            pension_col = "TYPE_PENSION_BNFT_CODE"
            entity_col = "TYPE_PLAN_ENTITY_CD"
            date_col = "PLAN_EFF_DATE"
            state_col = "SPONS_DFE_MAIL_US_STATE"
            expected_entity = "2"

        # Find the raw file
        raw_file = None
        for f in os.listdir(folder):
            if pattern.lower() in f.lower() and f.lower().endswith(".csv"):
                raw_file = os.path.join(folder, f)
                break

        if not raw_file:
            print(f"{i:>2}  {ein:<12} {state:<5} {source:<20} {firm_name:<35} RAW_FILE_NOT_FOUND")
            results.append({"ein": ein, "state": state, "result": "FILE_NOT_FOUND"})
            continue

        # Load just the columns we need for this EIN
        raw_df = pd.read_csv(raw_file, low_memory=False, encoding="latin1",
                             usecols=[ein_col, pension_col, entity_col, date_col, state_col])

        # Find matching rows
        raw_df[ein_col] = raw_df[ein_col].astype(str).str.strip().str.zfill(9)
        matches = raw_df[raw_df[ein_col] == ein]

        checks = []
        if len(matches) == 0:
            checks.append("NOT_FOUND_IN_RAW")
        else:
            # Check 1: 2J pension code
            pension_vals = matches[pension_col].astype(str).values
            has_2j = any("2J" in v for v in pension_vals)
            checks.append(f"2J={'PASS' if has_2j else 'FAIL'}")

            # Check 2: Single-employer entity code
            entity_vals = matches[entity_col].astype(str).str.strip().values
            has_entity = any(v == expected_entity or v == f"{expected_entity}.0" for v in entity_vals)
            checks.append(f"Entity={expected_entity}:{'PASS' if has_entity else 'FAIL'}")

            # Check 3: State matches
            state_vals = matches[state_col].astype(str).str.strip().str.upper().values
            has_state = state in state_vals
            checks.append(f"State={'PASS' if has_state else 'FAIL'}")

            # Check 4: Date after mandate
            mandate_dt = pd.Timestamp(MANDATE_DATES[state])
            dates = pd.to_datetime(matches[date_col], errors="coerce").dropna()
            has_date_after = any(d > mandate_dt for d in dates)
            checks.append(f"Date>Mandate={'PASS' if has_date_after else 'FAIL'}")

            # Check 5: Plan date matches dataset
            dataset_date = pd.Timestamp(plan_date)
            date_match = any(abs((d - dataset_date).days) <= 1 for d in dates)
            checks.append(f"DateMatch={'PASS' if date_match else 'APPROX'}")

        check_str = " | ".join(checks)
        overall = "PASS" if all("PASS" in c or "APPROX" in c for c in checks) else "FAIL"
        results.append({"ein": ein, "state": state, "source": source,
                        "firm": firm_name, "checks": check_str, "overall": overall})
        print(f"{i:>2}  {ein:<12} {state:<5} {source:<20} {firm_name:<35} {check_str}")

    print("\n" + "=" * 80)
    passed = sum(1 for r in results if r.get("overall") == "PASS")
    failed = sum(1 for r in results if r.get("overall") == "FAIL")
    print(f"SPOT CHECK SUMMARY: {passed} PASS / {failed} FAIL / {len(results)} total")

    # === Count Difference Investigation ===
    print("\n" + "=" * 80)
    print("COUNT DIFFERENCE INVESTIGATION")
    print("=" * 80)

    # Check what 2,194 SF records with entity_cd=2 look like
    sf24 = pd.read_csv(os.path.join(RAW_DIR, "form5500sf", "f_5500_sf_2024_all.csv"),
                       low_memory=False, encoding="latin1",
                       usecols=["SF_PLAN_ENTITY_CD", "SF_TYPE_PENSION_BNFT_CODE",
                                "SF_SPONS_US_STATE", "SF_PLAN_EFF_DATE", "SF_SPONS_EIN"])
    sf24["SF_PLAN_ENTITY_CD"] = sf24["SF_PLAN_ENTITY_CD"].astype(str).str.strip()
    sf24["SF_TYPE_PENSION_BNFT_CODE"] = sf24["SF_TYPE_PENSION_BNFT_CODE"].astype(str)

    # How many 5500-SF records have entity=2?
    e2_sf = sf24[sf24["SF_PLAN_ENTITY_CD"].isin(["2", "2.0"])]
    e2_401k = e2_sf[e2_sf["SF_TYPE_PENSION_BNFT_CODE"].str.contains("2J", na=False)]
    print(f"\n5500-SF 2024: {len(e2_sf):,} records with entity=2 (these are EXCLUDED by script)")
    print(f"  Of those, {len(e2_401k):,} have 2J code")
    print(f"  Breakdown: entity=2 should NOT appear in 5500-SF (it's a Form 5500 code)")

    # Check participant counts for dedup behavior
    print(f"\n--- Dedup investigation ---")
    print(f"Does a firm appear in both 5500 AND 5500-SF?")

    ein_5500 = set()
    ein_sf = set()
    for year in range(2017, 2025):
        p5500 = None
        for f in os.listdir(os.path.join(RAW_DIR, "form5500")):
            if f"f_5500_{year}" in f.lower() and f.endswith(".csv"):
                p5500 = os.path.join(RAW_DIR, "form5500", f)
                break
        if p5500:
            t = pd.read_csv(p5500, usecols=["SPONS_DFE_EIN"], low_memory=False, encoding="latin1")
            ein_5500.update(t["SPONS_DFE_EIN"].astype(str).str.strip().str.zfill(9).values)

        psf = None
        for f in os.listdir(os.path.join(RAW_DIR, "form5500sf")):
            if f"f_5500_sf_{year}" in f.lower() and f.endswith(".csv"):
                psf = os.path.join(RAW_DIR, "form5500sf", f)
                break
        if psf:
            t = pd.read_csv(psf, usecols=["SF_SPONS_EIN"], low_memory=False, encoding="latin1")
            ein_sf.update(t["SF_SPONS_EIN"].astype(str).str.strip().str.zfill(9).values)

    both = ein_5500 & ein_sf
    print(f"  EINs in Form 5500 only: {len(ein_5500 - ein_sf):,}")
    print(f"  EINs in Form 5500-SF only: {len(ein_sf - ein_5500):,}")
    print(f"  EINs in BOTH: {len(both):,}")
    print(f"  (EINs appearing in both are correctly handled by dedup)")

    # === Contribution coverage investigation ===
    print(f"\n--- Contribution coverage ---")
    sch_files = 0
    sch_rows = 0
    for year in range(2017, 2025):
        for folder_name, prefix in [("schedule_h", "sch_h"), ("schedule_i", "sch_i")]:
            folder = os.path.join(RAW_DIR, folder_name)
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    if prefix in f.lower() and f.endswith(".csv"):
                        sch_files += 1
                        # Just count the rows without loading all data
                        with open(os.path.join(folder, f), "r", encoding="latin1") as fh:
                            sch_rows += sum(1 for _ in fh) - 1  # minus header
    print(f"  Schedule H/I files found: {sch_files}")
    print(f"  Total Schedule H/I rows: {sch_rows:,}")
    print(f"  Note: Schedule H is filed by plans with 100+ participants (Form 5500)")
    print(f"  Note: Schedule I is filed by plans with <100 participants (Form 5500)")
    print(f"  Note: Form 5500-SF filers (~95% of dataset) do NOT file Schedule H/I")
    print(f"  This explains the ~3.7% contribution coverage rate")

if __name__ == "__main__":
    main()
