# Markov Model Run Report

- Run date: 2026-06-30
- Revision scope: Frontiers in Public Health / Health Economics targeted submission update.
- Random seed: 270627
- PSA draws: 5,000
- Main analysis: Canadian public payer perspective, 2022 CAD, 40-year lifetime approximation, annual cycles, half-cycle correction, 1.5% annual discounting.
- CADTH is used as a public benchmark, not as an independent external validation test.

## Base-Case Results

- Incremental cost: CAD$9,915
- Incremental QALYs: 0.0453
- Incremental life-years: 0.0167
- ICER: CAD$219,066/QALY
- NMB at CAD$50,000/QALY: CAD$-7,652
- NMB at CAD$150,000/QALY: CAD$-3,126

## External CADTH Reference

- CADTH incremental cost: CAD$9,385
- CADTH incremental QALYs: 0.046
- CADTH ICER: CAD$204,928/QALY
- CADTH price reduction at CAD$50,000/QALY: 71%

## Price-Threshold Scenario Analysis

- Required price reduction at CAD$50,000/QALY: 76.6% (annual drug cost CAD$1,104)
- Required price reduction at CAD$150,000/QALY: 31.3% (annual drug cost CAD$3,247)

## Unmodeled-Benefit Threshold Analysis

- At CAD$50,000/QALY and current price, total incremental QALYs would need to be 0.1983; this implies 0.1530 additional QALYs (338.1% of the modeled gain).
- At CAD$150,000/QALY and current price, total incremental QALYs would need to be 0.0661; this implies 0.0208 additional QALYs (46.0% of the modeled gain).

## Effect-Retention Structural Sensitivity

- Base retained-effect schedule: incremental QALYs 0.0453; ICER CAD$219,066/QALY
- Immediate loss after stopping: incremental QALYs 0.0414; ICER CAD$240,470/QALY
- Two-year residual after stopping: incremental QALYs 0.0491; ICER CAD$201,366/QALY

## Top One-Way Sensitivity Drivers

- diabetes_rr_semaglutide: ICER range CAD$147,892 to CAD$378,401/QALY
- utility_gain_per_pct_weight_loss: ICER range CAD$281,463 to CAD$151,773/QALY
- treatment_duration_years: ICER range CAD$189,122 to CAD$283,173/QALY
- annual_diabetes_incidence: ICER range CAD$279,788 to CAD$188,064/QALY
- treatment_exposure_factor: ICER range CAD$166,981 to CAD$274,214/QALY

## PSA Driver Correlations

- Diabetes RR: Spearman rho with NMB at CAD$150,000/QALY = -0.65
- Treatment exposure: Spearman rho with NMB at CAD$150,000/QALY = -0.36
- Utility gain per weight loss: Spearman rho with NMB at CAD$150,000/QALY = 0.33
- Annual drug cost: Spearman rho with NMB at CAD$150,000/QALY = -0.26
- Annual diabetes incidence: Spearman rho with NMB at CAD$150,000/QALY = 0.24

## Interpretation Boundary

This run is a reproducible public-source single-complication Markov reference model. Parameter provenance is classified as source-traced, source-derived, source-informed, official life-table-derived, benchmark-aligned scenario, or guideline/structural assumption in tables/markov_model_parameters.csv and the supplementary parameter-source map.
