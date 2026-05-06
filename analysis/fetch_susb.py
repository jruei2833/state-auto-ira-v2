"""Fetch Census SUSB (Statistics of US Businesses) state-by-employment-size files.

SUSB publishes annual state-level tables. The relevant series is
"U.S. & states, NAICS, detailed employment sizes". Files are at
    https://www2.census.gov/programs-surveys/susb/tables/{YEAR}/us_state_naics_detailedsizes_{YEAR}.xlsx

The detailedsizes file uses very granular bins (5,000+, 2,500-4,999, 750-999,
etc.) — we aggregate up to the project's standard bins for the DiD denominator:

    "all"      = SUSB '01: Total'
    "0-4"      = SUSB '02: <5 employees'
    "5-9"      = SUSB '03: 5-9 employees'
    "10-19"    = '04:10-14' + '05: 15-19'
    "20-99"    = '07: 20-24' + '08: 25-29' + '09: 30-34' + '10: 35-39'
                 + '11: 40-49' + '12: 50-74' + '13: 75-99'
    "100-499"  = '14: 100-149' + '15: 150-199' + '16: 200-299'
                 + '17: 300-399' + '18: 400-499'
    "500+"     = '20: 500-749' + '21: 750-999' + '22: 1,000-1,499'
                 + '23: 1,500-1,999' + '24: 2,000-2,499'
                 + '25: 2,500-4,999' + '26: 5,000+'
    SUSB '06: <20' and '19: <500' are SUBTOTALS — we drop them.

SUSB releases lag by ~2 years; 2022 is the most recent year available
as of May 2026.

The header row in the SUSB Excel file is row 3 (0-indexed: 2).

Filter: NAICS code = '--' (Total), NAICS Description = 'Total'.

Outputs:
    data/census_susb/raw/us_state_naics_detailedsizes_{year}.xlsx (raw)
    data/census_susb/state_year_firms_by_size.csv (standardized panel)
    methodology/census_susb_provenance_addendum.csv (per-file provenance)
"""

import os
import sys
import time
from datetime import date

import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "census_susb", "raw")
OUT_PANEL = os.path.join(BASE_DIR, "data", "census_susb",
                          "state_year_firms_by_size.csv")
PROVENANCE_OUT = os.path.join(BASE_DIR, "methodology",
                                "census_susb_provenance_addendum.csv")

# 2023+ not yet released as of May 2026 (Census SUSB has ~2-year lag and
# 2022 file was released April 2025; 2023 expected late 2026).
YEARS = list(range(2017, 2023))

URL_TEMPLATE = ("https://www2.census.gov/programs-surveys/susb/tables/"
                "{year}/us_state_naics_detailedsizes_{year}.xlsx")

STATE_FIPS = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
    "Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC",
    "Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL",
    "Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA",
    "Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
    "Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT",
    "Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ",
    "New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND",
    "Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA",
    "Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD",
    "Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA",
    "Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY",
}

# Map SUSB granular size class strings to project standard bins.
# Note SUSB has historically alternated between '04:10-14' (no space after
# colon) and '04: 10-14' (with space) — we compare on the trimmed token after
# the colon-space.
def _norm_size_label(s: str) -> str:
    """Strip the 'NN: ' prefix and any 'employees' suffix to get the bin."""
    s = str(s).strip()
    # Drop 'NN:' prefix
    if ":" in s:
        s = s.split(":", 1)[1].strip()
    s = s.replace("employees", "").strip()
    s = s.replace(",", "")  # '1,000' -> '1000'
    return s


# Map normalized SUSB bin -> project bin
SIZE_BIN_MAP = {
    "Total": "all",
    "<5": "0-4",
    "5-9": "5-9",
    "10-14": "10-19",
    "15-19": "10-19",
    "20-24": "20-99",
    "25-29": "20-99",
    "30-34": "20-99",
    "35-39": "20-99",
    "40-49": "20-99",
    "50-74": "20-99",
    "75-99": "20-99",
    "100-149": "100-499",
    "150-199": "100-499",
    "200-299": "100-499",
    "300-399": "100-499",
    "400-499": "100-499",
    "500-749": "500+",
    "750-999": "500+",
    "1000-1499": "500+",
    "1500-1999": "500+",
    "2000-2499": "500+",
    "2500-4999": "500+",
    "5000+": "500+",
}

# Subtotals to drop (already covered by their constituents)
SUBTOTAL_LABELS = {"<20", "<500"}


def download_one(year: int) -> tuple[str, str] | None:
    """Download SUSB state-by-size file for a year. Returns (path, url)."""
    url = URL_TEMPLATE.format(year=year)
    out_path = os.path.join(RAW_DIR, f"us_state_naics_detailedsizes_{year}.xlsx")
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        if size > 100_000:
            print(f"  cached: {out_path} ({size:,} bytes)")
            return out_path, url
    print(f"  GET {url}")
    r = requests.get(url, timeout=300)
    if r.status_code != 200:
        print(f"  [ERR] {year}: HTTP {r.status_code}")
        return None
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"  wrote {out_path} ({len(r.content):,} bytes)")
    return out_path, url


def parse_one(path: str, year: int) -> pd.DataFrame:
    """Parse a SUSB state-by-size file into long format.

    Returns columns: state | year | size_class | firm_count | establishment_count
    """
    df = pd.read_excel(path, sheet_name=0, header=2, engine="openpyxl")

    # Sometimes column names have leading/trailing whitespace
    df.columns = [str(c).strip() for c in df.columns]

    # Column-name variation across years: handle both 'NAICS' and 'NAICS Code'
    state_col = next((c for c in df.columns
                       if c.lower() in ("state name", "statedscr", "state_dscr")), None)
    if state_col is None:
        # fall back: 'State Name' column index
        state_col = "State Name" if "State Name" in df.columns else df.columns[1]

    naics_desc_col = next((c for c in df.columns
                            if c.lower() in ("naics description",
                                             "naicsdscr",
                                             "naics_dscr")), None)
    if naics_desc_col is None:
        naics_desc_col = "NAICS Description" if "NAICS Description" in df.columns else df.columns[3]

    size_col = next((c for c in df.columns
                      if c.lower() in ("enterprise size",
                                       "entrsizedscr", "entrsizedsc")), None)
    if size_col is None:
        size_col = "Enterprise Size" if "Enterprise Size" in df.columns else df.columns[4]

    firms_col = next((c for c in df.columns
                       if c.lower() in ("firms", "firm", "number of firms")), None)
    if firms_col is None:
        firms_col = "Firms" if "Firms" in df.columns else df.columns[5]

    estabs_col = next((c for c in df.columns
                        if c.lower() in ("establishments", "estb", "number of establishments")),
                       None)
    if estabs_col is None:
        estabs_col = "Establishments" if "Establishments" in df.columns else df.columns[6]

    # Filter to NAICS Total
    df = df[df[naics_desc_col].astype(str).str.strip().str.lower() == "total"].copy()

    # State filter
    df["state_full"] = df[state_col].astype(str).str.strip()
    df["state"] = df["state_full"].map(STATE_FIPS)
    df = df.dropna(subset=["state"]).copy()

    # Size class normalization
    df["bin"] = df[size_col].apply(_norm_size_label)

    # Drop subtotals
    df = df[~df["bin"].isin(SUBTOTAL_LABELS)].copy()
    df["size_class"] = df["bin"].map(SIZE_BIN_MAP)

    unmatched = df[df["size_class"].isna()]["bin"].unique()
    if len(unmatched) > 0:
        print(f"  WARNING: unmatched bins in {year}: {list(unmatched)[:10]}")
    df = df.dropna(subset=["size_class"]).copy()

    df["firm_count"] = pd.to_numeric(df[firms_col], errors="coerce")
    df["establishment_count"] = pd.to_numeric(df[estabs_col], errors="coerce")
    df["year"] = year

    # Aggregate granular bins up to project bins
    out = (df.groupby(["state", "year", "size_class"], as_index=False)
              .agg({"firm_count": "sum", "establishment_count": "sum"}))

    # Sanity check: each (state, year) must have all 7 size classes
    expected = {"all", "0-4", "5-9", "10-19", "20-99", "100-499", "500+"}
    by_state = out.groupby("state")["size_class"].apply(set)
    missing = by_state[by_state.apply(lambda s: s != expected)]
    if len(missing) > 0:
        print(f"  WARNING: states missing size classes in {year}:")
        for st, classes in missing.items():
            print(f"    {st}: missing {expected - classes}")

    return out


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUT_PANEL), exist_ok=True)
    os.makedirs(os.path.dirname(PROVENANCE_OUT), exist_ok=True)

    panel_frames: list[pd.DataFrame] = []
    provenance: list[dict] = []

    for year in YEARS:
        print(f"\n=== {year} ===")
        result = download_one(year)
        if result is None:
            print(f"  SKIP {year}: download failed")
            provenance.append({
                "source": "Census SUSB",
                "table": "us_state_naics_detailedsizes",
                "year": year,
                "url": URL_TEMPLATE.format(year=year),
                "downloaded_on": date.today().isoformat(),
                "rows_parsed": 0,
                "status": "FAILED_DOWNLOAD",
                "notes": "URL returned non-200 (year not released or moved)",
            })
            continue
        path, url = result
        try:
            df = parse_one(path, year)
        except Exception as e:
            print(f"  ERROR parsing {year}: {e}")
            provenance.append({
                "source": "Census SUSB",
                "table": "us_state_naics_detailedsizes",
                "year": year,
                "url": url,
                "downloaded_on": date.today().isoformat(),
                "rows_parsed": 0,
                "status": "FAILED_PARSE",
                "notes": str(e)[:200],
            })
            continue
        print(f"  parsed {len(df):,} rows for {year}")
        df["source_url"] = url
        panel_frames.append(df)
        provenance.append({
            "source": "Census SUSB",
            "table": "us_state_naics_detailedsizes",
            "year": year,
            "url": url,
            "downloaded_on": date.today().isoformat(),
            "rows_parsed": int(len(df)),
            "status": "OK",
            "notes": "",
        })
        time.sleep(0.5)

    if not panel_frames:
        print("[ERROR] No SUSB data parsed")
        sys.exit(1)

    panel = pd.concat(panel_frames, ignore_index=True)
    panel = panel[["state", "year", "size_class", "firm_count",
                    "establishment_count", "source_url"]]
    panel = panel.sort_values(["state", "year", "size_class"]).reset_index(drop=True)
    panel.to_csv(OUT_PANEL, index=False)
    print(f"\nWrote {OUT_PANEL}: {len(panel):,} rows")

    pd.DataFrame(provenance).to_csv(PROVENANCE_OUT, index=False)
    print(f"Wrote {PROVENANCE_OUT}")

    # Quick sanity printout: CA all years
    print("\nSample (CA all years, all sizes):")
    print(panel[panel["state"] == "CA"].to_string(index=False))


if __name__ == "__main__":
    main()
