"""Fetch BLS QCEW state-level annual private-sector aggregates.

QCEW (Quarterly Census of Employment and Wages) is the BLS administrative count
of UI-covered employment and establishments. Coverage is approximately 95% of
US jobs and is the closest BLS analog to Census CBP for private-sector
establishment counts.

Data source: BLS QCEW Open Data Access API
    https://data.bls.gov/cew/data/api/{year}/a/area/{area_code}.csv
where:
    {year}      = calendar year (annual averages, suffix 'a')
    {area_code} = 5-char state FIPS + '000' (e.g. '01000' = Alabama statewide)

Filtering convention to get one row per state-year of total private:
    own_code      = 5    (private ownership)
    industry_code = '10' (NAICS supersector "Total private")
    agglvl_code   = 51   (state, private ownership, total)

The annual average columns we extract:
    annual_avg_estabs  -> private_establishments
    annual_avg_emplvl  -> private_employment

QCEW annual data is published with a ~6-month lag, so 2024 should be the most
recent full-year data available as of mid-2026; 2025 will not yet be released.

Outputs:
    data/bls_qcew/raw/qcew_{state}_{year}.csv  (raw single-state-year CSVs)
    data/bls_qcew/state_year_private_establishments.csv  (standardized panel)
    methodology/bls_qcew_provenance_addendum.csv         (per-file provenance)
"""

from __future__ import annotations

import io
import os
import sys
import time
from datetime import datetime

import pandas as pd
import requests

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(REPO_ROOT, "data", "bls_qcew", "raw")
PANEL_OUT = os.path.join(REPO_ROOT, "data", "bls_qcew",
                          "state_year_private_establishments.csv")
PROVENANCE_OUT = os.path.join(REPO_ROOT, "methodology",
                               "bls_qcew_provenance_addendum.csv")

# 2017 through latest available full-year. QCEW publishes annual averages with
# ~6 month lag; as of 2026-05, 2024 annual is the latest available.
YEARS = list(range(2017, 2025))

# Same FIPS-to-state map used by fetch_cbp.py (50 states + DC).
FIPS_TO_STATE = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO",
    "09": "CT", "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI",
    "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
    "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
    "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
    "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
    "54": "WV", "55": "WI", "56": "WY",
}

URL_PATTERN = "https://data.bls.gov/cew/data/api/{year}/a/area/{area_code}.csv"


def fetch_state_year(state: str, fips: str, year: int):
    """Fetch one state-year QCEW CSV. Returns (raw_path, url, http_status,
    n_rows_total, n_rows_filtered, est, emp).
    """
    area_code = f"{fips}000"
    url = URL_PATTERN.format(year=year, area_code=area_code)
    raw_path = os.path.join(RAW_DIR, f"qcew_{state}_{year}.csv")

    # Skip download if cached.
    if os.path.exists(raw_path):
        text = open(raw_path, "r", encoding="utf-8").read()
        status = 200
    else:
        try:
            r = requests.get(url, timeout=60)
            status = r.status_code
            if status != 200:
                print(f"  [WARN] {state} {year}: HTTP {status}")
                return raw_path, url, status, 0, 0, None, None
            text = r.text
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"  [ERR] {state} {year}: {e}")
            return raw_path, url, -1, 0, 0, None, None

    df = pd.read_csv(io.StringIO(text),
                      dtype={"area_fips": str, "industry_code": str})
    n_total = len(df)

    # Total private state aggregate: own_code=5, industry_code='10', agglvl_code=51
    sel = df[(df["own_code"] == 5)
             & (df["industry_code"] == "10")
             & (df["agglvl_code"] == 51)]
    n_filt = len(sel)
    if n_filt != 1:
        print(f"  [WARN] {state} {year}: expected 1 total-private row, got {n_filt}")
        return raw_path, url, status, n_total, n_filt, None, None

    row = sel.iloc[0]
    est = float(row["annual_avg_estabs"])
    emp = float(row["annual_avg_emplvl"])
    return raw_path, url, status, n_total, n_filt, est, emp


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(PROVENANCE_OUT), exist_ok=True)

    panel_rows = []
    prov_rows = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    for fips, state in sorted(FIPS_TO_STATE.items(), key=lambda kv: kv[1]):
        for year in YEARS:
            raw_path, url, status, n_total, n_filt, est, emp = fetch_state_year(
                state, fips, year
            )
            print(f"  {state} {year}: status={status}, total_rows={n_total}, "
                  f"private_total_rows={n_filt}, estabs={est}, emp={emp}")
            if est is not None and emp is not None:
                panel_rows.append({
                    "state": state,
                    "year": year,
                    "private_establishments": est,
                    "private_employment": emp,
                    "source_url": url,
                })
            prov_rows.append({
                "downloaded_date": today,
                "state": state,
                "year": year,
                "url": url,
                "raw_path": os.path.relpath(raw_path, REPO_ROOT).replace("\\", "/"),
                "http_status": status,
                "n_rows_total": n_total,
                "n_rows_total_private_state_agg": n_filt,
                "annual_avg_estabs": est if est is not None else "",
                "annual_avg_emplvl": emp if emp is not None else "",
            })
            # Be polite to BLS servers.
            time.sleep(0.05)

    panel = pd.DataFrame(panel_rows).sort_values(["state", "year"]).reset_index(drop=True)
    prov = pd.DataFrame(prov_rows)

    panel.to_csv(PANEL_OUT, index=False)
    prov.to_csv(PROVENANCE_OUT, index=False)

    print(f"\nWrote {PANEL_OUT}: {len(panel):,} state-year rows")
    print(f"Wrote {PROVENANCE_OUT}: {len(prov):,} provenance rows")
    print(f"\nYears: {sorted(panel['year'].unique())}")
    print(f"States: {len(panel['state'].unique())} unique")
    print(f"\nSample (first 8 rows):")
    print(panel.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
