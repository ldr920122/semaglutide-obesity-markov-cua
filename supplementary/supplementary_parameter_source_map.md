# Supplementary Table S1. Parameter Source and Provenance Map

Date: 2026-06-27

This table is intended to make model input provenance auditable. Parameters are classified as direct public-source extraction, official table derivation, source-informed scenario, benchmark-aligned scenario, or guideline/structural assumption. Benchmark-aligned parameters are explicitly labeled and should not be presented as independently validated or directly observed trial inputs.

| Parameter | Base | Range | Provenance class | Primary sources | Derivation and justification |
|---|---:|---:|---|---|---|
| Starting age | 50 years | 45-55 | Source-informed structural assumption | STEP 1, STEP 4, CADTH | Rounded representative adult obesity-treatment starting age; also aligns the model's starting mortality with Statistics Canada age-50 qx. |
| Baseline obesity utility | 0.78 | 0.72-0.84 | Source-informed scenario | Breeze 2022; Kral 2024; CADTH | Breeze et al. report mean baseline EQ-5D-3L near 0.788 in a BMI>28 weight-loss cohort. Range captures obesity/comorbidity uncertainty. |
| Semaglutide weight loss | 14.9% | 11.9-17.9 | Source-traced | STEP 1 / Wilding 2021 | STEP 1 reported mean body-weight change at week 68 of -14.9% with semaglutide. |
| Comparator weight loss | 2.4% | 1.0-4.0 | Source-traced | STEP 1 / Wilding 2021 | STEP 1 reported mean body-weight change at week 68 of -2.4% with placebo. |
| Utility gain per percentage-point weight-loss difference | 0.00065 | 0.00035-0.00125 | Benchmark-aligned scenario | Breeze 2022; Kral 2024; CADTH | Literature supports a positive BMI/EQ-5D association, but the model uses a conservative attenuated coefficient as a benchmark-aligned scenario. This is not a STEP trial-measured utility endpoint and is not used as independent validation against CADTH. |
| Annual drug cost | CAD 4,726.41 | 4,253.77-5,199.05 | Source-traced public reference | CADTH | CADTH pharmacoeconomic review reports public Canadian semaglutide annual drug-cost anchor. |
| Treatment exposure factor | 0.72 | 0.55-0.90 | Benchmark-aligned cost scenario | STEP trials; CADTH | Scenario captures titration, persistence, and discontinuation. It is benchmark-aligned to the public CADTH cost anchor and tested widely in DSA/PSA. |
| Monitoring cost | CAD 120/year | 50-250 | Fee-schedule scenario | Ontario Schedule of Benefits; CADTH | Conservative annual public-payer monitoring increment approximating one to two physician/laboratory follow-up contacts. |
| Annual diabetes incidence | 0.025 | 0.0125-0.0400 | Source-derived scenario | Bilandzic 2017; PHAC/CANRISK | Annualized from a high-risk Canadian diabetes-risk threshold of approximately 22.6% over 10 years: 1 - (1 - 0.226)^(1/10) = 0.0253. |
| Diabetes relative risk with semaglutide | 0.78 | 0.60-0.95 | Benchmark-aligned scenario | STEP 1; Bilandzic 2017; CADTH | Represents weight-loss-mediated diabetes delay during the retained-effect schedule. This is a benchmark-aligned scenario parameter, not a claim of trial-observed diabetes prevention. |
| Annual diabetes cost increment | CAD 1,800/year | 900-3,200 | Source-informed scenario | Bilandzic 2017; Rosella 2016; CADTH | Triangulated from Canadian attributable diabetes-cost evidence and converted into a conservative annual complication-cost increment. |
| Diabetes utility decrement | 0.045 | 0.020-0.080 | Source-informed scenario | Lung 2011; Wang 2024 utility review | Conservative incremental disutility superimposed on baseline obesity utility; range covers published diabetes utility uncertainty. |
| Background mortality at age 50 | 0.00264 | 0.00187-0.00389 | Official life-table-derived | Statistics Canada Table 13-10-0114-01 | Canada, both sexes, 2022/2024 qx at age 50. Low/high use qx at ages 45 and 55. |
| Annual log mortality growth | 0.08575 | 0.070-0.100 | Official life-table-derived | Statistics Canada Table 13-10-0114-01 | Fitted from Statistics Canada qx at age 50 and age 70: log(qx70/qx50)/20 = 0.08575. |
| Diabetes mortality relative risk | 1.50 | 1.20-1.90 | Source-informed scenario | Emerging Risk Factors Collaboration 2023; Wang 2024 mortality study | Conservative mortality multiplier for the diabetes state, consistent with elevated all-cause mortality after type 2 diabetes diagnosis. |
| Treatment duration | 3 years | 2-5 | Public-reference structural assumption | CADTH | Aligns base-case drug-cost accrual with CADTH reference structure; varied in sensitivity analysis. |
| Retained-effect multiplier | Base years 1-4: 1.00, 0.85, 0.65, 0.25; thereafter 0 | 0-1 | Structural scenario informed by STEP 4 | STEP 4 / Rubino 2021 | Treatment costs accrue during years 1-3. Base case allows one residual post-treatment year. Structural sensitivity scenarios test immediate post-treatment loss and two-year residual effect. Exported as `tables/effect_retention_schedule.csv` and `tables/effect_retention_sensitivity.csv`. |
| Time horizon | 40 years | 20-50 | Guideline-aligned structural assumption | CADTH guideline; CADTH review | Lifetime approximation for an adult cohort starting at age 50. |
| Discount rate | 1.5% | 0-3% | Guideline-aligned | CADTH/CDA-AMC guideline | Canadian economic-evaluation guideline-recommended discounting for costs and outcomes. |

## Submission Note

No parameter remains labeled as `needs_source_verification` in the executable model or generated parameter CSV after this revision. Parameters that are not directly extracted are deliberately labeled as source-informed or benchmark-aligned scenarios and are varied in sensitivity analysis. The CADTH comparison is a public benchmark, not an independent external validation test.
