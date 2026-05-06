# Data Collection Spec: State-Administrative Records

**Project:** State Auto-IRA Research
**Workstream:** Externally-validated firm-side cross-check
**Purpose:** Pull state-program-administered statistics that bear on private-plan formation. Specifically, exemption-filing counts (which represent firms that *chose private plans instead of the state program*) and any state-published firm-size or industry breakdowns.
**Output target:** `data/state_admin/` and `methodology/state_admin_collection_log.md`

---

## What this collects and why

State auto-IRA programs maintain administrative data that bears directly on the project's research question. When an employer files an exemption, they are by definition choosing a private plan (typically a 401(k)) over the state program. Exemption-filing counts are therefore a state-side firm count of the same population the v3 Form 5500 dataset captures from the federal side.

This spec collects publicly available state-published data only. No CPRA/FOIA/records requests. Anything requiring a request goes in a separate workstream.

The goal is twofold: (1) external validation of v3 firm counts state-by-state, and (2) any firm-size, industry, or temporal breakdowns the state programs publish that would let us cross-check the descriptive analysis.

## Scope

Pull the most recent publicly available administrative data for each of the 10 mandate states in the v3 dataset:

CA (CalSavers), OR (OregonSaves), IL (Secure Choice), CT (MyCTSavings), MD (MarylandSaves), CO (SecureSavings), VA (RetirePath), ME (MERIT), DE (DEEARNS), NJ (RetireReady NJ).

For each state, the priority order of data to look for is:

1. **Exemption-filing counts.** Total exemptions filed cumulatively, exemptions filed per year, exemptions by employer-size band if published. This is the single most important number.
2. **Registration counts and program participation.** Total employers registered with the state program, savers/participants, assets under management. Useful as denominator context.
3. **Firm-size or industry breakdowns** of either registrations or exemptions, if published.
4. **Annual reports** from the state board overseeing the program. Often contain year-over-year program statistics not surfaced on dashboards.
5. **Board meeting materials** (agendas, presentations, financial reports) — often contain operational statistics not republished in marketing materials.

## Sources to check per state

For each state, check in this order:

1. **Official program website** (e.g., calsavers.com, oregonsaves.com) — look for "About," "Statistics," "Reports," "For Press" pages
2. **Sponsoring agency website** (CA State Treasurer for CalSavers, OR State Treasury for OregonSaves, IL State Treasurer for Secure Choice, etc.) — annual reports and press releases
3. **State board minutes/materials** — many program boards post meeting materials with operational statistics
4. **Vestwell** — administers several of these programs (CA, CO, OR, MD, VT). Vestwell publishes occasional aggregate research on state programs that draws on its administrative data.
5. **State auditor / legislative analyst reports** — sometimes the state auditor or legislative analyst office publishes program reviews

## Output structure

Create `data/state_admin/state_admin_summary.csv` with one row per state and columns:

```
state | program_name | data_as_of_date | total_employer_registrations |
total_exemption_filings | exemption_filings_cumulative | total_savers |
total_assets_usd | source_url | source_type | notes
```

For richer state-by-state data (firm-size breakdowns etc.), create per-state files: `data/state_admin/<state>_detail.csv`.

For each state, also append a section to `methodology/state_admin_collection_log.md` documenting:

- What sources were checked
- What was found vs. what wasn't published
- Date of pull
- Any discrepancies between sources

## Comparison to v3 dataset

After collection, build a comparison table at `analysis/state_admin_vs_v3.md`:

```
state | v3_v2_conservative_firms | state_exemption_filings |
ratio | notes
```

The ratio is the project's main contribution from this exercise. If state exemption filings substantially exceed v3 firm counts, that suggests filing lag or scope differences in v3. If they're substantially below, that suggests the state program doesn't capture all firms that established 401(k)s (for example, firms that already had plans pre-mandate and filed exemption later, or firms that established plans but never filed exemption). Either direction is informative.

The expected pattern, based on the Bloomfield-Goodman-Rao-Slavov NBER paper, is that exemption filings should be in the same order of magnitude as v3 firm counts but not identical because (a) some firms had pre-mandate plans, (b) some firms file late, and (c) some firms establish plans without ever filing exemption. Document the ratio honestly even if it complicates the headline.

## Things to flag, not work around

If a state's program does not publish exemption-filing counts at all (some don't), document that fact in the collection log and move on. Don't try to estimate from indirect signals.

If sources conflict (e.g., a press release says X exemptions, the dashboard shows Y), document both, do not average. Surface the conflict to me.

If a state has changed its program name or restructured (e.g., RetirePath VA was previously administered by Virginia529, now Commonwealth Savers), document the transition and source data from the current administering body.

## What this does NOT do

- No CPRA/FOIA requests (separate workstream, on hold)
- No firm-level data (state programs don't publish individual employer lists)
- No DiD re-run with this data (collection only; analysis is a follow-up decision)

## Definition of done

This task is done when there is one CSV row per mandate state with the publicly available admin statistics, a comparison table against v3 counts, and a collection log noting what was and wasn't available per state. Nothing requires guessing or estimation.
