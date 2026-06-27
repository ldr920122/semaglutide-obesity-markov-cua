# Citation and Parameter-Source Audit

Date: 2026-06-27

## Bottom Line

The manuscript's core clinical, economic, utility, mortality, and model-output claims now have traceable sources or reproducible model-output files. No model parameter remains labeled as `needs_source_verification` in `tables/markov_model_parameters.csv`.

## Core Cited Source Groups

| Source group | Citation keys | Manuscript use | Audit status |
|---|---|---|---|
| Semaglutide trial inputs | `Wilding2021pmid33567185`; `Rubino2021pmid33755728` | STEP 1 and STEP 4 weight-loss inputs | Public PubMed source checked |
| HTA / public benchmark | `CADTHSemaglutideObesity2022`; `CADTHGuidelines2017` | Drug cost, CADTH benchmark ICER, price-reduction reference, discount rate | Public CADTH/NCBI source checked |
| Utility mapping | `Breeze2022pmid35796997`; `Kral2024pmc11480186` | Baseline utility and conservative weight-loss utility mapping | Public PubMed/PMC/Crossref metadata checked |
| Diabetes incidence and cost | `Bilandzic2017DiabetesCanada`; `Rosella2016pmid26201986`; `CANRISKPublicHealthCanada` | Diabetes incidence and annual cost scenario | Public Canadian source checked |
| Diabetes utility | `Lung2011pmid21472392`; `DiabetesUtilityReview2024pmc11380328` | Diabetes disutility scenario | Public PubMed/PMC metadata checked |
| Mortality | `StatisticsCanadaLifeTable2022to2024`; `EmergingRiskFactors2023pmid37708900`; `Wang2024pmc10935790` | Background mortality, mortality growth, diabetes mortality multiplier | Official table / public PubMed-PMC source checked |
| Monitoring cost | `OntarioScheduleBenefits2025` | Monitoring-cost scenario | Public fee-schedule source checked |
| Reporting standard | `Husereau2022CHEERS` | CHEERS 2022 reporting alignment | PubMed citation present |

## In-Text to Reference Consistency

- All newly added citation keys used in the manuscript are present in `references.bib`.
- The model parameter CSV uses the same citation keys as the revised reference list.
- The manuscript no longer claims PRISMA-level systematic review coverage.
- The manuscript distinguishes direct source extraction from source-informed and benchmark-aligned scenario parameters.

## Model Output Consistency

| Output | Manuscript value | Source file | Audit status |
|---|---:|---|---|
| Incremental cost | CAD 9,915 | `tables/base_case_results.csv` | Match |
| Incremental QALYs | 0.0453 | `tables/base_case_results.csv` | Match |
| ICER | CAD 219,066/QALY | `tables/base_case_results.csv` | Match |
| NMB at CAD 50,000/QALY | CAD -7,652 | `tables/base_case_results.csv` | Match |
| NMB at CAD 150,000/QALY | CAD -3,126 | `tables/base_case_results.csv` | Match |
| Probability cost-effective at CAD 50,000/QALY | 0.0% | `tables/psa_summary.csv` | Match |
| Probability cost-effective at CAD 150,000/QALY | 11.0% | `tables/psa_summary.csv` | Match |
| Immediate post-treatment loss ICER | CAD 240,470/QALY | `tables/effect_retention_sensitivity.csv` | Match |
| Two-year residual effect ICER | CAD 201,366/QALY | `tables/effect_retention_sensitivity.csv` | Match |
| Required price reduction at CAD 50,000/QALY | 76.6% | `tables/price_threshold_summary.csv` | Match |
| Required price reduction at CAD 150,000/QALY | 31.3% | `tables/price_threshold_summary.csv` | Match |

## Remaining Non-Data Items

The following are not public-data parameters and must be supplied by the real author team before portal submission:

- author names and affiliations
- author contributions
- funding statement
- conflicts of interest
- acknowledgments
- final target-journal article type and portal-specific declarations
