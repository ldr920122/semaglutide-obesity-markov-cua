# Method and Visual Enhancement Changelog

Date: 2026-06-30

## Why This Revision Was Made

The previous version was transparent and internally consistent, but the analysis risked looking methodologically thin compared with recent obesity pharmacoeconomic papers using richer complication structures, Core Obesity Model variants, individual-patient simulation, cardiovascular outcomes, obstructive sleep apnea, chronic kidney disease, and patient-level risk-factor pathways.

The revision strengthens the manuscript without inventing unsupported cardiovascular or OSA transition states.

## What Changed

1. Added unmodeled-benefit threshold analysis.
   - New outputs: `tables/benefit_price_frontier_grid.csv`, `tables/benefit_price_frontier_summary.csv`.
   - Main result: at the current price anchor, omitted non-diabetes benefits would need to add 338.1% of the modeled QALY gain to reach CAD$50,000/QALY and 46.0% to reach CAD$150,000/QALY.

2. Added PSA-based driver correlations.
   - New output: `tables/psa_driver_correlations.csv`.
   - Main result: NMB at CAD$150,000/QALY is most strongly associated with diabetes relative risk, treatment exposure, utility gain, drug cost, and baseline diabetes incidence.

3. Added EVPI outputs.
   - New output: `tables/evpi.csv`.
   - Main result: per-patient EVPI is CAD$0 at CAD$50,000/QALY and CAD$160 at CAD$150,000/QALY.

4. Added a new publication-grade figure.
   - New figure: `figures/value_frontier_and_drivers.pdf/svg/tiff`.
   - Figure source files: `figures/value_frontier_source.csv`, `figures/psa_driver_correlations_source.csv`.
   - TIFF exports were regenerated with LZW compression at 600 dpi.

5. Added method-precedent artifacts.
   - New files: `method_precedent_matrix.csv`, `method_precedent_matrix.md`, `method_upgrade_plan.md`, `literature_to_method_gate.md`.
   - These compare the current model with recent obesity economic evaluations and document why a threshold analysis was added instead of unsupported new disease states.

6. Updated manuscript text.
   - Abstract, Methods, Results, Discussion, Conclusion, and Data Availability now reflect the enhanced analyses.
   - New references were added for SELECT/CVD and patient-level obesity economic models.

## Impact on Conclusions

The base-case conclusion did not change. Semaglutide remains not cost-effective at CAD$50,000/QALY or CAD$150,000/QALY under the public-price single-complication reference model.

The revision improves interpretability and reviewer defensibility by showing how much additional non-diabetes benefit would be required to change the threshold conclusion.

## Boundary

The new benefit-price frontier is a threshold analysis, not a cardiovascular, OSA, CKD, hepatic, or musculoskeletal disease model. The manuscript should continue to avoid claiming to be a full reimbursement HTA or a systematic review.

