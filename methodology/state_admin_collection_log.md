# State-Administrative Data Collection Log

**Workstream:** Externally-validated firm-side cross-check
**Spec:** `methodology/state_admin_collection_spec.md`
**Output:** `data/state_admin/`
**Pull date:** 2026-05-06
**Method:** Public-source-only (program websites, sponsoring agency pages, board meeting materials, press releases). No CPRA/FOIA. Many statistics extracted from PDFs via direct download + pypdf parsing.

This log documents per-state what sources were checked, what was found vs. what was not published, and any source conflicts.

---

## CA — CalSavers

**Sources checked:**
- CalSavers main site `calsavers.com` (about page) — confirmed program-level totals (281,000+ employers, 629,000+ savers, $1.6B+ assets as of March 31 2026 reporting cycle).
- CA State Treasurer reports page `treasurer.ca.gov/calsavers/reports/2025/` — listed monthly Participation Summary Report PDFs from Jan 2025 - Dec 2025.
- December 2025 monthly report PDF — primary source.

**Found:**
- Cumulative exempt employers: **208,412** (as of 12/31/2025).
- Registered employers: **255,793**.
- Funded accounts: **599,352**.
- Payroll Contributing Accounts: **711,760**.
- Total Assets: **$1,587,939,563**.
- Multiple Employer Accounts: **111,833**.
- Self-Enrolled Funded Accounts: **3,226**.
- Effective opt-out rate: **35.40%**.
- Cumulative contributions: **$1,744,084,919**.
- Cumulative withdrawals: **$463,214,435**.
- Account balance distribution (6 bands).
- Wave-level breakdown: Prior Waves, Wave 4 (12/31/2025 deadline for 1-4 employees), Wave 2025 (new employers).
- Total estimated eligible employer universe: **891,271**.

**Not published:** Industry breakdown.

**No conflicts.** CalSavers monthly Participation Summary Report is the single canonical source.

**As-of date used:** 2025-12-31.

---

## OR — OregonSaves

**Sources checked:**
- `oregonsaves.com` employer/about pages — does not publish current statistics.
- OR State Treasury Upward Oregon page `oregon.gov/treasury/upward-oregon/pages/oregon-retirement-savings-board.aspx` — links to board materials.
- ORSB board materials (Feb 2025, May 2025, Aug 2025, Nov 2025).
- August 2025 board materials (PDF, 143 pages) — primary source for current dashboard.
- November 2025 minutes — provided $420M assets reference, no exempt update.

**Found:**
- Cumulative exempt employers: **46,914** (as of 6/30/2025, per Quarterly Dashboard p.94).
- Registered employers: **32,190**.
- Funded accounts: **137,765**.
- Payroll Contributing Accounts: **174,974**.
- Total Assets: **$384,333,069**.
- Multiple Employer Accounts: **92,770**.
- Wave 2025 update (as of 7/31/2025): 12,088 new employer records added to program from state data file updates; 8,287 employers with 1+ employee communicated; 787 registered, 1,057 exempt, 3,802 exempt by Form 5500 prior to communications, 5 communications total.

**Not published:** Pre-2025 exemption count by year/wave; industry/employer-size breakdowns.

**No conflicts.** Vestwell/Sellwood Quarterly Dashboard is the canonical source.

**As-of date used:** 2025-06-30 (current as of August 2025 board meeting). November 2025 minutes mentioned ">$420M in plan and over 5,000 new savers" but no updated exempt count.

---

## IL — Illinois Secure Choice

**Sources checked:**
- IL Treasurer Secure Choice page `illinoistreasurer.gov/Individuals/Secure_Choice/Secure_Choice_Performance_Dashboards` — links to monthly dashboards.
- March 2026 Monthly Dashboard PDF — primary source.

**Found:**
- Cumulative exempt employers: **72,872** (as of 3/31/2026).
- Registered employers: **27,303**.
- Funded accounts: **169,745**.
- Payroll Contributing: **197,607**.
- Total Assets: **$316,907,088**.
- Effective opt-out rate: **37.17%**.
- Full withdrawal rate: **27.01%**.
- Average funded account balance: **$1,866.96**.
- Average contribution rate: **6.53%**.

**Not published:** Industry/size breakdowns; ERIC member exemption details (covered by separate MOU per ERIC press release).

**No conflicts.** Monthly Dashboard is the canonical source.

**As-of date used:** 2026-03-31.

---

## CT — MyCTSavings

**Sources checked:**
- `myctsavings.com` (homepage, about) — no statistics.
- CT Office of State Comptroller `osc.ct.gov/crsp/` — current snapshot ($67.36M assets, 38,209 savers, 7,710 employers as of 5/1/2026). No exemption count.
- CRSP 2023 Annual Report PDF (`osc.ct.gov/wp-content/uploads/2025/03/CRSP-2023-Annual-Report-Final.pdf`) — FY2023 metrics: 4,414 registered, 15,981 savers, $6.5M assets.
- October 18, 2023 press release: "over 10,900 companies have certified they offer their own retirement plans."
- Connecticut General Statutes §31-426 — annual report due to General Assembly by Dec 31. Only FY2023 annual report posted publicly.

**Found:**
- Cumulative exempt employers: **10,900** (as of 10/18/2023, press release).
- Registered employers: **7,710** (current).
- Active savers: **38,209** (current).
- Total Assets: **$67,360,000** (current).
- Funded accounts as of 12/31/2025: **36,307** (cited via third-party tax alert summarizing program update).

**Not published:** Updated cumulative exemption count (the 10,900 figure is dated October 2023). FY2024 and later annual reports not posted publicly. Industry/size breakdown not published.

**Conflicts:** None outright, but the 10,900 exemption number is 2.5 years stale. CRSP reports page `osc.ct.gov/crsp/reports/` shows "No publications found" — monthly statistics reports referenced in the FY2023 annual report do not appear to be currently posted.

**As-of date for exempt count:** 2023-10-18 (press release).

---

## MD — MarylandSaves

**Sources checked:**
- `marylandsaves.org` and `marylandsaves.com` — no quantitative dashboard.
- MarylandSaves Board of Trustees page — meeting minutes from 2024 and 2025 do not contain detailed registration/exemption tables.
- DLS Office of Policy Analysis "Evaluation of the Maryland Small Business Retirement Savings Program" (December 2024) — primary source.
- 2025 Board Meeting Minutes (March, June, September) — qualitative discussion; no fresh statistics.
- 2025 SDAT fee waiver list page — does not publish a count.

**Found (DLS 2024 Evaluation, as of June 30, 2024):**
- Businesses enrolled in MarylandSaves: **3,812**.
- Businesses actively submitting payroll: **1,189**.
- Funded accounts: **8,744**.
- Total Assets: **$9,200,000**.
- SDAT fee waiver list (TY2023): **22,048** businesses submitted by MarylandSaves; **21,958** entities enrolled per SDAT (small discrepancy attributed to forfeited/dissolved businesses); **20,727** annual reports filed with fees waived.
- SDAT fee waiver list (TY2024): **20,200** businesses.
- Of fee waiver businesses (June 2024 breakdown): ~14,100 with retirement plan, **~5,000 with certified program exemption**, ~3,800 enrolled in MarylandSaves.
- Average funded account balance: **$1,050**, median **$410**.

**Not published:** Updated 2025 statistics (DLS evaluation is the most recent comprehensive report). Industry breakdown.

**Conflicts noted:** SDAT fee waiver count (~22,048 TY2023) vs. program-exemption-only count (~5,000) is a definitional difference, not a conflict — but using the wrong number is misleading. Documented in `analysis/state_admin_vs_v3.md`.

**As-of date used:** 2024-06-30 (most recent comprehensive published figures).

---

## CO — Colorado SecureSavings

**Sources checked:**
- `coloradosecuresavings.com` — 403 forbidden via WebFetch (likely bot blocking); did not retry repeatedly.
- CO Treasury press releases (multiple, 2024-2026).
- CSSP 2024 Annual Board Report (April 2024 PDF) — primary source.
- Colorado Secure Savings Program Board page on Treasury site — was 403 via WebFetch.

**Found (CSSP 2024 Annual Report, ~April 1, 2024):**
- Enrolled employers: **14,332**.
- Verified offer retirement plan (treated as cumulative-exemption-equivalent): **26,000**.
- Open accounts: **68,374**.
- Funded accounts: **51,814**.
- Total Assets: **$48,000,000**.
- Average monthly contribution: **$194.08**.
- Average funded account balance: **$940.96**.
- Unregistered employers (Feb 2024): **~42,000**.

**Found (more recent press releases, August 2025 / February 2026):**
- August 2025: 17,025 registered, 85,000 savers, $140M+ assets.
- February 2026: 100,000+ savers (CO press release "Surges Past 100,000 Savers").

**Not published in 2025-2026 press releases:** Updated 5500-pre-exempted count.

**Conflicts noted:** None within CO sources. The 26,000 "verified offer retirement plan" Apr-2024 figure is the closest analog to "cumulative exemption" available; later press releases focus on registered/savers/AUM and do not refresh this metric.

**As-of date for exemption proxy:** 2024-04-01.

---

## VA — Commonwealth Savers (formerly Virginia529 / RetirePath VA)

**Sources checked:**
- `retirepathva.com` — does not publish numerical statistics.
- `virginia.gov/agencies/commonwealth-savers-plan/` — describes program; no statistics.
- JLARC `Commonwealth_Savers_2025_Annual_Status_Slides.pdf` (July 14, 2025 board presentation) — primary source.
- CommonwealthSavers.com — annual reports section (could not retrieve).

**Found (JLARC 2025 presentation, as of May 31, 2025):**
- Funded RetirePath accounts: **16,400** (slide 13: "in AUM 16.4K Funded Accounts Launched June 20, 2023").

**Not published:**
- **Registered employers** — not in JLARC slides.
- **Exemption count** — not in JLARC slides; not in any VA published source found.
- **Total Assets / AUM** — slide 3/13 mentions but the layout obscured the dollar amount in text extraction; the chart shows ~$140M-ish at June 2025 but cannot cite precisely.

This is a published-data limitation, not a research gap. VA's mandate covers 25+ employee firms (a smaller universe than CA/OR/IL).

**Conflicts noted:** None.

**As-of date for funded accounts:** 2025-05-31. Exemption / registered employer counts: **NOT PUBLISHED**.

---

## ME — MERIT (Maine Retirement Investment Trust)

**Sources checked:**
- `meritsaves.org` (homepage and media page) — banner statistic only.
- MERIT press release "Maine workers save $25 million for retirement" (January 5, 2026) — primary source for participating employers and savers.
- Maine Public article (Dec 30, 2024) — earlier-period statistics.
- Maine State Treasurer Maine Retirement Savings Board page — links to MERIT but no statistics page.

**Found:**
- Participating employers (Jan 5, 2026 press release): **3,000+**.
- Active savers (Jan 5, 2026): **18,200**.
- Total Assets: **$25,000,000**.
- Combined "registered or exempted" (MERIT media page banner): **8,000+**.
- Implied exempted count: **~5,000** (8,000 - 3,000).
- December 2024: 2,506 registered, 12,015 funded savers, $8.2M assets.
- Eligible employer universe at full rollout (Jan 2024): ~10,000 employers / ~200,000 employees (~40% of ME private sector workforce).

**Not published:**
- Direct exempted count — only the combined "registered or exempted" banner statistic.
- Industry/size breakdown.

**Conflicts noted:** None internal. The 8,000 banner stat is approximate; the 3,000 participating count is from a press release. Treating implied exempted as ~5,000 is an inference but the spec allows reasonable transcription.

**As-of date used:** 2026-01-05.

---

## DE — Delaware EARNS

**Sources checked:**
- `treasurer.delaware.gov/earns/` and `earnsdelaware.com` — landing/program detail pages.
- DE Treasury press releases: launch (July 2024), $1M milestone (Feb 2025), Oct 2025 deadline reminder, $10M milestone (April 2026).
- April 14, 2026 press release: primary source for current numbers.

**Found:**
- Registered employers (April 13, 2026): **1,944**.
- Funded accounts (April 13, 2026): **9,219**.
- Total Assets (April 13, 2026): **$10,500,000**.
- Average funded account balance: **$1,139.64**.
- Average contribution rate across plan: **5.64%**.
- Earlier milestones: Feb 2025 — 1,596 registered, 4,590 funded, $1.4M; October 2025 — 7,500+ savers, $6M+.

**Not published:** Cumulative exemption count. Press releases mention employers can certify exemption (5+ W-2 employees, 6+ months in business as eligibility threshold) but do not publish how many have certified exemption.

**Conflicts noted:** None.

**As-of date for available metrics:** 2026-04-13. Exemption count: **NOT PUBLISHED**.

---

## NJ — RetireReady NJ

**Sources checked:**
- `nj.gov/treasury/securechoiceprogram/` (program page) — describes program; no current statistics.
- NJ Treasury news 7/7/2025 release "RetireReady NJ Marks One Year of Operation" — primary 2025 source.
- February 6 2026 RetireReady NJ Program Amended document (PDF) — current snapshot.
- NJ Monitor / NJBIZ / Insider NJ press coverage — secondary.

**Found:**
- July 7, 2025 press release: 1,200+ employers, 18,000+ savers, $8.1M+ AUM.
- Feb 6, 2026 program-amended document: 25,000+ savers, $18M+ saved (employer count not refreshed).

**Not published:**
- **Cumulative exemption count** — not in any NJ Treasury source found.
- Industry/size breakdown.

**Conflicts noted:** None internal. NJ recently expanded program coverage from 25+ employee firms to 10+ employee firms (A5358 signed Jan 2025), so current eligible universe is now larger than the period when the v3 dataset's NJ EINs were observed.

**As-of date for available metrics:** 2026-02-06. Exemption count and current registered count: **NOT PUBLISHED**.

---

## Summary of published data limitations

| state | publishes exemption count? | publishes registered employers? | publishes savers? | publishes AUM? |
|-------|:---:|:---:|:---:|:---:|
| CA | yes (monthly) | yes | yes | yes |
| OR | yes (quarterly board materials) | yes | yes | yes |
| IL | yes (monthly) | yes | yes | yes |
| CT | partial (one 2023 press release) | yes (current) | yes | yes |
| MD | partial (DLS 2024 evaluation; SDAT fee waiver count differs definitionally) | yes | yes | yes |
| CO | partial (April 2024 annual report only) | yes | yes | yes |
| VA | **no** | no | partial (funded accounts only) | partial |
| ME | partial (combined banner statistic) | yes | yes | yes |
| DE | **no** | yes | yes | yes |
| NJ | **no** | partial (mid-2025 figure only) | yes | yes |

Three states (VA, DE, NJ) do not publish exemption counts and therefore cannot be compared to v3 firm counts on this dimension. This is documented and not estimated per the spec.

## Methodological notes

1. **Exemption-count definitions vary by state.** Some states (CA, OR, IL) report cumulative employer-self-certified exemptions. CO reports both employer-certified and Form-5500-pre-exempted (the 26,000 figure is a hybrid). MD reports SDAT fee waiver entries which include broader categories than program-exemption only. The comparison table normalizes to the closest available "certified program exemption" figure but the user should be aware that definitions are not perfectly identical state-to-state.

2. **As-of dates differ.** Most-recent published data ranges from October 2023 (CT exemption count) to April 2026 (DE press release). The cross-state comparison is therefore not strictly contemporaneous. v3 firm counts reflect Form 5500 filings through whatever build date generated `data/v2-conservative/state_auto_ira_401k_dataset.csv`.

3. **No dataset estimation.** Per the spec, where a state does not publish a number we documented its absence rather than estimating from indirect signals. ME's "implied exempted ~5,000" is the only inference made, and it follows directly from arithmetic on two published banner statistics.

4. **PDF extraction.** Several state programs publish key metrics only in PDF form (CA monthly reports, OR board materials, IL monthly dashboards, CO annual report, MD DLS evaluation). All extraction was via download + pypdf parsing, not manual transcription, with the exception of summary numbers cited in webfetch responses where the PDF was inaccessible (e.g., MarylandSaves employer fact sheet was 403).
