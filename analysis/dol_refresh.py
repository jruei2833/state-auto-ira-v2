"""DOL Form 5500 refresh helper — Apr 2026.

Steps:
  1. Verify the four refresh zips exist in form5500-raw-data/refresh_2026_04/.
  2. Back up the prior 2024 CSVs in form5500-raw-data/.
  3. Extract refreshed 2024 + 2025 CSVs into the existing folder structure
     (form5500/, form5500sf/). The CSV name inside each zip matches the
     historical convention (lowercase, e.g., f_5500_2024_all.csv).
  4. Compute per-file row counts (raw, post-2J, post-single-employer,
     post-state-filter, post-date-filter for v1 and v2).
  5. Write the row counts to methodology/source_provenance_log.csv,
     replacing the TBD placeholders with actual values.

This script does NOT re-run the full dataset build; that is delegated to
the patched build_both.py (extended to YEARS = range(2017, 2026)).
"""

from __future__ import annotations

import csv
import datetime as dt
import os
import re
import shutil
import sys
import zipfile

import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO, "form5500-raw-data")
REFRESH_DIR = os.path.join(RAW_DIR, "refresh_2026_04")
BACKUP_DIR = os.path.join(RAW_DIR, "pre_refresh_backup_2026_04")
PROVENANCE_PATH = os.path.join(REPO, "methodology", "source_provenance_log.csv")

# Mandate dates copied from build_both.py — needed to compute the
# "post-mandate" row count for the provenance log.
MANDATE_V1 = {
    "OR": "2017-11-01", "IL": "2018-05-01", "CA": "2018-11-01",
    "CT": "2022-04-01", "MD": "2022-09-01", "CO": "2023-01-01",
    "VA": "2023-07-01", "ME": "2024-01-01", "DE": "2024-01-01",
    "NJ": "2024-03-01",
}
MANDATE_V2 = {
    "OR": "2017-11-01", "IL": "2018-11-01", "CA": "2019-07-01",
    "CT": "2022-04-01", "MD": "2022-09-01", "CO": "2023-01-01",
    "VA": "2023-07-01", "ME": "2024-01-01", "DE": "2024-07-01",
    "NJ": "2024-06-30",
}

ZIP_FILES = {
    # zip-name → (subdir under raw, expected CSV stem)
    "F_5500_2024_All.zip": ("form5500", "f_5500_2024_all"),
    "F_5500_SF_2024_All.zip": ("form5500sf", "f_5500_sf_2024_all"),
    "F_5500_2025_All.zip": ("form5500", "f_5500_2025_all"),
    "F_5500_SF_2025_All.zip": ("form5500sf", "f_5500_sf_2025_all"),
}

URL_BASE = "https://askebsa.dol.gov/FOIA%20Files"
URL_TEMPLATE = {
    "F_5500_2024_All.zip": f"{URL_BASE}/2024/All/F_5500_2024_All.zip",
    "F_5500_SF_2024_All.zip": f"{URL_BASE}/2024/All/F_5500_SF_2024_All.zip",
    "F_5500_2025_All.zip": f"{URL_BASE}/2025/All/F_5500_2025_All.zip",
    "F_5500_SF_2025_All.zip": f"{URL_BASE}/2025/All/F_5500_SF_2025_All.zip",
}

F5500_COLS = {
    "pension": "TYPE_PENSION_BNFT_CODE",
    "entity": "TYPE_PLAN_ENTITY_CD",
    "entity_value": ["2", "2.0"],
    "date": "PLAN_EFF_DATE",
    "state": "SPONS_DFE_MAIL_US_STATE",
    "ein": "SPONS_DFE_EIN",
}
F5500SF_COLS = {
    "pension": "SF_TYPE_PENSION_BNFT_CODE",
    "entity": "SF_PLAN_ENTITY_CD",
    "entity_value": ["1", "1.0"],
    "date": "SF_PLAN_EFF_DATE",
    "state": "SF_SPONS_US_STATE",
    "ein": "SF_SPONS_EIN",
}


def get_col(df, name):
    if name in df.columns:
        return name
    upper = name.upper()
    for c in df.columns:
        if c.upper() == upper:
            return c
    return None


def count_after_filters(csv_path: str, col_map: dict) -> dict:
    """Return per-stage row counts for one CSV file.

    Stages:
        raw            : total rows in CSV
        after_2J       : after pension code 2J filter
        after_single   : after single-employer entity filter
        after_state    : after state-in-mandate-list filter
        after_v1_date  : after plan-effective-date > v1 mandate date
        after_v2_date  : after plan-effective-date > v2 mandate date
    """
    print(f"  reading {os.path.basename(csv_path)}...", flush=True)
    use_cols = [col_map[k] for k in ("pension", "entity", "date", "state", "ein")]
    head = pd.read_csv(csv_path, nrows=0, encoding="latin1")
    actual = {k: get_col(head, col_map[k]) for k in
              ("pension", "entity", "date", "state", "ein")}
    if not all(actual.values()):
        print(f"  [WARN] missing cols in {csv_path}: {actual}")
        return {"raw": 0, "after_2J": 0, "after_single": 0,
                "after_state": 0, "after_v1_date": 0, "after_v2_date": 0}

    df = pd.read_csv(csv_path, usecols=list(actual.values()),
                     encoding="latin1", low_memory=False)
    raw = len(df)

    df[actual["pension"]] = df[actual["pension"]].astype(str)
    df = df[df[actual["pension"]].str.contains("2J", na=False)]
    after_2J = len(df)

    df[actual["entity"]] = df[actual["entity"]].astype(str).str.strip()
    df = df[df[actual["entity"]].isin(col_map["entity_value"])]
    after_single = len(df)

    df[actual["state"]] = df[actual["state"]].astype(str).str.strip().str.upper()
    df = df[df[actual["state"]].isin(set(MANDATE_V1.keys()))]
    after_state = len(df)

    df[actual["date"]] = pd.to_datetime(df[actual["date"]], errors="coerce")
    df = df.dropna(subset=[actual["date"]])

    after_v1 = sum(
        ((df[actual["state"]] == s)
         & (df[actual["date"]] > pd.Timestamp(d))).sum()
        for s, d in MANDATE_V1.items()
    )
    after_v2 = sum(
        ((df[actual["state"]] == s)
         & (df[actual["date"]] > pd.Timestamp(d))).sum()
        for s, d in MANDATE_V2.items()
    )

    return {"raw": raw, "after_2J": after_2J, "after_single": after_single,
            "after_state": after_state,
            "after_v1_date": int(after_v1), "after_v2_date": int(after_v2)}


def extract_zip(zip_path: str, dest_dir: str) -> str:
    """Extract a zip into dest_dir; return the path to the extracted CSV."""
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise RuntimeError(f"no CSV in {zip_path}")
        name = names[0]  # always single CSV per DOL zip
        # extract with lower-case filename to match existing convention
        target = os.path.join(dest_dir, name.lower())
        with z.open(name) as src, open(target, "wb") as dst:
            shutil.copyfileobj(src, dst)
    return target


def main():
    pull_date = dt.date.today().isoformat()
    print(f"DOL Form 5500 refresh, pull date {pull_date}")

    # 1. verify zips
    missing = [z for z in ZIP_FILES if not os.path.exists(
        os.path.join(REFRESH_DIR, z))]
    if missing:
        print(f"[ERROR] missing zip files: {missing}")
        sys.exit(1)

    # 2. backup pre-refresh 2024 files
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for src in [
        os.path.join(RAW_DIR, "form5500", "f_5500_2024_all.csv"),
        os.path.join(RAW_DIR, "form5500sf", "f_5500_sf_2024_all.csv"),
    ]:
        if os.path.exists(src):
            backup_target = os.path.join(BACKUP_DIR, os.path.basename(src))
            if not os.path.exists(backup_target):
                shutil.copy2(src, backup_target)
                print(f"  backed up {src} -> {backup_target}")
            else:
                print(f"  backup exists: {backup_target}")

    # 3. extract refresh zips into the existing data dirs
    refresh_csvs = {}
    for zip_name, (subdir, _stem) in ZIP_FILES.items():
        zip_path = os.path.join(REFRESH_DIR, zip_name)
        dest_dir = os.path.join(RAW_DIR, subdir)
        os.makedirs(dest_dir, exist_ok=True)
        csv_path = extract_zip(zip_path, dest_dir)
        refresh_csvs[zip_name] = csv_path
        print(f"  extracted {zip_name} -> {csv_path}")

    # 4. count rows post-filter for each refreshed CSV
    print("\nCounting filter stages for each refreshed file...")
    counts: dict[str, dict] = {}
    for zip_name, csv_path in refresh_csvs.items():
        col_map = (F5500_COLS if "F_5500_" in zip_name and "SF" not in zip_name
                   else F5500SF_COLS)
        counts[zip_name] = count_after_filters(csv_path, col_map)
        print(f"  {zip_name}: {counts[zip_name]}")

    # 5. update source_provenance_log.csv with row counts for 2024 / 2025
    update_provenance_log(pull_date, counts)


def update_provenance_log(pull_date: str, counts: dict):
    """Replace TBD placeholders for the 2024 and 2025 rows."""
    with open(PROVENANCE_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    # Build lookup: (source_name, filing_year) → counts dict
    zip_to_key = {
        "F_5500_2024_All.zip": ("Form 5500", "2024"),
        "F_5500_SF_2024_All.zip": ("Form 5500-SF", "2024"),
        "F_5500_2025_All.zip": ("Form 5500", "2025"),
        "F_5500_SF_2025_All.zip": ("Form 5500-SF", "2025"),
    }

    # Add 2025 rows if missing
    existing_keys = {(r["source_name"], r["filing_year"]) for r in rows}
    for zip_name, (sn, fy) in zip_to_key.items():
        if (sn, fy) not in existing_keys:
            new_row = {col: "" for col in fieldnames}
            new_row.update({
                "source_name": sn,
                "filing_year": fy,
                "pull_date": "TBD",
                "file_name": f"f_{'5500_sf' if 'SF' in zip_name else '5500'}_{fy}_latest.zip",
                "source_url": "https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets",
                "raw_rows": "TBD", "after_pension_code_2J_filter": "TBD",
                "after_single_employer_filter": "TBD",
                "after_state_filter": "TBD",
                "after_date_filter_v1_inclusive": "TBD",
                "after_date_filter_v2_conservative": "TBD",
                "notes": "First addition: 2025 partial-year filings (mandate-state plans only)",
            })
            rows.append(new_row)

    # Update rows with counts
    for r in rows:
        sn = r.get("source_name", "")
        fy = r.get("filing_year", "")
        for zip_name, (target_sn, target_fy) in zip_to_key.items():
            if sn == target_sn and fy == target_fy:
                c = counts[zip_name]
                r["pull_date"] = pull_date
                r["raw_rows"] = c["raw"]
                r["after_pension_code_2J_filter"] = c["after_2J"]
                r["after_single_employer_filter"] = c["after_single"]
                r["after_state_filter"] = c["after_state"]
                r["after_date_filter_v1_inclusive"] = c["after_v1_date"]
                r["after_date_filter_v2_conservative"] = c["after_v2_date"]
                # preserve original note for 2024 rows
                if not r.get("notes"):
                    r["notes"] = "Refreshed Apr 2026"
                else:
                    r["notes"] = r["notes"] + f" | refreshed {pull_date}"
                break

    # Sort: keep totals at the end
    sorted_rows = (
        sorted([r for r in rows if not r["source_name"].startswith("TOTAL")],
               key=lambda r: (r["source_name"], r["filing_year"]))
        + [r for r in rows if r["source_name"].startswith("TOTAL")]
    )

    with open(PROVENANCE_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(sorted_rows)
    print(f"\nUpdated {PROVENANCE_PATH}")


if __name__ == "__main__":
    main()
