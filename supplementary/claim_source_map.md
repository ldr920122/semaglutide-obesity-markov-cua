# Claim-Source Map

Date: 2026-06-27

This map links the manuscript's core claims to public sources or model outputs. It is designed as a reviewer-facing traceability aid, not as a systematic-review screening log.

| Claim area | Manuscript location | Evidence/source | Status |
|---|---|---|---|
| STEP 1 semaglutide and placebo weight-loss inputs | Results, source-traced clinical inputs | Wilding et al., NEJM 2021, PubMed PMID 33567185 | Public clinical source checked |
| STEP 4 maintenance/regain inputs | Results, source-traced clinical inputs | Rubino et al., JAMA 2021, PubMed PMID 33755728 | Public clinical source checked |
| Canadian public-payer drug-cost anchor and CADTH benchmark ICER | Methods; Results, CADTH public benchmark | CADTH pharmacoeconomic review on NCBI Bookshelf, NBK601689 | Public HTA source checked |
| Discount rate | Methods, study design | CADTH/CDA-AMC economic-evaluation guideline, 4th edition | Guideline source checked |
| Baseline mortality and mortality growth | Methods, parameter extraction | Statistics Canada Table 13-10-0114-01, 2022/2024 qx | Official table extracted |
| Diabetes incidence/cost inputs | Methods, parameter extraction; Supplementary Table S1 | Bilandzic and Rosella 2017; Rosella et al. 2016 | Canadian source-informed scenario |
| Utility mapping and baseline utility | Methods, population; Supplementary Table S1 | Breeze et al. 2022; Kral et al. 2024; CADTH | Source-informed and benchmark-aligned scenario |
| Diabetes disutility | Methods, parameter extraction; Supplementary Table S1 | Lung et al. 2011; Wang et al. 2024 systematic review | Source-informed scenario |
| Diabetes excess mortality | Methods, parameter extraction; Supplementary Table S1 | Emerging Risk Factors Collaboration 2023; Wang et al. 2024 | Source-informed scenario |
| Base-case cost, QALY, ICER, NMB | Results, base-case table | `analysis/run_markov_psa.py`; `tables/base_case_results.csv` | Reproducible model output |
| PSA intervals and CEAC probabilities | Results, PSA table/figures | `tables/psa_draws.csv`; `tables/psa_summary.csv`; `tables/ceac.csv` | Reproducible model output |
| DSA drivers | Results, deterministic sensitivity analysis | `tables/dsa_tornado.csv`; `figures/tornado_icer_source.csv` | Reproducible model output |
| Price-threshold analysis | Results, price-threshold scenario analysis | `tables/price_threshold_scenarios.csv`; `tables/price_threshold_summary.csv`; `figures/price_threshold_curve_source.csv` | Reproducible model output |
| CADTH benchmark comparison | Results, CADTH public benchmark table | `tables/cadth_external_reference_comparison.csv`; CADTH NBK601689 | Model output plus public benchmark source; not independent external validation |

## Boundary Statement

The manuscript should not be described as a systematic review. The evidence search is a public-source mapping and parameter-provenance exercise. Embase, Web of Science, Scopus, and Cochrane/CENTRAL are not represented as fully screened databases.
