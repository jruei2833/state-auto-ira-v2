"""
Audit script for the State Auto-IRA 401(k) dataset.
Validates data quality, filtering correctness, and consistency.
"""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "state_auto_ira_401k_dataset.csv")

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

PREVIOUS_COUNTS = {
    "CA": 79485, "IL": 14035, "OR": 7015, "MD": 3464,
    "CO": 2630, "CT": 2332, "VA": 2054, "NJ": 783,
    "DE": 207, "ME": 137,
}

def main():
    print("=" * 70)
    print("STATE AUTO-IRA DATASET AUDIT")
    print("=" * 70)

    df = pd.read_csv(DATASET_PATH)
    df["PLAN_EFFECTIVE_DATE"] = pd.to_datetime(df["PLAN_EFFECTIVE_DATE"])
    total = len(df)
    print(f"\nDataset: {DATASET_PATH}")
    print(f"Total rows: {total:,}")
    print(f"Columns: {list(df.columns)}")

    # ---- CHECK 1: All plan dates after mandate dates ----
    print(f"\n{'=' * 70}")
    print("CHECK 1: All plan effective dates fall AFTER state mandate dates")
    print("=" * 70)
    all_pass = True
    for state in sorted(MANDATE_DATES.keys()):
        mandate_dt = pd.Timestamp(MANDATE_DATES[state])
        state_df = df[df["STATE"] == state]
        bad = state_df[state_df["PLAN_EFFECTIVE_DATE"] <= mandate_dt]
        if len(bad) > 0:
            all_pass = False
            print(f"  FAIL  {state}: {len(bad)} records on or before {MANDATE_DATES[state]}")
        else:
            earliest = state_df["PLAN_EFFECTIVE_DATE"].min()
            print(f"  PASS  {state}: {len(state_df):>6,} records | earliest: {earliest.date()} (mandate: {MANDATE_DATES[state]})")
    print(f"\n  Result: {'PASS' if all_pass else 'FAIL'}")

    # ---- CHECK 2: EIN uniqueness (deduplication) ----
    print(f"\n{'=' * 70}")
    print("CHECK 2: EIN deduplication (each EIN appears exactly once)")
    print("=" * 70)
    dup_count = df.duplicated(subset=["EIN"]).sum()
    unique_eins = df["EIN"].nunique()
    print(f"  Total rows:   {total:,}")
    print(f"  Unique EINs:  {unique_eins:,}")
    print(f"  Duplicate rows: {dup_count:,}")
    if dup_count == 0:
        print(f"\n  Result: PASS")
    else:
        print(f"\n  Result: FAIL - {dup_count} duplicate EINs found")
        # Show a few duplicates
        dup_eins = df[df.duplicated(subset=["EIN"], keep=False)]["EIN"].unique()[:5]
        for ein in dup_eins:
            rows = df[df["EIN"] == ein]
            print(f"    EIN {ein}: {len(rows)} rows in states {list(rows['STATE'].unique())}")

    # ---- CHECK 3: Only valid states ----
    print(f"\n{'=' * 70}")
    print("CHECK 3: Only mandate states present")
    print("=" * 70)
    valid_states = set(MANDATE_DATES.keys())
    actual_states = set(df["STATE"].unique())
    unexpected = actual_states - valid_states
    if not unexpected:
        print(f"  PASS: All {len(actual_states)} states are valid mandate states")
    else:
        print(f"  FAIL: Unexpected states found: {unexpected}")
    print(f"  States: {sorted(actual_states)}")

    # ---- CHECK 4: Null analysis ----
    print(f"\n{'=' * 70}")
    print("CHECK 4: Null/missing value analysis")
    print("=" * 70)
    null_counts = df.isnull().sum()
    for col in df.columns:
        n = null_counts[col]
        pct = n / total * 100
        status = "OK" if pct < 5 else "WARN" if pct < 50 else "HIGH"
        print(f"  {status:>4}  {col:<25} {n:>8,} nulls ({pct:.1f}%)")

    # ---- CHECK 5: Source breakdown ----
    print(f"\n{'=' * 70}")
    print("CHECK 5: Source file breakdown")
    print("=" * 70)
    source_counts = df["SOURCE"].value_counts()
    for src, cnt in source_counts.items():
        print(f"  {src:<25} {cnt:>8,} records ({cnt/total*100:.1f}%)")

    # ---- CHECK 6: Comparison to previous run (112,142) ----
    print(f"\n{'=' * 70}")
    print("CHECK 6: Comparison to previous Claude Code / Codex runs (112,142)")
    print("=" * 70)
    current_counts = df["STATE"].value_counts().to_dict()
    prev_total = sum(PREVIOUS_COUNTS.values())
    print(f"  {'State':<8} {'Previous':>10} {'Current':>10} {'Delta':>8}  Status")
    print(f"  {'-'*8} {'-'*10} {'-'*10} {'-'*8}  {'-'*10}")
    total_delta = 0
    for state in sorted(MANDATE_DATES.keys()):
        prev = PREVIOUS_COUNTS.get(state, 0)
        curr = current_counts.get(state, 0)
        delta = curr - prev
        total_delta += abs(delta)
        status = "MATCH" if delta == 0 else f"+{delta}" if delta > 0 else str(delta)
        print(f"  {state:<8} {prev:>10,} {curr:>10,} {delta:>+8,}  {status}")
    print(f"  {'TOTAL':<8} {prev_total:>10,} {total:>10,} {total-prev_total:>+8,}")
    if total_delta == 0:
        print(f"\n  Result: PERFECT MATCH")
    else:
        variance_pct = abs(total - prev_total) / prev_total * 100
        print(f"\n  Result: {variance_pct:.2f}% variance ({total - prev_total:+,} records)")

    # ---- CHECK 7: Employee count reasonableness ----
    print(f"\n{'=' * 70}")
    print("CHECK 7: Employee count distribution (reasonableness)")
    print("=" * 70)
    emp = df["EMPLOYEE_COUNT"].dropna()
    print(f"  Records with employee data: {len(emp):,} / {total:,} ({len(emp)/total*100:.1f}%)")
    print(f"  Min:    {emp.min():.0f}")
    print(f"  25th:   {emp.quantile(0.25):.0f}")
    print(f"  Median: {emp.median():.0f}")
    print(f"  75th:   {emp.quantile(0.75):.0f}")
    print(f"  Max:    {emp.max():.0f}")
    print(f"  Mean:   {emp.mean():.1f}")
    zeros = (emp == 0).sum()
    huge = (emp > 10000).sum()
    print(f"  Zero employees: {zeros:,}")
    print(f"  >10,000 employees: {huge:,}")

    # ---- CHECK 8: Date distribution ----
    print(f"\n{'=' * 70}")
    print("CHECK 8: Plan effective date distribution by year")
    print("=" * 70)
    df["YEAR"] = df["PLAN_EFFECTIVE_DATE"].dt.year
    year_counts = df["YEAR"].value_counts().sort_index()
    for yr, cnt in year_counts.items():
        bar = "#" * (cnt // 500)
        print(f"  {int(yr)}: {cnt:>8,}  {bar}")

    # ---- SUMMARY ----
    print(f"\n{'=' * 70}")
    print("AUDIT SUMMARY")
    print("=" * 70)
    checks = [
        ("Mandate date filtering", all_pass),
        ("EIN deduplication", dup_count == 0),
        ("Valid states only", len(unexpected) == 0),
        ("Previous run comparison", abs(total - prev_total) < prev_total * 0.01),
    ]
    for name, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")

    print(f"\n  Total records: {total:,}")
    print(f"  Audit completed.")


if __name__ == "__main__":
    main()
