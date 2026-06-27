# Data Quality Review

Date: 2026-06-28

Revision scope: Frontiers in Public Health / Health Economics targeted submission update.

## Bottom Line

The package has been upgraded from a working draft to a source-provenance-audited pharmacoeconomic Markov model package. The strongest data anchors are STEP 1, STEP 4, CADTH, Statistics Canada life tables, and the executable model outputs. Parameters that cannot be directly extracted from a single public source are now explicitly labeled as source-informed or benchmark-aligned scenarios and are varied in sensitivity analysis.

## Data Elements Checked

| Data element | Current status | Interpretation |
|---|---|---|
| STEP 1 clinical effect | Source-traced to PubMed-indexed trial report | Suitable as clinical treatment-effect input |
| STEP 4 maintenance/regain contrast | Source-traced to PubMed-indexed trial report | Suitable as maintenance/discontinuation context |
| CADTH incremental cost, QALY, ICER | Source-traced to CADTH pharmacoeconomic review on NCBI Bookshelf | Suitable as public benchmark, not independent external validation |
| CADTH scenario ICERs and price-reduction statement | Source-traced to CADTH pharmacoeconomic review | Suitable as public benchmark context |
| Drug acquisition cost | Source-traced to CADTH public pharmacoeconomic review | Suitable as Canadian public-payer anchor |
| Background mortality | Official Statistics Canada life-table extraction | Suitable; no placeholder remains |
| Utility mapping | Source-informed and benchmark-aligned | Suitable if framed as conservative scenario mapping, not direct trial utility measurement |
| Diabetes incidence/cost | Source-informed Canadian public-health/economic inputs | Suitable with scenario framing and sensitivity analysis |
| Monitoring cost | Public fee-schedule scenario | Suitable as scenario parameter |
| PSA / CEAC | Generated from 5,000 draws | Suitable and included in tables/figures |
| Tornado DSA | Generated from prespecified ranges | Suitable and included |
| Price-threshold analysis | Generated from model price scenarios and exact threshold solving | Suitable and included in tables/figures |
| Retained-effect structural sensitivity | Generated from executed Markov model under base, immediate-loss, and two-year residual scenarios | Suitable and included in manuscript table and supplementary CSV |

## Fixes Completed in This Revision

1. Replaced placeholder mortality with Statistics Canada 2022/2024 qx values.
2. Updated model source fields so regenerated `tables/markov_model_parameters.csv` has no `needs_source_verification` statuses.
3. Added public sources for utility, diabetes risk, diabetes costs, diabetes disutility, mortality, and monitoring costs.
4. Re-ran the Markov model after parameter-source revision.
5. Regenerated pharmacoeconomic figures from updated tables.
6. Updated manuscript results to the new model run: ICER CAD 219,066/QALY, incremental QALYs 0.0453, incremental cost CAD 9,915.
7. Added supplementary parameter-source map, CHEERS checklist, and claim-source map.
8. Removed PubMed topic-hotness language from the scientific manuscript.
9. Reframed CADTH as a public benchmark rather than an independent validation test.
10. Added price-threshold scenario analysis and a price-threshold curve.
11. Added Frontiers-targeted retained-effect structural sensitivity scenarios:
    base schedule, immediate loss after treatment stopping, and two-year residual effect.
12. Added a Frontiers submission-readiness checklist and clarified repository, author, ORCID, funding, COI, and author-contribution fields as journal-portal compliance items.

## Frontiers-Targeted Data Checks

| Check | Result |
|---|---|
| Base retained-effect ICER | CAD$219,066/QALY |
| Immediate loss after stopping ICER | CAD$240,470/QALY |
| Two-year residual effect ICER | CAD$201,366/QALY |
| CHEERS 2022 checklist | Present as `supplementary_cheers_2022_checklist.md` |
| Frontiers upload checklist | Present as `frontiers_public_health_submission_checklist.md` |
| Repository URL | Must be inserted by authors after OSF/GitHub/Zenodo/Figshare/institutional deposit; no fabricated URL is used |

## Remaining Submission Risks

- The model remains deliberately parsimonious and does not include cardiovascular events, obstructive sleep apnea, adverse events, or full BMI trajectory microsimulation.
- Some inputs are source-informed or benchmark-aligned rather than directly extracted. This is now disclosed and tested, but it should remain visible in Methods and Limitations.
- The search should still be described as public-source mapping, not a systematic review.
- Author names, affiliations, ORCID IDs, author contributions, funding, conflicts of interest, acknowledgments, APC/waiver choice, repository URL, and journal-portal declarations are real author-responsibility fields, not public model parameters.
