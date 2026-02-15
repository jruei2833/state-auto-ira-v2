# State Auto-IRA 401(k) Dataset Builder
# Usage: python build_dataset.py

import pandas as pd
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "form5500-raw-data")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")
DELIVERABLES_DIR = os.path.join(BASE_DIR, "deliverables")
VALIDATION_DIR = os.path.join(BASE_DIR, "validation")
METHODOLOGY_DIR = os.path.join(BASE_DIR, "methodology")

MANDATE_DATES = {
    "OR": "2017-11-01",
    "IL": "2018-05-01",
    "CA": "2018-11-01",
    "CT": "2022-04-01",
    "MD": "2022-09-01",
    "CO": "2023-01-01",
    "VA": "2023-07-01",
    "ME": "2024-01-01",
    "DE": "2024-01-01",
    "NJ": "2024-03-01",
}

PROGRAM_NAMES = {
    "OR": "OregonSaves",
    "IL": "Secure Choice",
    "CA": "CalSavers",
    "CT": "MyCTSavings",
    "MD": "MarylandSaves",
    "CO": "SecureSavings",
    "VA": "RetirePath",
    "ME": "Maine Retirement Savings",
    "DE": "EARNS",
    "NJ": "RetireReady NJ",
}

YEARS = range(2017, 2025)

# Column mappings with correct entity code values
# Form 5500: single-employer = 2
F5500_COLS = {
    "pension": "TYPE_PENSION_BNFT_CODE",
    "entity": "TYPE_PLAN_ENTITY_CD",
    "entity_value": ["2", "2.0"],
    "date": "PLAN_EFF_DATE",
    "state": "SPONS_DFE_MAIL_US_STATE",
    "ein": "SPONS_DFE_EIN",
    "name": "SPONSOR_DFE_NAME",
    "city": "SPONS_DFE_MAIL_US_CITY",
    "plan_name": "PLAN_NAME",
    "participants": "TOT_PARTCP_BOY_CNT",
}

# Form 5500-SF: single-employer = 1
F5500SF_COLS = {
    "pension": "SF_TYPE_PENSION_BNFT_CODE",
    "entity": "SF_PLAN_ENTITY_CD",
    "entity_value": ["1", "1.0"],
    "date": "SF_PLAN_EFF_DATE",
    "state": "SF_SPONS_US_STATE",
    "ein": "SF_SPONS_EIN",
    "name": "SF_SPONSOR_NAME",
    "city": "SF_SPONS_US_CITY",
    "plan_name": "SF_PLAN_NAME",
    "participants": "SF_TOT_PARTCP_BOY_CNT",
}


def ensure_dirs():
    for d in [OUTPUT_DIR, DELIVERABLES_DIR, VALIDATION_DIR, METHODOLOGY_DIR]:
        os.makedirs(d, exist_ok=True)


def find_file(folder, pattern):
    if not os.path.exists(folder):
        return None
    for f in os.listdir(folder):
        if pattern.lower() in f.lower() and f.lower().endswith(".csv"):
            return os.path.join(folder, f)
    return None


def get_col(df, col_name):
    if col_name in df.columns:
        return col_name
    for c in df.columns:
        if c.upper() == col_name.upper():
            return c
    return None


def process_file(filepath, col_map, label):
    print(f"  Loading {label}... ", end="", flush=True)
    df = pd.read_csv(filepath, low_memory=False, encoding="latin1")
    print(f"{len(df):,} rows")

    pension_col = get_col(df, col_map["pension"])
    entity_col = get_col(df, col_map["entity"])
    date_col = get_col(df, col_map["date"])
    state_col = get_col(df, col_map["state"])
    ein_col = get_col(df, col_map["ein"])
    name_col = get_col(df, col_map["name"])
    city_col = get_col(df, col_map["city"])
    plan_name_col = get_col(df, col_map["plan_name"])
    part_col = get_col(df, col_map["participants"])

    missing = []
    if not pension_col:
        missing.append(f"pension ({col_map['pension']})")
    if not date_col:
        missing.append(f"date ({col_map['date']})")
    if not state_col:
        missing.append(f"state ({col_map['state']})")
    if not ein_col:
        missing.append(f"EIN ({col_map['ein']})")
    if missing:
        print(f"  [SKIP] Missing: {', '.join(missing)}")
        return pd.DataFrame()

    # Filter 1: 401(k) plans (code 2J)
    df[pension_col] = df[pension_col].astype(str)
    df = df[df[pension_col].str.contains("2J", na=False)].copy()
    print(f"  After 401(k) filter: {len(df):,}")

    # Filter 2: Single-employer plans (different codes per file type)
    if entity_col:
        entity_values = col_map["entity_value"]
        df[entity_col] = df[entity_col].astype(str).str.strip()
        excluded = len(df) - df[entity_col].isin(entity_values).sum()
        df = df[df[entity_col].isin(entity_values)].copy()
        print(f"  After single-employer filter (code {entity_values[0]}): {len(df):,} ({excluded:,} excluded)")

    # Filter 3: Mandate states
    target_states = list(MANDATE_DATES.keys())
    df[state_col] = df[state_col].astype(str).str.strip().str.upper()
    df = df[df[state_col].isin(target_states)].copy()
    print(f"  After state filter: {len(df):,}")

    if len(df) == 0:
        return pd.DataFrame()

    # Filter 4: Plan effective date after mandate date
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    rows = []
    for state, mandate_str in MANDATE_DATES.items():
        mandate_dt = pd.Timestamp(mandate_str)
        state_df = df[(df[state_col] == state) & (df[date_col] > mandate_dt)]
        if len(state_df) > 0:
            rows.append(state_df)

    if not rows:
        print(f"  After mandate date filter: 0")
        return pd.DataFrame()

    df = pd.concat(rows, ignore_index=True)
    print(f"  After mandate date filter: {len(df):,}")

    # Build standardized output
    output = pd.DataFrame()
    output["EIN"] = df[ein_col].astype(str).str.strip().str.zfill(9)
    if name_col and name_col in df.columns:
        output["FIRM_NAME"] = df[name_col].astype(str).str.strip()
        output.loc[output["FIRM_NAME"].isin(["nan", "NaN", ""]), "FIRM_NAME"] = None
    else:
        output["FIRM_NAME"] = None
    output["PLAN_NAME"] = df[plan_name_col].astype(str).str.strip() if plan_name_col and plan_name_col in df.columns else ""
    output["STATE"] = df[state_col].values
    output["CITY"] = df[city_col].astype(str).str.strip() if city_col and city_col in df.columns else ""
    output["PLAN_EFFECTIVE_DATE"] = df[date_col].values
    if part_col and part_col in df.columns:
        output["EMPLOYEE_COUNT"] = pd.to_numeric(df[part_col], errors="coerce")
    else:
        output["EMPLOYEE_COUNT"] = None
    output["SOURCE"] = label

    return output


def main():
    print("=" * 60)
    print("State Auto-IRA 401(k) Dataset Builder")
    print("=" * 60)

    ensure_dirs()
    all_records = []

    for year in YEARS:
        print(f"\n{'='*40} {year} {'='*40}")

        path = find_file(os.path.join(RAW_DIR, "form5500"), f"f_5500_{year}")
        if path:
            result = process_file(path, F5500_COLS, f"Form5500_{year}")
            if len(result) > 0:
                all_records.append(result)
                print(f"  => {len(result):,} records from Form 5500")

        path = find_file(os.path.join(RAW_DIR, "form5500sf"), f"f_5500_sf_{year}")
        if path:
            result = process_file(path, F5500SF_COLS, f"Form5500SF_{year}")
            if len(result) > 0:
                all_records.append(result)
                print(f"  => {len(result):,} records from Form 5500-SF")

    if not all_records:
        print("\n[ERROR] No records found!")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("COMBINING AND DEDUPLICATING")
    print("=" * 60)

    combined = pd.concat(all_records, ignore_index=True)
    print(f"Total records before dedup: {len(combined):,}")

    combined = combined.sort_values("PLAN_EFFECTIVE_DATE", ascending=False)
    deduped = combined.drop_duplicates(subset=["EIN"], keep="first")
    print(f"Total unique firms (by EIN): {len(deduped):,}")

    # Join employer contribution data
    print(f"\n{'='*60}")
    print("JOINING EMPLOYER CONTRIBUTION DATA")
    print("=" * 60)

    contrib_data = []
    for year in YEARS:
        path = find_file(os.path.join(RAW_DIR, "schedule_h"), f"sch_h_{year}")
        if path:
            print(f"  Loading Schedule H {year}... ", end="", flush=True)
            sch = pd.read_csv(path, low_memory=False, encoding="latin1")
            print(f"{len(sch):,} rows")
            ein_col = contrib_col = None
            for c in sch.columns:
                if "SPONS" in c.upper() and "EIN" in c.upper():
                    ein_col = c
                    break
            if not ein_col:
                for c in sch.columns:
                    if "EIN" in c.upper():
                        ein_col = c
                        break
            for c in sch.columns:
                if "EMPLR" in c.upper() and "CONTRIB" in c.upper():
                    contrib_col = c
                    break
            if ein_col and contrib_col:
                subset = sch[[ein_col, contrib_col]].copy()
                subset.columns = ["EIN", "EMPLOYER_CONTRIBUTION"]
                contrib_data.append(subset)

        path = find_file(os.path.join(RAW_DIR, "schedule_i"), f"sch_i_{year}")
        if path:
            print(f"  Loading Schedule I {year}... ", end="", flush=True)
            sch = pd.read_csv(path, low_memory=False, encoding="latin1")
            print(f"{len(sch):,} rows")
            ein_col = contrib_col = None
            for c in sch.columns:
                if "SPONS" in c.upper() and "EIN" in c.upper():
                    ein_col = c
                    break
            if not ein_col:
                for c in sch.columns:
                    if "EIN" in c.upper():
                        ein_col = c
                        break
            for c in sch.columns:
                if "EMPLR" in c.upper() and "CONTRIB" in c.upper():
                    contrib_col = c
                    break
            if ein_col and contrib_col:
                subset = sch[[ein_col, contrib_col]].copy()
                subset.columns = ["EIN", "EMPLOYER_CONTRIBUTION"]
                contrib_data.append(subset)

    if contrib_data:
        all_contrib = pd.concat(contrib_data, ignore_index=True)
        all_contrib["EIN"] = all_contrib["EIN"].astype(str).str.strip().str.zfill(9)
        all_contrib["EMPLOYER_CONTRIBUTION"] = pd.to_numeric(all_contrib["EMPLOYER_CONTRIBUTION"], errors="coerce")
        all_contrib = all_contrib.dropna(subset=["EMPLOYER_CONTRIBUTION"])
        contrib_by_ein = all_contrib.groupby("EIN")["EMPLOYER_CONTRIBUTION"].last().reset_index()
        before = len(deduped)
        deduped = deduped.merge(contrib_by_ein, on="EIN", how="left")
        matched = deduped["EMPLOYER_CONTRIBUTION"].notna().sum()
        print(f"\n  Matched contributions: {matched:,} / {before:,} ({matched/before*100:.1f}%)")
    else:
        deduped["EMPLOYER_CONTRIBUTION"] = None

    # Save outputs
    print(f"\n{'='*60}")
    print("SAVING OUTPUTS")
    print("=" * 60)

    dataset_path = os.path.join(OUTPUT_DIR, "state_auto_ira_401k_dataset.csv")
    deduped.to_csv(dataset_path, index=False)
    size_mb = os.path.getsize(dataset_path) / (1024 * 1024)
    print(f"  Dataset: {dataset_path}")
    print(f"  {len(deduped):,} rows, {size_mb:.1f} MB")

    summary = []
    print(f"\n  --- State Summary ---")
    for state in sorted(MANDATE_DATES.keys()):
        state_df = deduped[deduped["STATE"] == state]
        count = len(state_df)
        avg_emp = state_df["EMPLOYEE_COUNT"].mean() if count > 0 else 0
        avg_contrib = state_df["EMPLOYER_CONTRIBUTION"].mean() if count > 0 else 0
        summary.append({
            "State": state,
            "Program": PROGRAM_NAMES.get(state, ""),
            "Mandate_Date": MANDATE_DATES[state],
            "Firms_Identified": count,
            "Avg_Employees": round(avg_emp, 1) if pd.notna(avg_emp) else 0,
            "Avg_Employer_Contribution": round(avg_contrib, 2) if pd.notna(avg_contrib) else 0,
        })
        print(f"  {state:2s} | {PROGRAM_NAMES.get(state, ''):25s} | {count:>7,} firms")

    summary_df = pd.DataFrame(summary)
    summary_path = os.path.join(DELIVERABLES_DIR, "summary_statistics.csv")
    summary_df.to_csv(summary_path, index=False)

    total = len(deduped)
    states_with_data = sum(1 for s in summary if s["Firms_Identified"] > 0)

    methodology_path = os.path.join(METHODOLOGY_DIR, "METHODOLOGY.md")
    with open(methodology_path, "w") as f:
        f.write("# Methodology: State Auto-IRA 401(k) Dataset\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Data Source\n")
        f.write("DOL Form 5500 bulk datasets (2017-2024) from EFAST2 system.\n\n")
        f.write("## Filtering Criteria\n")
        f.write("1. TYPE_PENSION_BNFT_CODE contains '2J' (401(k) plans)\n")
        f.write("2. Single-employer plans (Form 5500: entity code 2, Form 5500-SF: entity code 1)\n")
        f.write("3. State is one of the 10 mandate states\n")
        f.write("4. PLAN_EFF_DATE is after the state mandate date\n")
        f.write("5. Deduplicated by EIN for unique firms\n\n")
        f.write("## State Mandate Dates\n")
        f.write("| State | Program | Mandate Date |\n|-------|---------|-------------|\n")
        for state in sorted(MANDATE_DATES.keys()):
            f.write(f"| {state} | {PROGRAM_NAMES.get(state, '')} | {MANDATE_DATES[state]} |\n")
        f.write(f"\n## Results\n- Total unique firms: {total:,}\n- States with data: {states_with_data}\n")

    validation_path = os.path.join(VALIDATION_DIR, "cross_validation_report.md")
    with open(validation_path, "w") as f:
        f.write("# Cross-Validation Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"- Total unique firms: {total:,}\n- Generated by: build_dataset.py\n\n")
        f.write("## State Breakdown\n| State | Firms |\n|-------|-------|\n")
        for s in summary:
            f.write(f"| {s['State']} | {s['Firms_Identified']:,} |\n")

    final_path = os.path.join(DELIVERABLES_DIR, "FINAL_SUMMARY.md")
    with open(final_path, "w") as f:
        f.write("# State Auto-IRA Research: Final Summary\n\n")
        f.write(f"**{total:,} unique firms** across {states_with_data} states established 401(k) plans\n")
        f.write("after their state's auto-IRA mandate took effect.\n\n")
        f.write("| State | Program | Firms |\n|-------|---------|-------|\n")
        for s in sorted(summary, key=lambda x: x["Firms_Identified"], reverse=True):
            f.write(f"| {s['State']} | {s['Program']} | {s['Firms_Identified']:,} |\n")

    print(f"\n{'='*60}")
    print(f"DONE! {total:,} unique firms across {states_with_data} states")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  git add -A")
    print(f'  git commit -m "Add dataset and all deliverables"')
    print(f"  git push origin master")


if __name__ == "__main__":
    main()
