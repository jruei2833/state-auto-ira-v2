# Build both dataset versions
# v1-inclusive: legislation/regulation dates (more firms)
# v2-conservative: program launch dates (fewer firms, more defensible)
# Usage: python build_both.py

import pandas as pd
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "form5500-raw-data")

VERSIONS = {
    "v1-inclusive": {
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
    },
    "v2-conservative": {
        "OR": "2017-11-01",
        "IL": "2018-11-01",
        "CA": "2019-07-01",
        "CT": "2022-04-01",
        "MD": "2022-09-01",
        "CO": "2023-01-01",
        "VA": "2023-07-01",
        "ME": "2024-01-01",
        "DE": "2024-07-01",
        "NJ": "2024-06-30",
    },
}

PROGRAM_NAMES = {
    "OR": "OregonSaves", "IL": "Secure Choice", "CA": "CalSavers",
    "CT": "MyCTSavings", "MD": "MarylandSaves", "CO": "SecureSavings",
    "VA": "RetirePath", "ME": "Maine Retirement Savings",
    "DE": "EARNS", "NJ": "RetireReady NJ",
}

YEARS = range(2017, 2025)

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


def load_and_filter_base(filepath, col_map, label):
    """Load file and apply non-date filters. Returns filtered df with standardized columns."""
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

    if not all([pension_col, date_col, state_col, ein_col]):
        print(f"  [SKIP] Missing required columns")
        return pd.DataFrame()

    # Filter: 401(k) plans
    df[pension_col] = df[pension_col].astype(str)
    df = df[df[pension_col].str.contains("2J", na=False)].copy()

    # Filter: Single-employer
    if entity_col:
        df[entity_col] = df[entity_col].astype(str).str.strip()
        df = df[df[entity_col].isin(col_map["entity_value"])].copy()

    # Filter: Mandate states
    target_states = list(VERSIONS["v1-inclusive"].keys())
    df[state_col] = df[state_col].astype(str).str.strip().str.upper()
    df = df[df[state_col].isin(target_states)].copy()

    if len(df) == 0:
        return pd.DataFrame()

    # Parse dates
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # Build standardized output
    output = pd.DataFrame()
    output["EIN"] = df[ein_col].astype(str).str.strip().str.replace('.0', '', regex=False).str.zfill(9)
    output["FIRM_NAME"] = df[name_col].astype(str).str.strip() if name_col and name_col in df.columns else ""
    output["PLAN_NAME"] = df[plan_name_col].astype(str).str.strip() if plan_name_col and plan_name_col in df.columns else ""
    output["STATE"] = df[state_col].values
    output["CITY"] = df[city_col].astype(str).str.strip() if city_col and city_col in df.columns else ""
    output["PLAN_EFFECTIVE_DATE"] = df[date_col].values
    if part_col and part_col in df.columns:
        output["EMPLOYEE_COUNT"] = pd.to_numeric(df[part_col], errors="coerce")
    else:
        output["EMPLOYEE_COUNT"] = None
    output["SOURCE"] = label

    # Clean up nan firm names
    output.loc[output["FIRM_NAME"].isin(["nan", "NaN", ""]), "FIRM_NAME"] = None

    print(f"  => {len(output):,} records (pre-date filter)")
    return output


def apply_mandate_filter(df, mandate_dates):
    """Filter by mandate dates for a specific version."""
    rows = []
    for state, mandate_str in mandate_dates.items():
        mandate_dt = pd.Timestamp(mandate_str)
        state_df = df[(df["STATE"] == state) & (df["PLAN_EFFECTIVE_DATE"] > mandate_dt)]
        if len(state_df) > 0:
            rows.append(state_df)
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def load_contributions():
    """Load Schedule H and I for employer contribution data."""
    print(f"\nLoading employer contribution data...")
    contrib_data = []
    for year in YEARS:
        for sched, folder in [("Schedule H", "schedule_h"), ("Schedule I", "schedule_i")]:
            path = find_file(os.path.join(RAW_DIR, folder), f"sch_{folder.split('_')[1]}_{year}")
            if not path:
                continue
            sch = pd.read_csv(path, low_memory=False, encoding="latin1")
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

    if not contrib_data:
        return pd.DataFrame()

    all_contrib = pd.concat(contrib_data, ignore_index=True)
    all_contrib["EIN"] = all_contrib["EIN"].astype(str).str.strip().str.replace('.0', '', regex=False).str.zfill(9)
    all_contrib["EMPLOYER_CONTRIBUTION"] = pd.to_numeric(all_contrib["EMPLOYER_CONTRIBUTION"], errors="coerce")
    all_contrib = all_contrib.dropna(subset=["EMPLOYER_CONTRIBUTION"])
    return all_contrib.groupby("EIN")["EMPLOYER_CONTRIBUTION"].last().reset_index()


def save_version(deduped, mandate_dates, version_name, contrib_df):
    """Save dataset and supporting files for one version."""
    version_dir = os.path.join(BASE_DIR, "data", version_name)
    os.makedirs(version_dir, exist_ok=True)

    # Join contributions
    if len(contrib_df) > 0:
        deduped = deduped.merge(contrib_df, on="EIN", how="left")
        matched = deduped["EMPLOYER_CONTRIBUTION"].notna().sum()
        print(f"  Contribution match: {matched:,} / {len(deduped):,} ({matched/len(deduped)*100:.1f}%)")
    else:
        deduped["EMPLOYER_CONTRIBUTION"] = None

    # Save dataset
    path = os.path.join(version_dir, "state_auto_ira_401k_dataset.csv")
    deduped.to_csv(path, index=False)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"  Dataset: {path} ({len(deduped):,} rows, {size_mb:.1f} MB)")

    # Summary
    print(f"\n  --- {version_name} State Summary ---")
    summary = []
    for state in sorted(mandate_dates.keys()):
        state_df = deduped[deduped["STATE"] == state]
        count = len(state_df)
        summary.append({"State": state, "Program": PROGRAM_NAMES.get(state, ""),
                        "Mandate_Date": mandate_dates[state], "Firms": count})
        print(f"  {state:2s} | {PROGRAM_NAMES.get(state, ''):25s} | {count:>7,} firms")

    summary_path = os.path.join(version_dir, "summary_statistics.csv")
    pd.DataFrame(summary).to_csv(summary_path, index=False)

    return len(deduped)


def main():
    print("=" * 60)
    print("State Auto-IRA 401(k) — Building BOTH Versions")
    print("=" * 60)

    # Ensure output dirs exist
    for d in ["data/v1-inclusive", "data/v2-conservative", "deliverables", "validation", "methodology"]:
        os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

    # Phase 1: Load all data with base filters (no date filter yet)
    all_records = []
    for year in YEARS:
        print(f"\n{'='*40} {year} {'='*40}")

        path = find_file(os.path.join(RAW_DIR, "form5500"), f"f_5500_{year}")
        if path:
            result = load_and_filter_base(path, F5500_COLS, f"Form5500_{year}")
            if len(result) > 0:
                all_records.append(result)

        path = find_file(os.path.join(RAW_DIR, "form5500sf"), f"f_5500_sf_{year}")
        if path:
            result = load_and_filter_base(path, F5500SF_COLS, f"Form5500SF_{year}")
            if len(result) > 0:
                all_records.append(result)

    if not all_records:
        print("\n[ERROR] No records found!")
        sys.exit(1)

    combined = pd.concat(all_records, ignore_index=True)
    print(f"\nTotal base records (all states, pre-date-filter): {len(combined):,}")

    # Phase 2: Load contributions once
    contrib_df = load_contributions()

    # Phase 3: Build each version
    for version_name, mandate_dates in VERSIONS.items():
        print(f"\n{'='*60}")
        print(f"  BUILDING: {version_name}")
        print(f"{'='*60}")

        filtered = apply_mandate_filter(combined, mandate_dates)
        print(f"  Records after mandate date filter: {len(filtered):,}")

        filtered = filtered.sort_values("PLAN_EFFECTIVE_DATE", ascending=False)
        deduped = filtered.drop_duplicates(subset=["EIN"], keep="first")
        print(f"  Unique firms (by EIN): {len(deduped):,}")

        save_version(deduped.copy(), mandate_dates, version_name, contrib_df)

    # Phase 4: Save shared docs
    methodology_path = os.path.join(BASE_DIR, "methodology", "METHODOLOGY.md")
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
        f.write("## Two Versions\n")
        f.write("- **v1-inclusive**: Uses legislation/regulation dates (more firms)\n")
        f.write("- **v2-conservative**: Uses program launch dates (fewer firms, more defensible)\n")
        f.write("- See data/README.md for full comparison\n")

    print(f"\n{'='*60}")
    print("ALL DONE!")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  git add -A")
    print(f'  git commit -m "Add v1 and v2 datasets with documentation"')
    print(f"  git push origin master --force")


if __name__ == "__main__":
    main()
