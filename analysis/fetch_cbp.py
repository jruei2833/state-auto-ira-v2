"""Fetch Census County Business Patterns (CBP) private establishments by state-year.

CBP covers private-sector establishments only (federal/state/local government
employees are excluded by program definition), so the raw count is exactly
the denominator we want for the DiD: the population of firms eligible to
establish a 401(k) plan.

Census API URL forms (no key needed for state-level queries):

    https://api.census.gov/data/{year}/cbp
        ?get=ESTAB&for=state:*&NAICS{17|22}=00

NAICS scheme changed in 2022 — query parameter switches.
"""

import json
import os
import sys
import time

import pandas as pd
import requests

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "cbp_state_year.csv")

# CBP releases lag by ~2 years. As of writing, the latest available year is
# typically t-2 or t-3. We try every year in the window and write whatever
# comes back; missing years are imputed by carry-forward.
YEARS = list(range(2017, 2025))

FIPS_TO_STATE = {
    "01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT",
    "10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL",
    "18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD",
    "25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE",
    "32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND",
    "39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD",
    "47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV",
    "55":"WI","56":"WY",
}


def fetch_year(year):
    # CBP API uses NAICS2017 as the predicate variable name across 2017-2023
    # (Census kept the variable name even after the underlying classification
    # switched to NAICS 2022). 2024 is not yet released.
    url = ("https://api.census.gov/data/"
           f"{year}/cbp?get=ESTAB,EMP&for=state:*&NAICS2017=00")
    print(f"  GET {url}")
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        print(f"  [ERR] {year}: HTTP {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    header, *rows = data
    df = pd.DataFrame(rows, columns=header)
    df["year"] = year
    df["state"] = df["state"].map(FIPS_TO_STATE)
    df = df.dropna(subset=["state"])
    df["establishments"] = pd.to_numeric(df["ESTAB"], errors="coerce")
    df["employment"] = pd.to_numeric(df["EMP"], errors="coerce")
    return df[["state", "year", "establishments", "employment"]]


def main():
    frames = []
    for y in YEARS:
        f = fetch_year(y)
        if f is not None:
            frames.append(f)
        time.sleep(0.5)  # be polite

    if not frames:
        print("[ERROR] No CBP data fetched")
        sys.exit(1)

    cbp = pd.concat(frames, ignore_index=True)

    # Carry-forward fill for missing years (CBP release lag).
    available_years = sorted(cbp["year"].unique())
    print(f"\nCBP years actually returned: {available_years}")
    full_grid = pd.MultiIndex.from_product(
        [sorted(FIPS_TO_STATE.values()), YEARS], names=["state", "year"]
    ).to_frame(index=False)
    out = full_grid.merge(cbp, on=["state", "year"], how="left")

    # Forward-fill within state, then back-fill at the start
    out = out.sort_values(["state", "year"])
    out[["establishments", "employment"]] = (
        out.groupby("state")[["establishments", "employment"]]
           .ffill().bfill()
    )

    out.to_csv(OUT_PATH, index=False)
    print(f"\nWrote {OUT_PATH}: {len(out):,} state-year rows")
    print(f"Sample:\n{out.head(10)}")


if __name__ == "__main__":
    main()
