# 401(k) Match Formula Industry Benchmarks

**Date:** 2026-04-29
**Purpose:** Industry-level benchmarks on 401(k) match formulas, used as substitute for firm-level data when neither SEC EDGAR nor BrightScope yields firm-specific match-formula data for the State Auto-IRA dataset.

> **Important caveat — read first.**
>
> The data in this document is **aggregate industry data**, not firm-specific. It describes typical match-formula prevalence across the broader 401(k) market — not the specific match formulas of the 106,577 firms in the v2-conservative dataset. The State Auto-IRA dataset's firms are predominantly small private companies establishing new 401(k)s after a state mandate, while these benchmark sources skew toward larger, established plans. Use these benchmarks for **context** about what match formulas look like in the broader market, not as a substitute for firm-specific evidence.
>
> Where benchmark sources stratify by plan size, the smaller-plan strata are more comparable to the State Auto-IRA dataset.

## Source summary

| Source | Coverage | Year | Sample | Access |
|---|---|---|---|---|
| Vanguard *How America Saves 2025* | Vanguard recordkept DC plans | 2024 plan year | ~5M participants in ~1,500 plans | Free PDF, [corporate.vanguard.com](https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf) |
| PSCA 68th Annual Survey of 401(k) Plans | Plan-sponsor self-reports | 2024 plan year | 755 plans | Paid (~$500-$1,000); statistics here cited from [PSCA press release Nov 2025](https://www.psca.org/news/psca-news/2025/11/psca-annual-survey-participation-climbs-as-employers-embrace-secure-2.0-flexibility) |
| ICI/BrightScope *Defined Contribution Plan Profile* | Form 5500 audited 401(k) filings | 2020 plan year (most recent free release) | ~65,000 large plans | Free PDF, [ici.org](https://www.ici.org/system/files/2023-09/23-rpt-dcplan-profile-401k.pdf) |

## 1. Headline rates

| Statistic | Vanguard 2024 | PSCA 2024 | ICI/BrightScope 2020 |
|---|---|---|---|
| % of plans with any employer contribution | 96% | 81.3% (any match) | 86.9% (large plans) |
| % match-only | 50% | 52.5% | — |
| % both match + non-matching | 36% | 28.5% | — |
| % non-matching only | 10% | n/a | — |
| % no employer contribution | 4% | n/a | 13% |
| Average employer contribution rate | 4.6% of pay (promised match) | 4.8% of pay (actual) | n/a |
| Median employer contribution rate | 4.0% of pay (promised match) | n/a | n/a |
| Average employee deferral | n/a | 7.7% of pay | n/a |
| Total savings rate (employer + employee) | n/a | 12.5% of pay | n/a |

The three sources broadly agree on the prevalence of matching: roughly **80-95% of plans offer some form of employer contribution**, and **around half of all plans use a match-only design**. The match averages around **4-5% of pay** when expressed as the maximum value of the employer-promised match.

## 2. Most common match formulas (across the industry)

### Vanguard 2025 (Figure 8): top 5 match formulas

| Match formula | % of Vanguard plans with a match |
|---|---|
| 50% on first 6% of pay | 13% |
| 100% on first 3% + 50% on next 2% | 10% |
| 100% on first 6% of pay | 9% |
| 100% on first 5% of pay | 7% |
| 100% on first 4% of pay | 6% |

### ICI/BrightScope 2020 (Exhibit 1.8): cross-tab of match rate × deferral percentage matched

Among large plans with a *simple match formula* (50.5% of large plans with employer contributions):

| Match rate \\ Max deferral matched | <3% | 3% | 4% | 5% | **6%** | 7-9% | 10%+ | Other | **Row total** |
|---|---|---|---|---|---|---|---|---|---|
| 25% | 0.0 | 0.9 | 2.5 | 2.2 | 3.1 | 2.4 | 0.1 | 0.0 | 11.2% |
| **50%** | 2.5 | 1.2 | 7.4 | 3.0 | **21.9** | 3.9 | 0.7 | (*) | **40.6%** |
| 75% | 0.0 | 0.0 | 0.1 | (*) | 0.9 | 0.2 | 0.0 | (*) | 1.3% |
| **100%** | 2.5 | 5.2 | 13.0 | 7.9 | 6.0 | 0.1 | 0.1 | 1.9 | **36.6%** |
| Other | 0.4 | (*) | 0.4 | 2.4 | 4.7 | 0.6 | 1.8 | 0.0 | 10.3% |
| **Column total** | 5.3 | 7.4 | 23.4 | 15.5 | **36.5** | 7.1 | 2.7 | 2.0 | 100% |

Reading the ICI/BrightScope table:
- **The single most common simple-match formula is 50% on first 6% of pay**, used by **21.9% of large plans with simple matches** (so ~21.9% × 50.5% = ~11% of all large 401(k) plans).
- Next most common simple-match formula: **100% on first 4% of pay** (13.0% of plans with simple matches).
- Of plans using simple matches, **40.6% match at 50¢ per dollar**, **36.6% match dollar-for-dollar**, and **11.2% match at 25¢ per dollar**.
- The 6% deferral threshold (the maximum employee deferral the employer will match) dominates: **36.5% of all simple-match formulas** stop matching at the 6% deferral level.

Both Vanguard and ICI/BrightScope agree that **50% on first 6%** is the single most common formula and that **100% on first 3%, 50% on next 2%** (a multi-tier safe-harbor formula) is the most common multi-tier formula.

## 3. Plan-design dispersion (Vanguard, 2024)

Promised match value (max possible employer contribution as % of pay), among plans with a single- or multi-tier match formula:

| Promised match % of pay | % of Vanguard plans |
|---|---|
| <0.5% | 0% |
| 0.5-0.99% | 1% |
| 1.00-1.99% | 4% |
| 2.00-2.99% | 6% |
| **3.00-3.99%** | **28%** |
| **4.00-4.99%** | **29%** |
| 5.00-5.99% | 12% |
| 6.00-6.99% | 13% |
| 7%+ | 7% |

**Distribution is bimodal-ish around 3-5% of pay.** The interquartile range is roughly 3.0% to 5.0% of pay; relatively few plans promise less than 2% or more than 7%.

## 4. Required employee deferral for maximum match (Vanguard 2024)

| Required employee deferral | % of plans |
|---|---|
| <4% | 7% |
| 4.0-4.99% | 13% |
| 5.0-5.99% | 25% |
| **6.0-6.99%** | **45%** |
| 7%+ | 10% |

**6% is the modal required-employee-deferral threshold** to maximize the match. The average required deferral is **6.5%**, the median **6.0%**. This has been declining slightly: the 10-year average required deferral fell from 7.4% (2017) to 6.5% (2024).

## 5. Vesting

| Statistic | PSCA 2024 | ICI/BrightScope 2020 |
|---|---|---|
| % of plans with immediate vesting of employer match | 44.1% | 53.9% |
| % of plans with eligibility ≤ first year of service | n/a | 76% (cumulative) |
| Most common eligibility/vesting combination | n/a | "Within first year + immediate vesting" (23.8% of plans) |

Vanguard's report does not break vesting out separately at the formula level; PSCA and ICI/BrightScope are the more useful sources here.

## 6. Plan-size relationship (ICI/BrightScope 2020)

Larger plans (by both participants and assets) are more likely to:

- **Offer any employer contribution** (>96% at $250M+ in plan assets, vs. 50.5% at $10M or less)
- **Make automatic (non-matching) contributions** (~24% at $100M+ vs. 10.6% at $10M or less)
- **Have participant loans outstanding** (>97% at $100M+ vs. 78% on average)

The implication for the State Auto-IRA dataset: since 62% of those firms are solo or micro (0-9 participants — well below the 100-participant threshold for ICI/BrightScope inclusion), benchmarks from these sources may **overstate** match prevalence and richness for the population of mandate-induced plans. We have no rigorous benchmark for sub-100-participant plans because Form 5500 audited filings (the BrightScope universe) only kick in at 100 participants.

## 7. Most defensible "industry standard" framing for the policy memo

Combining the three sources, a defensible summary statement for the policy memo:

> Across the broader 401(k) industry, **roughly 80% of plans offer an employer matching contribution**. Among those, the most prevalent design is a **simple match formula of 50% on the first 6% of compensation** (used by approximately one-fifth of plans with a simple match). The **average maximum employer-promised match is 4.0-4.6% of pay**, with most plans falling in a range of 3-5% of pay. Around half of plans offer immediate vesting of the employer match.
>
> *Caveat:* These benchmarks come from samples skewed toward larger employers (Vanguard recordkept plans, BrightScope audited filings ≥100 participants, PSCA self-reported). The State Auto-IRA dataset's mandate-induced plans are predominantly small (62% solo or micro), and small-plan match-formula data at this level of detail is not publicly available in any single source.

## 8. What we would still want, but cannot get publicly

- **Match-formula prevalence stratified by firm size below 100 employees.** This is precisely the population in the State Auto-IRA dataset, and it's the population that's least represented in industry benchmarks because Form 5500 audited filings only require detailed schedules for plans with ≥100 participants. The data exists in the Form 5500 plan-document attachments (which include summary plan descriptions filed as PDFs), but parsing those at scale is itself a major project. BrightScope, via its audited-filings universe, also does not cover sub-100-participant plans.
- **Whether mandate-induced plans differ from non-mandate plans on match design.** This would require firm-level match-formula data from both groups; without it, we can't say whether mandate-state firms tend to offer richer or sparser matches than firms in non-mandate states.
- **Whether mandate-induced plans use safe-harbor designs at higher rates.** Safe-harbor 401(k)s are commonly chosen by small employers because they avoid annual nondiscrimination testing — a plausible mechanism for mandate-induced firms specifically. PSCA's annual survey reports safe-harbor adoption but doesn't break out by mandate-state status.

## 9. Files

- `analysis/benchmark_sources/vanguard_how_america_saves_2025.pdf` — full report (PDF, ~9 MB)
- `analysis/benchmark_sources/ici_brightscope_dc_plan_profile_2023.pdf` — most recent free ICI/BrightScope DC profile (2020 plan year), 80pp
- (PSCA 68th Annual Survey: not redistributed — paid product; statistics in §1 cited from PSCA's public press release)
