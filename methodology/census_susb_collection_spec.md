# Data Collection Spec: Census SUSB (Statistics of US Businesses)

**Project:** State Auto-IRA Research
**Workstream:** Improved DiD denominator and firm-level descriptive context
**Purpose:** Integrate Census SUSB firm-level data as a primary or sensitivity-check denominator for the DiD, replacing or supplementing Census County Business Patterns (CBP) which is establishment-based rather than firm-based.
**Output target:** `data/census_susb/`, updated DiD panels, and `analysis/susb_vs_cbp_sensitivity.md`

---

## Why SUSB matters and why CBP isn't enough

The current DiD uses Census County Business Patterns (CBP) as the denominator: new 401(k) plans per 1,000 private establishments. CBP is the right starting point because it's monthly-updated and granular, but it has a meaningful conceptual mismatch with the project's outcome variable.

CBP counts **establishments** (physical locations). One firm with five locations counts as five CBP units. The Form 5500 outcome counts **plans**, which are sponsored at the firm level — a firm with five locations sponsors one 401(k) plan.

Census SUSB counts **firms** (legal entities, with a separate "establishments" count for cross-reference). Using SUSB firm counts as the denominator gives "new 401(k) plans per 1,000 private firms" — a direct firm-to-firm ratio that better matches the unit of analysis.

The expected effect on the DiD: SUSB firm counts are smaller than CBP establishment counts (multi-establishment firms are more common than single-establishment firms in the larger size bands), so the denominator shrinks and the per-1,000 rate rises. The headline ATT estimate should *increase* in absolute magnitude when re-expressed per 1,000 firms vs. per 1,000 establishments. The percentage change story doesn't shift.

This is not a complete replacement of CBP — both should be reported. SUSB becomes the headline denominator because it's the better firm-to-firm match; CBP stays as a sensitivity check.

## Data source

SUSB is downloadable for free from Census at:
- Annual data tables: https://www.census.gov/programs-surveys/susb/data/tables.html
- The relevant series is "U.S. & states, NAICS, detailed employment sizes" — specifically the state-level files

For each year 2017-2023, pull the state-by-employment-size-class table. Census publishes SUSB on roughly a 2-year lag, so 2024 may not be available; use most recent available and document the cutoff.

The relevant variables per state-year:
- Number of firms (any size)
- Number of firms by employment-size class: 0-4, 5-9, 10-19, 20-99, 100-499, 500+
- For cross-reference: number of establishments (should approximately match CBP)

## Tasks

### Task 1: Pull and standardize SUSB

Download SUSB state-level files for 2017 through most recent available year. Store raw downloads in `data/census_susb/raw/`. Standardize into a single panel at `data/census_susb/state_year_firms_by_size.csv` with columns:

```
state | year | size_class | firm_count | establishment_count | source_url
```

Where `size_class` takes values: "all", "0-4", "5-9", "10-19", "20-99", "100-499", "500+".

### Task 2: Rebuild DiD panels with SUSB denominator

Take the existing v1-inclusive and v2-conservative state-year panels (the ones used for the published CS-DiD result) and add new outcome columns:

- `new_401k_per_1000_firms` (SUSB-based, all firm sizes)
- `new_401k_per_1000_firms_5plus` (SUSB-based, restricted to firms with 5+ employees — the relevant universe for most state mandates)

The 5+ restriction matters because most state mandates apply only to firms with 5 or more employees (CT, IL, MD, CO, OR-after-2023, VA-25+). California and Oregon are the exceptions that extend to 1+ employees. Document state-by-state which size threshold applies and consider running both: full SUSB firm count, and SUSB firm count restricted to the actually-mandated size band per state.

### Task 3: Re-run CS-DiD on the SUSB-denominator panels

Run the same Callaway-Sant'Anna specification (not-yet-treated comparison, both v1 and v2 panels) using the new outcome variables. Compare to the published CBP-based results.

Output to `analysis/did_results_susb_v1_inclusive.csv`, `analysis/did_results_susb_v2_conservative.csv`, and a comparison writeup `analysis/susb_vs_cbp_sensitivity.md`.

The expected finding is that estimates rise in absolute magnitude but the qualitative result (ATT > 0, robust to dropping CA, etc.) is unchanged. If estimates *fall* or change sign, that's a substantive finding about the difference between firm-level and establishment-level denominators that needs investigation, not a robustness check that quietly replaces the headline.

### Task 4: Update the firm-level descriptive analysis

The firm-level analysis showed 62% of mandate-induced plans are solo or micro (0-9 participants). With SUSB, we can normalize that against the actual firm-size distribution per state — i.e., how many 0-9 employee firms exist in each mandate state — and report mandate-induced plan formation as a *rate* per firm-size band, not just a share of plans.

Output to `analysis/firm_level_analysis_susb_normalized.md`.

## Guardrails

SUSB has a definitional quirk worth being careful about: "firm" in SUSB means a single legal entity, but multi-state firms are counted in each state where they have establishments. This means national chains can appear in multiple states' firm counts. For the project's purposes (small-business mandate response), this is unlikely to matter much because mandate-affected firms are overwhelmingly single-state, but document the issue.

SUSB also excludes some sectors (most agriculture, postal service, private households, government). These are also excluded from Form 5500 in practice for the project's mandate population, so the comparison is approximately apples-to-apples, but document the residual scope difference.

## What this does NOT do

- Does not pull SUSB by industry/NAICS (separate ask if useful)
- Does not pull SUSB-equivalent data for other countries (project is US-only)
- Does not replace CBP — adds SUSB alongside

## Definition of done

This task is done when:
1. SUSB panel is built and committed
2. DiD has been re-run on SUSB-denominator panels (both v1 and v2)
3. Comparison writeup exists explaining the difference vs. CBP-based headline
4. Firm-level analysis has SUSB-normalized rates by size band
5. The headline ATT figure that goes into the eventual final report is confirmed (either still 2.37 per 1,000 establishments with CBP, or a new SUSB-based figure with the difference clearly explained)
