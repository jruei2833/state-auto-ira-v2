# Data Collection Spec: BLS QCEW (Quarterly Census of Employment and Wages)

**Project:** State Auto-IRA Research
**Workstream:** DiD denominator sensitivity check
**Purpose:** Provide a third denominator alongside Census CBP and Census SUSB so the DiD's headline ATT is not dependent on one denominator choice. QCEW is the most-current and most-granular employment data available; if the headline ATT is robust across CBP, SUSB, and QCEW denominators, that closes a class of methodological objections.
**Output target:** `data/bls_qcew/`, updated DiD sensitivity panels, and `analysis/did_denominator_sensitivity.md`

---

## Why QCEW

QCEW is the BLS's quarterly count of employment and wages for the entire universe of establishments covered by state unemployment insurance. It's the gold-standard employment denominator for state-level analysis: more current than CBP, and unlike CBP it's quarterly. Coverage is approximately 95% of US jobs.

The trade-off versus SUSB is that QCEW is establishment-based (like CBP), not firm-based. So QCEW is conceptually closer to CBP than to SUSB. Using QCEW alongside CBP tests whether the CBP-based result depends on the specific Census methodology; using SUSB tests whether the establishment-vs-firm distinction matters.

The headline ATT should be roughly unchanged under QCEW vs CBP (both are establishment counts, similar coverage, different agencies). Material divergence between QCEW and CBP would itself be a finding worth investigating.

## Data source

QCEW is downloadable for free from BLS at:
- https://www.bls.gov/cew/downloadable-data-files.htm

For state-level annual averages by year, the relevant files are the "single state" or "state and county high level" annual averages. For 2017 through most recent available year (likely 2024 or partial 2025).

The relevant variables per state-year:
- Total private establishment count, annual average
- Total private employment, annual average

Pull *only the private sector aggregates* (NAICS supersector "10" or industry code variants for total private). Do not pull by detailed NAICS unless explicitly needed — keep this collection focused.

## Tasks

### Task 1: Pull and standardize QCEW

Download QCEW state-level annual files for 2017 through most recent available. Store raw downloads in `data/bls_qcew/raw/`. Standardize into a single panel at `data/bls_qcew/state_year_private_establishments.csv` with columns:

```
state | year | private_establishments | private_employment | source_url
```

### Task 2: Compare QCEW to CBP

Before running any DiD, build a comparison table at `analysis/qcew_vs_cbp_levels.md`:

```
state | year | cbp_establishments | qcew_establishments | ratio | absolute_diff
```

For most state-years the ratio should be close to 1.0 (CBP and QCEW count similar things from different administrative sources). If any state-year has a ratio meaningfully different from 1.0, document and investigate before proceeding to DiD. Most likely cause of divergence is timing-of-measurement differences (CBP is a March snapshot; QCEW is annual average).

### Task 3: Re-run CS-DiD with QCEW denominator

Add a new outcome column to the existing DiD panels:
- `new_401k_per_1000_qcew_establishments`

Run the same Callaway-Sant'Anna specification as the headline. Report alongside the CBP-based and SUSB-based estimates in a single sensitivity table.

### Task 4: Three-denominator sensitivity table

Produce `analysis/did_denominator_sensitivity.md` with the headline ATT under all three denominator choices:

```
| Denominator | Source | Conceptual unit | ATT (v1) | ATT (v2) |
|---|---|---|---|---|
| CBP establishments | Census | Physical location | 2.37 | 2.37 |
| QCEW establishments | BLS | UI-covered worksite | TBD | TBD |
| SUSB firms | Census | Legal entity | TBD | TBD |
| SUSB firms 5+ employees | Census | Legal entity, mandate-eligible | TBD | TBD |
```

The story to tell in the writeup: the headline finding is robust to which denominator we use, with the absolute magnitude shifting predictably (firms < establishments, so per-firm rates are higher than per-establishment rates). The qualitative conclusion (mandates cause meaningful 401(k) plan formation) does not depend on denominator choice.

If the conclusion *does* depend on denominator choice, that is a substantive finding to investigate, not a sensitivity check to bury.

## Guardrails

QCEW excludes some categories that CBP includes (and vice versa). The most material exclusions:
- QCEW excludes elected officials, members of armed forces, most agricultural workers on small farms, railroad employees, and certain religious organizations
- CBP excludes self-employed persons, employees of private households, railroad employees, agricultural production workers, and most government employees

For the project's mandate-relevant population (private-sector firms with employees), these exclusions are mostly equivalent. Document the residual scope difference but don't try to harmonize — both are widely accepted as private-sector employer denominators.

QCEW data is published with about a 6-month lag. 2024 annual data should be available now; 2025 will be partial.

## What this does NOT do

- Does not pull QCEW by industry detail (separate ask)
- Does not pull QCEW by ownership sector (private only is fine for project purposes)
- Does not replace CBP or SUSB — provides a third comparison point

## Definition of done

This task is done when:
1. QCEW panel is built
2. QCEW vs CBP comparison table exists and is sane (ratios near 1.0)
3. DiD has been re-run with QCEW denominator
4. Three-denominator sensitivity table is produced
5. The headline robustness conclusion is documented one way or the other

If all three denominators give similar qualitative conclusions, this workstream closes the "but what if you used a different denominator" reviewer objection. That's the goal.
