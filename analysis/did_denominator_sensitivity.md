# DiD Denominator Sensitivity

Headline ATT for new 401(k) plan formation under three different denominator choices, on both v1-inclusive and v2-conservative mandate-date specifications. The Callaway-Sant'Anna (2021) group-time ATT with not-yet-treated controls is the headline specification in every row. Estimates are rates per 1,000 of the relevant denominator, with 95% wild-bootstrap (state-clustered) confidence intervals from the `differences` package.

## Headline ATT under three denominators

| Denominator | Source | Conceptual unit | ATT v1-inclusive | ATT v2-conservative |
|---|---|---|---|---|
| CBP establishments | Census CBP | Physical location, March snapshot | 2.37 [1.53, 3.20] | 2.37 [1.51, 3.23] |
| QCEW establishments | BLS QCEW | UI-covered worksite, annual average | 1.59 [1.20, 1.98] | 1.62 [1.20, 2.03] |
| SUSB firms (all) | Census SUSB | Legal entity | 2.89 [1.91, 3.86] | 2.90 [1.88, 3.92] |
| SUSB firms 5+ employees | Census SUSB | Legal entity, mandate-eligible | 7.83 [5.12, 10.53] | 7.83 [5.02, 10.64] |

Estimates report point ATT and 95% confidence interval. Units: new 401(k) plan formations per 1,000 of the indicated denominator (CBP/QCEW = establishments; SUSB = firms).

## Drop-California robustness (still CS not-yet-treated)

California is the largest treated state. If the headline result is driven by CA alone, dropping CA should attenuate or flip the ATT. Across all three denominators, drop-CA stays positive and significant.

| Denominator | Drop-CA v1 | Drop-CA v2 |
|---|---|---|
| CBP establishments | 2.12 [1.17, 3.07] | 2.12 [1.17, 3.07] |
| QCEW establishments | 1.51 [1.03, 1.99] | 1.51 [1.03, 1.99] |
| SUSB firms (all) | 2.64 [1.47, 3.81] | 2.64 [1.47, 3.81] |
| SUSB firms 5+ employees | 6.70 [4.09, 9.32] | 6.70 [4.09, 9.32] |

## Interpretation

**The headline finding is robust to denominator choice.** Across CBP-establishments, QCEW-establishments, and SUSB-firms (both all-firms and 5+-employees subsets), the CS not-yet-treated ATT is positive, statistically significant at the 5% level, and survives the drop-CA robustness check. The qualitative conclusion that state auto-IRA mandates cause an increase in new 401(k) plan formations does not depend on which denominator is used.

**Magnitude scales predictably with denominator size.** Per-firm rates are higher than per-establishment rates because firms are a smaller denominator (a multi-establishment firm is one firm but several establishments). Within establishment denominators, the QCEW-based ATT is smaller than the CBP-based ATT because QCEW counts more establishments (UI-covered worksites are typically more granular than the Census Business Register's establishment definition for multi-unit firms).

For v2-conservative: CBP ATT = 2.37, QCEW ATT = 1.62, ratio QCEW/CBP = **0.681**. This is in the same neighborhood as the median CBP/QCEW establishment ratio (0.79), as expected if the denominator difference is purely a level scaling.

**The mandate-eligible 5+ employee firm subset gives the largest ATT magnitude.** This is mechanically expected: solo-prop firms are non-treatable for state auto-IRA mandates, so excluding them concentrates the treatment effect on the relevant population. The 5+ ATT of ~7.8 per 1,000 firms means roughly 0.78 percentage points of mandate-eligible firms newly form a 401(k) plan in response to the mandate.

## Specification details

- **Estimator:** Callaway and Sant'Anna (2021) group-time ATT, aggregated to a simple summary using the `differences` Python package (version 0.3.0).
- **Control group:** Not-yet-treated. Never-treated robustness in the underlying `did_results_*.csv` files yields qualitatively identical estimates.
- **Inference:** Wild bootstrap with 999 iterations, clustered at the state level. Permutation inference (200 random reassignments of treatment among never-treated states, in `did_robustness_*.csv` files) yields p < 0.005 for every primary spec.
- **Years:** 2017 through 2024.
- **Treated states (10):** CA, CO, CT, DE, IL, MD, ME, NJ, OR, VA. Cohort sizes vary by mandate-date version (v1-inclusive uses earliest credible date; v2-conservative uses default-enrollment date).

