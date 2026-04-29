"""SEC EDGAR pilot: identify public-company-looking firms in the
v2-conservative dataset, search EDGAR for their 10-K and DEF 14A filings,
and extract 401(k) match formula language.

Outputs `deliverables/match_formula_tracker.csv` with one row per searched
firm (including searched-but-not-found cases), per the schema defined at
the top of this file.

There is no formal workplan defining the schema or selection rules — both
are documented inline. If the workplan defines them differently, adjust
the SCHEMA list and SELECTION_FILTERS section.

Approach:
  1. Filter v2-conservative to firms with employee count ≥ 250 (proxy for
     plan-participant count; large firms are more likely public) and a
     "public-suggestive" name (INC / CORP / HOLDINGS / GROUP / etc.) and
     no obvious non-public tokens (PC, MD, DDS, DENTAL, LAW OFFICE, etc.).
  2. Take the top 50 by employee count.
  3. For each candidate: hit EDGAR full-text search with the cleaned
     company name, restricted to 10-K + DEF 14A. Pick the best match.
  4. If found: fetch the filing's primary text file, locate "401(k)"
     mentions, and extract a 1-3 sentence excerpt around match-formula
     language using a curated set of regex heuristics.
  5. Write tracker CSV including searched-but-not-found and ambiguous-match
     cases.

EDGAR best practices observed:
  - User-Agent: identifies the requester per SEC.gov/oit/announcement/
    new-rate-control-limits — using the user's email address.
  - Rate limit: ≤10 req/sec — script adds 0.15s sleep between calls so
    typical run is ~1 req/sec.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse

import pandas as pd
import requests

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO, "data", "v2-conservative",
                         "state_auto_ira_401k_dataset.csv")
DELIVERABLE = os.path.join(REPO, "deliverables", "match_formula_tracker.csv")
LOG_PATH = os.path.join(REPO, "analysis", "edgar_search.log")

USER_AGENT = ("State Auto-IRA Research jruei@americafirstpolicy.com "
              "(SEC EDGAR pilot - read-only)")
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json"}

EDGAR_FULL_TEXT = "https://efts.sec.gov/LATEST/search-index"
EDGAR_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"

TARGET_FORMS = ["10-K", "DEF 14A", "20-F", "10-K/A"]
N_CANDIDATES = 50
MIN_EMPLOYEES = 250

NON_PUBLIC_TOKENS = re.compile(
    r"\b(MD|DDS|DMD|PC|P\.C\.|DENTAL|DENTISTRY|ORTHODONTIC|DERMATOLOGY|"
    r"PEDIATRIC|CARDIOLOGY|VETERINARY|FAMILY PRACTICE|LAW OFFICE|ATTORNEY|"
    r"REALTY|CHURCH|MINISTRY|ASSEMBLY OF GOD|CATHOLIC|BAPTIST|"
    r"FAMILY TRUST|CPA|ACCOUNTANT|INSURANCE AGENCY)\b",
    re.IGNORECASE,
)
PUBLIC_HINTS = re.compile(
    r"\b(INC|INCORPORATED|CORP|CORPORATION|HOLDINGS|HOLDING|GROUP|"
    r"TECHNOLOGIES|TECHNOLOGY|INDUSTRIES|ENTERPRISES|COMPANY|COMPANIES|"
    r"INTERNATIONAL|GLOBAL|SOLUTIONS|SYSTEMS|RESOURCES|BANCORP|BANK|"
    r"FINANCIAL|CAPITAL|PRODUCTS|FOODS|MEDIA|NETWORKS|NETWORK)\b",
    re.IGNORECASE,
)

# 401(k) match-formula extraction patterns, ordered by specificity
MATCH_PATTERNS = [
    # "100% of the first 3% and 50% of the next 2%"
    re.compile(
        r"(\d{1,3})\s*%\s+of\s+(?:the\s+first\s+)?(\d{1,3}(?:\.\d+)?)\s*%"
        r"(?:\s+(?:and|plus)\s+(\d{1,3})\s*%\s+of\s+(?:the\s+next\s+)?"
        r"(\d{1,3}(?:\.\d+)?)\s*%)?",
        re.IGNORECASE,
    ),
    # "matches dollar-for-dollar up to 4%"
    re.compile(
        r"dollar[\s-]*for[\s-]*dollar\s+(?:up\s+to\s+)?(\d{1,3}(?:\.\d+)?)\s*%",
        re.IGNORECASE,
    ),
    # "matching contribution of 50% on the first 6%"
    re.compile(
        r"matching\s+contributions?\s+(?:of|equal\s+to)\s+"
        r"(\d{1,3})\s*%\s+(?:of|on)\s+(?:the\s+first\s+)?(\d{1,3}(?:\.\d+)?)\s*%",
        re.IGNORECASE,
    ),
]
SAFE_HARBOR_RX = re.compile(r"safe[\s-]*harbor", re.IGNORECASE)
PROFIT_SHARING_RX = re.compile(r"profit[\s-]*sharing", re.IGNORECASE)
DISCRETIONARY_RX = re.compile(r"discretionary\s+(?:matching\s+)?contribution",
                              re.IGNORECASE)


# --------------------- candidate selection ---------------------

def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    n = name.strip().upper()
    n = re.sub(r"[,\.]", " ", n)
    n = re.sub(r"\s+(LLC|L L C|LP|L P|INC|INCORPORATED|CORP|CORPORATION|"
               r"GROUP|HOLDINGS|HOLDING|CO|COMPANY)\.?$", "", n).strip()
    n = re.sub(r"\s+", " ", n)
    return n


def select_candidates(df: pd.DataFrame, n: int) -> pd.DataFrame:
    df = df.copy()
    df["EMPLOYEE_COUNT"] = pd.to_numeric(df["EMPLOYEE_COUNT"], errors="coerce")
    df = df[df["EMPLOYEE_COUNT"] >= MIN_EMPLOYEES]
    df["firm_upper"] = df["FIRM_NAME"].fillna("").str.upper()
    df = df[df["firm_upper"].str.strip() != ""]
    df = df[df["firm_upper"].apply(lambda x: bool(PUBLIC_HINTS.search(x)))]
    df = df[~df["firm_upper"].apply(lambda x: bool(NON_PUBLIC_TOKENS.search(x)))]
    df = df.sort_values("EMPLOYEE_COUNT", ascending=False)
    df = df.head(n)
    df["normalized_name"] = df["FIRM_NAME"].apply(normalize_name)
    return df.reset_index(drop=True)


# --------------------- EDGAR search ---------------------

# Stop tokens — words common across thousands of company names that
# carry no identifying information. Two companies sharing only stop tokens
# are not the same company.
STOP_TOKENS = {
    "HOLDINGS", "HOLDING", "GROUP", "MANAGEMENT", "ENTERPRISES", "ENTERPRISE",
    "COMPANY", "COMPANIES", "CORPORATION", "INCORPORATED", "SOLUTIONS",
    "SYSTEMS", "INDUSTRIES", "INTERNATIONAL", "GLOBAL", "RESOURCES",
    "SERVICES", "TECHNOLOGIES", "TECHNOLOGY", "CAPITAL", "FINANCIAL",
    "PARTNERS", "PARTNERSHIP", "PRODUCTS", "BRANDS", "MEDIA", "NETWORKS",
    "NETWORK", "COMMUNICATIONS", "ENERGY", "HEALTH", "HEALTHCARE",
    "PHARMACEUTICALS", "BIOTECH", "TRUST", "EQUITY", "INVESTMENTS",
    "INVESTMENT", "LIMITED", "AMERICAN", "AMERICA", "NATIONAL", "FIRST",
    "GENERAL", "UNITED", "WORLDWIDE", "FOODS", "FOOD", "RESTAURANT",
    "EDUCATION", "MANUFACTURING", "MEDICAL", "PROPERTIES", "PROPERTY",
    "REALTY", "REAL", "ESTATE", "INSURANCE", "BANCORP", "BANK", "BANKING",
    "SENIOR", "LIVING", "CARE", "SPACE", "MINING", "RETAIL", "INDUSTRIAL",
    "AUTOMOTIVE", "COMMERCIAL", "RESIDENTIAL", "ENTERTAINMENT", "STAFFING",
    "LABOR", "SCHOOL", "SCHOOLS", "BEHAVIORAL", "PIZZA", "APPAREL", "FORCE",
    "WORKFORCE", "PACKING", "PRODUCT", "PRODUCTION", "GENERATION",
    "INTERMEDIATE", "PATRIOT", "PREMIER", "HOME", "HOMES", "COUNTY",
    "AUTOMATION", "ELECTRIC", "ELECTRONICS", "GAS", "OIL", "WATER", "AIR",
    "STEEL", "METAL", "WOOD", "PAPER", "CHEMICAL", "PLASTIC", "MATERIALS",
    "INC", "LLC", "CORP", "LP", "PLC", "ADR", "LTD", "CO", "AND", "FOR",
    "THE", "OUR", "NEW", "OLD", "THIS", "THAT", "USA", "USE", "DBA",
}

_TICKER_CACHE: dict | None = None


def distinctive_tokens(s: str) -> list[str]:
    """Tokens (length >= 4, alphanumeric) with stop tokens removed,
    preserving order of first appearance."""
    seen: set[str] = set()
    out: list[str] = []
    for tok in re.findall(r"\b[A-Z][A-Z0-9]{3,}\b", s.upper()):
        if tok in STOP_TOKENS or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out


def load_ticker_index() -> dict:
    """Download SEC's authoritative public-company list (CIK + name + ticker).

    The full-text search API often misses matches when the Form 5500 plan
    sponsor name differs slightly from the SEC entity name. Cross-referencing
    against this list gives a more reliable yes/no on "is this a public
    company" before we even hit EDGAR for filings.
    """
    global _TICKER_CACHE
    if _TICKER_CACHE is not None:
        return _TICKER_CACHE
    url = "https://www.sec.gov/files/company_tickers.json"
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    raw = r.json()
    by_token: dict[str, list[dict]] = {}
    entries = []
    for v in raw.values():
        cik = int(v["cik_str"])
        name = str(v["title"]).upper()
        ticker = str(v["ticker"]).upper()
        toks = distinctive_tokens(name)
        e = {"cik": cik, "name": name, "ticker": ticker, "tokens": toks}
        entries.append(e)
        for tok in toks:
            by_token.setdefault(tok, []).append(e)
    _TICKER_CACHE = {"entries": entries, "by_token": by_token}
    return _TICKER_CACHE


def fuzzy_name_match(query_upper: str, idx: dict) -> tuple[dict | None, float, str]:
    """Match a Form 5500 firm name to a SEC ticker-list entry.

    Decision rule (strict, conservative — false negatives are preferable
    to false positives because the user reviews the tracker manually):

      1. Tokenize both names; drop stop tokens (see STOP_TOKENS above).
      2. Require the FIRST DISTINCTIVE TOKEN of both names to be the same.
         (This rules out 'SKILLSET GROUP' matching 'BHP GROUP' or
         'TRUSTED HEALTH' matching 'NRC HEALTH'.)
      3. For "high"-confidence match: require >= 2 distinctive tokens to
         intersect. This filters out cases like 'SUMMIT STAFFING' matching
         'SUMMIT NETWORKS' where only the leading word matches.
      4. For "low"-confidence (1-token) matches: return them as ambiguous
         so the user can review.

    Returns (best entry or None, score, confidence label).
    """
    qtokens = distinctive_tokens(query_upper)
    if not qtokens:
        return None, 0.0, "no_distinctive_tokens"
    first_q = qtokens[0]

    candidates = idx["by_token"].get(first_q, [])
    if not candidates:
        return None, 0.0, "no_first_token_match"

    qset = set(qtokens)
    best, best_score, best_overlap, best_first_match = None, 0.0, 0, False
    for e in candidates:
        ntokens = e["tokens"]
        if not ntokens:
            continue
        first_c = ntokens[0]
        if first_c != first_q:
            continue  # require both leading distinctive tokens to match
        nset = set(ntokens)
        inter = qset & nset
        jaccard = len(inter) / len(qset | nset)
        if jaccard > best_score:
            best, best_score = e, jaccard
            best_overlap = len(inter)
            best_first_match = True

    if best is None:
        return None, 0.0, "no_strict_match"
    confidence = "high" if best_overlap >= 2 else "low"
    return best, best_score, confidence


def edgar_full_text_search(name: str, forms: list[str]) -> dict:
    """Hit EDGAR full-text search restricted to a CIK if known.

    The full-text search 500s frequently for free-form name queries; we
    therefore search by CIK (which never 500s) and let our fuzzy_name_match
    decide if the candidate is a public company first.
    """
    forms_q = ",".join(f.replace(" ", "+") for f in forms)
    q = f'"{name}"'
    params = {"q": q, "forms": forms_q}
    url = f"{EDGAR_FULL_TEXT}?{urllib.parse.urlencode(params)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 500:
            return {"status": "error", "n_hits": 0, "query": q, "hits": [],
                    "error_msg": "EDGAR full-text 500 (often query-pattern related)"}
        if r.status_code != 200:
            return {"status": "error", "n_hits": 0, "query": q, "hits": [],
                    "error_msg": f"HTTP {r.status_code}"}
        data = r.json()
        return {"status": "ok", "query": q,
                "hits": data.get("hits", {}).get("hits", []),
                "n_hits": data.get("hits", {}).get("total", {}).get("value", 0)}
    except Exception as exc:
        return {"status": "error", "n_hits": 0, "query": q, "hits": [],
                "error_msg": str(exc)}


def find_recent_filing(cik: int, target_forms: list[str]) -> dict | None:
    """Return the most recent 10-K (or 20-F for foreign) for `cik`,
    falling back to the most recent DEF 14A if no annual report.

    The 10-K's "Employee Benefit Plans" footnote consistently describes
    the 401(k) match formula for the entire workforce. Proxy statements
    (DEF 14A) describe executive compensation and frequently say
    something like "we do not offer special retirement plans" without
    mentioning the regular employee 401(k) match.
    """
    url = EDGAR_SUBMISSIONS.format(cik=cik)
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return None
        sub = r.json()
        recent = sub.get("filings", {}).get("recent", {})
        accs = recent.get("accessionNumber", [])
        prims = recent.get("primaryDocument", [])
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        # Build candidate by form-priority, then most-recent
        ann_forms = {"10-K", "10-K/A", "20-F", "20-F/A"}
        proxy_forms = {"DEF 14A", "DEFA14A"}
        ann_match, proxy_match = None, None
        for acc, prim, frm, dt_ in zip(accs, prims, forms, dates):
            entry = {"cik": cik, "accession": acc, "primary": prim,
                     "form": frm, "filing_date": dt_,
                     "doc_url": (f"https://www.sec.gov/Archives/edgar/data/"
                                  f"{cik}/{acc.replace('-', '')}/{prim}")}
            if frm in ann_forms and ann_match is None:
                ann_match = entry
            elif frm in proxy_forms and proxy_match is None:
                proxy_match = entry
            if ann_match is not None:
                break
        return ann_match or proxy_match
    except Exception:
        return None


def edgar_search(name: str, forms: list[str]) -> dict:
    """Combined: ticker-list fuzzy match → submission API → return filing.

    Returns:
        {"status": "found"|"not_found"|"ambiguous"|"error",
         "cik": int|None, "company_name": str|None,
         "accession": str|None, "form": str|None,
         "filing_date": str|None, "doc_url": str|None,
         "match_score": float, "query": str, "error_msg": str|None}
    """
    base_result = {"status": None, "cik": None, "company_name": None,
                    "accession": None, "form": None, "filing_date": None,
                    "doc_url": None, "match_score": 0.0,
                    "query": name, "error_msg": None}
    try:
        idx = load_ticker_index()
    except Exception as exc:
        base_result["status"] = "error"
        base_result["error_msg"] = f"ticker index fetch: {exc}"
        return base_result

    best, score, confidence = fuzzy_name_match(name.upper(), idx)
    if best is None:
        # Try full-text search as a fallback for non-ticker companies
        # (private firms with public-debt 10-Ks register under different names)
        fts = edgar_full_text_search(name, forms)
        if fts["status"] == "error":
            base_result["status"] = "error"
            base_result["error_msg"] = fts.get("error_msg")
            return base_result
        if fts["n_hits"] == 0:
            base_result["status"] = "not_found"
            return base_result
        # If full-text returned hits, evaluate
        upper_name = name.upper()
        for h in fts["hits"]:
            src = h.get("_source", {})
            display = src.get("display_names", [""])[0]
            if upper_name in display.upper():
                ciks = src.get("ciks", [])
                if ciks:
                    cik = int(ciks[0])
                    adsh = h.get("_id", "").split(":")[0]
                    base_result["status"] = "found"
                    base_result["cik"] = cik
                    base_result["company_name"] = display
                    base_result["accession"] = adsh
                    base_result["form"] = src.get("form", "")
                    base_result["filing_date"] = src.get("file_date", "")
                    base_result["doc_url"] = (
                        f"https://www.sec.gov/Archives/edgar/data/"
                        f"{cik}/{adsh.replace('-', '')}/"
                    )
                    base_result["match_score"] = 2.0  # exact substring
                    return base_result
        # ambiguous: hits but none with exact-substring company match
        top = fts["hits"][0]
        top_name = top.get("_source", {}).get("display_names", [""])[0]
        base_result["status"] = "ambiguous"
        base_result["company_name"] = top_name
        base_result["error_msg"] = f"top FTS hit: {top_name}"
        return base_result

    # Ticker match: high or low confidence. We treat low-confidence
    # (1 distinctive token shared) as "ambiguous" so the user can review.
    cik = best["cik"]
    base_result["match_score"] = score
    filing = find_recent_filing(cik, forms)
    base_result["cik"] = cik
    base_result["company_name"] = best["name"]
    if filing is not None:
        base_result["accession"] = filing["accession"]
        base_result["form"] = filing["form"]
        base_result["filing_date"] = filing["filing_date"]
        base_result["doc_url"] = filing["doc_url"]
    if confidence == "high":
        base_result["status"] = "found"
    else:
        base_result["status"] = "ambiguous"
        base_result["error_msg"] = (
            f"low-confidence (1 distinctive token shared); candidate {best['name']}"
        )
    return base_result


def fetch_filing_text(doc_url: str) -> str | None:
    """Fetch the primary document of an EDGAR filing as plain text.
    `doc_url` is the direct URL to the primary HTML/text document.
    """
    if not doc_url:
        return None
    try:
        r = requests.get(doc_url, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            return None
        return r.text
    except Exception:
        return None


def extract_match_text(html_or_text: str) -> dict:
    """Find 401(k) match-formula language and return excerpt + summary."""
    if not html_or_text:
        return {"excerpt": "", "summary": "", "has_match": False,
                "has_safe_harbor": False, "has_profit_sharing": False,
                "has_discretionary": False}

    # Strip HTML tags crudely
    text = re.sub(r"<[^>]+>", " ", html_or_text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text)

    # Locate "401(k)" mentions and grab surrounding context
    # Use a broad regex that catches "401(k)", "401k", "401 (k)"
    rx_401k = re.compile(r"401\s*\(?\s*k\s*\)?", re.IGNORECASE)
    matches = list(rx_401k.finditer(text))
    if not matches:
        return {"excerpt": "", "summary": "", "has_match": False,
                "has_safe_harbor": False, "has_profit_sharing": False,
                "has_discretionary": False}

    # For each 401(k) mention, grab a window of ±800 chars and look for
    # match-formula language inside. Pick the first window that yields a
    # match-formula hit; otherwise return the first window verbatim.
    best_excerpt = ""
    summary_parts: list[str] = []
    has_match = False
    for m in matches[:8]:  # cap windows examined
        start = max(0, m.start() - 400)
        end = min(len(text), m.end() + 1200)
        window = text[start:end]
        if not best_excerpt:
            best_excerpt = window
        # Try each match-formula pattern
        for rx in MATCH_PATTERNS:
            mm = rx.search(window)
            if mm:
                has_match = True
                grps = mm.groups()
                if len(grps) >= 4 and grps[2] is not None:
                    summary_parts.append(
                        f"{grps[0]}% on first {grps[1]}%, "
                        f"{grps[2]}% on next {grps[3]}%"
                    )
                elif len(grps) >= 2 and grps[1] is not None:
                    summary_parts.append(
                        f"{grps[0]}% match up to {grps[1]}% of comp"
                    )
                elif len(grps) >= 1 and grps[0] is not None:
                    summary_parts.append(
                        f"dollar-for-dollar up to {grps[0]}%"
                    )
                best_excerpt = window
                break
        if has_match:
            break

    has_sh = bool(SAFE_HARBOR_RX.search(best_excerpt))
    has_ps = bool(PROFIT_SHARING_RX.search(best_excerpt))
    has_dc = bool(DISCRETIONARY_RX.search(best_excerpt))

    summary = "; ".join(summary_parts) if summary_parts else ""
    if has_sh and "safe harbor" not in summary.lower():
        summary = ("safe harbor; " + summary) if summary else "safe harbor"
    if has_dc and "discretionary" not in summary.lower():
        summary = ("discretionary; " + summary) if summary else "discretionary"

    return {"excerpt": best_excerpt[:1000].strip(),
            "summary": summary,
            "has_match": has_match,
            "has_safe_harbor": has_sh,
            "has_profit_sharing": has_ps,
            "has_discretionary": has_dc}


# --------------------- pipeline ---------------------

SCHEMA = [
    "search_index", "ein", "firm_name", "normalized_name", "state",
    "employee_count", "plan_effective_date",
    "search_status", "edgar_cik", "edgar_company_name",
    "filing_form", "filing_accession", "filing_date", "filing_doc_url",
    "match_text_excerpt", "match_formula_summary",
    "has_match", "has_safe_harbor", "has_profit_sharing", "has_discretionary",
    "search_query", "searched_at", "notes",
]


def main():
    df = pd.read_csv(DATA_PATH)
    cands = select_candidates(df, N_CANDIDATES)
    print(f"Selected {len(cands)} candidates")
    os.makedirs(os.path.dirname(DELIVERABLE), exist_ok=True)

    rows = []
    log_lines = []
    for i, row in cands.iterrows():
        idx = i + 1
        firm = row["FIRM_NAME"]
        name = row["normalized_name"]
        log_lines.append(f"[{idx}/{len(cands)}] {firm} -> '{name}'")
        print(log_lines[-1])

        rec = {
            "search_index": idx,
            "ein": row["EIN"],
            "firm_name": firm,
            "normalized_name": name,
            "state": row["STATE"],
            "employee_count": int(row["EMPLOYEE_COUNT"]),
            "plan_effective_date": row["PLAN_EFFECTIVE_DATE"],
            "search_status": "",
            "edgar_cik": "",
            "edgar_company_name": "",
            "filing_form": "",
            "filing_accession": "",
            "filing_date": "",
            "filing_doc_url": "",
            "match_text_excerpt": "",
            "match_formula_summary": "",
            "has_match": False,
            "has_safe_harbor": False,
            "has_profit_sharing": False,
            "has_discretionary": False,
            "search_query": "",
            "searched_at": dt.datetime.now().isoformat(timespec="seconds"),
            "notes": "",
        }

        result = edgar_search(name, TARGET_FORMS)
        rec["search_status"] = result["status"]
        rec["search_query"] = result.get("query", "")
        if result.get("error_msg"):
            rec["notes"] = result["error_msg"]
        time.sleep(0.3)

        if result["status"] in ("found", "ambiguous"):
            rec["edgar_cik"] = result["cik"] or ""
            rec["edgar_company_name"] = result["company_name"] or ""
            rec["filing_form"] = result["form"] or ""
            rec["filing_accession"] = result["accession"] or ""
            rec["filing_date"] = result["filing_date"] or ""
            rec["filing_doc_url"] = result["doc_url"] or ""

            log_lines.append(
                f"  -> [{result['status']}] CIK {result['cik']} "
                f"{result['company_name']} {result['form']} {result['filing_date']}"
            )
            print(log_lines[-1])

            html = fetch_filing_text(result.get("doc_url") or "")
            time.sleep(0.3)
            if html:
                ext = extract_match_text(html)
                rec["match_text_excerpt"] = ext["excerpt"]
                rec["match_formula_summary"] = ext["summary"]
                rec["has_match"] = ext["has_match"]
                rec["has_safe_harbor"] = ext["has_safe_harbor"]
                rec["has_profit_sharing"] = ext["has_profit_sharing"]
                rec["has_discretionary"] = ext["has_discretionary"]
                summary_short = ext["summary"][:80] if ext["summary"] else "(no formula extracted)"
                log_lines.append(f"  formula: {summary_short}")
                print(log_lines[-1])
            else:
                rec["notes"] = (rec["notes"] + " | " if rec["notes"] else "") + \
                                "filing text not retrievable"
        elif result["status"] == "ambiguous":
            rec["edgar_company_name"] = result.get("company_name", "")
            rec["notes"] = (rec["notes"] + " | " if rec["notes"] else "") + \
                            f"top hit was {result.get('company_name', '')}"

        rows.append(rec)

    with open(DELIVERABLE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        w.writerows(rows)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    # Summary
    n_found = sum(1 for r in rows if r["search_status"] == "found")
    n_match = sum(1 for r in rows if r["has_match"])
    n_sh = sum(1 for r in rows if r["has_safe_harbor"])
    n_nf = sum(1 for r in rows if r["search_status"] == "not_found")
    n_amb = sum(1 for r in rows if r["search_status"] == "ambiguous")
    n_err = sum(1 for r in rows if r["search_status"] == "error")
    print(f"\nSummary: {len(rows)} searched, {n_found} found, {n_nf} not_found,"
          f" {n_amb} ambiguous, {n_err} error")
    print(f"Match formula extracted: {n_match}")
    print(f"Safe-harbor mentioned: {n_sh}")
    print(f"Output: {DELIVERABLE}")


if __name__ == "__main__":
    main()
