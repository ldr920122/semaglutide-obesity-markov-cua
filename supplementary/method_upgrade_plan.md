# Method Upgrade Plan

Date: 2026-06-30

Target manuscript: semaglutide adult obesity public-payer Markov cost-utility analysis.

## Gate Decision

Method thickness before this update: acceptable but exposed.

Main concern: recent obesity pharmacoeconomic papers increasingly use richer Core Obesity Model, individual-patient simulation, cardiovascular, OSA, CKD, HbA1c and discontinuation structures. The current manuscript is deliberately a single-complication diabetes model. If submitted without additional method defense, reviewers could reasonably say the work is transparent but too thin.

Method thickness after this update: strengthened and defensible for Frontiers in Public Health / Health Economics as a transparent reference-model article, not as a definitive reimbursement HTA.

## Actions Implemented

1. Added unmodeled-benefit threshold analysis.
   - Purpose: quantify how much additional non-diabetes QALY gain would be required for omitted cardiovascular, OSA, musculoskeletal or hepatic benefits to change the value conclusion.
   - Output: `tables/benefit_price_frontier_grid.csv`, `tables/benefit_price_frontier_summary.csv`, `figures/value_frontier_and_drivers.*`.
   - Interpretation boundary: this is not a CV or OSA model; it is a break-even threshold analysis.

2. Added probabilistic driver analysis.
   - Purpose: complement one-way tornado analysis with PSA-derived rank correlations against net monetary benefit.
   - Output: `tables/psa_driver_correlations.csv`, `figures/psa_driver_correlations_source.csv`.
   - Primary finding: diabetes relative risk, treatment exposure, utility gain, drug cost and diabetes incidence are the dominant NMB drivers.

3. Added EVPI per-patient outputs.
   - Purpose: show whether decision uncertainty has meaningful value across willingness-to-pay thresholds.
   - Output: `tables/evpi.csv`.
   - Use: supplementary robustness output; do not overemphasize in the abstract.

4. Added method-precedent matrix.
   - Purpose: compare current methods with recent hotspot literature and prevent the manuscript from looking unaware of richer obesity economic models.
   - Output: `method_precedent_matrix.csv`, `method_precedent_matrix.md`.

## Actions Not Implemented

1. Did not add full cardiovascular, CKD or OSA health states.
   - Reason: doing so without independent, jurisdiction-specific event rates, costs, utilities and transition equations would create a larger but less credible model.

2. Did not add deep learning, reinforcement learning or prediction modelling.
   - Reason: the research question is a cost-utility analysis, not prediction or sequential decision optimization.

3. Did not turn source mapping into a systematic review.
   - Reason: the manuscript does not follow PRISMA screening and should not claim systematic-review status.

## Remaining Human Gate

The new Literature-to-Method Gate rule is Zotero collection-first. This project currently uses the manuscript bibliography plus PubMed-verified metadata rather than a bound Zotero collection. Before treating the method-precedent matrix as the final citation boundary, the cited precedent papers should be imported into the project Zotero collection and marked as read or checked by the author team.

