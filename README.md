# Semaglutide Obesity Markov Cost-Utility Model

This repository contains the reproducibility package for the manuscript:

**Semaglutide for adult obesity management: a transparent public-source single-complication Markov cost-utility reference model**

## Authors

- Yiming Xie, Department of Finance, Taizhou People's Hospital Affiliated to Nanjing Medical University, Taizhou, Jiangsu, China
- Dongrui Liu, Department of Pharmacy, Taizhou People's Hospital Affiliated to Nanjing Medical University, Taizhou, Jiangsu, China

Corresponding author: Dongrui Liu.

ORCID IDs are not provided in this repository.

## Contents

- `analysis/run_markov_psa.py`: executable cohort Markov model, deterministic sensitivity analysis, PSA, price-threshold analysis, and retained-effect structural sensitivity.
- `scripts/make_pharmacoeconomic_figures.py`: reproducible figure-generation workflow.
- `tables/`: model parameters, base-case results, PSA outputs, CEAC data, tornado sensitivity results, price-threshold outputs, retained-effect sensitivity, and CADTH benchmark comparison.
- `figures/`: source CSV files for manuscript figures.
- `supplementary/`: parameter-source map, CHEERS checklist, citation audit, data-quality review, model run report, and reference library.

## Reproduce the Model

```bash
python3 -m pip install -r requirements.txt
python3 analysis/run_markov_psa.py
python3 scripts/make_pharmacoeconomic_figures.py
```

The model uses a fixed random seed (`270627`) and 5,000 probabilistic sensitivity-analysis draws.

## Main Model Outputs

- Base-case incremental cost: CAD 9,915
- Base-case incremental QALYs: 0.0453
- Base-case ICER: CAD 219,066/QALY
- Immediate post-treatment effect loss ICER: CAD 240,470/QALY
- Two-year residual effect ICER: CAD 201,366/QALY
- Required annual drug-price reduction at CAD 50,000/QALY: 76.6%
- Required annual drug-price reduction at CAD 150,000/QALY: 31.3%

## Data Scope

This package uses publicly available aggregate literature, public HTA documents, official life-table inputs, public fee schedules, and source-informed model assumptions. It contains no patient-level hospital data.

## Citation

Please cite the related manuscript if using this code or the generated model outputs.
