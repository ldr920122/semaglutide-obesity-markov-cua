# Citation and Parameter-Source Audit

Date: 2026-06-28

## Bottom Line

The final manuscript citation structure has been cleaned and rechecked. The manuscript now has 23 unique in-text citation keys and `references.bib` contains exactly the same 23 keys. There are no undefined citations, no duplicate reference keys, and no orphan bibliography entries. The previously uncited parameter-provenance sources in Supplementary Table S1 are now cited in the Methods. Dense citation clusters were revised so that each major evidence statement is supported by a targeted citation group rather than by a long undifferentiated reference string.

## Citation Structure Check

| Check | Result |
|---|---:|
| Unique in-text citation keys | 23 |
| BibTeX entries retained | 23 |
| Undefined citations | 0 |
| Orphan BibTeX entries | 0 |
| Duplicate BibTeX keys | 0 |
| Citation groups with 4 or more keys | 0 |

## PubMed / PMC Authenticity Check

NCBI E-utilities checks were run on 2026-06-28 for the high-PMID 2026 citations and parameter-provenance biomedical sources. The five 2026 papers cited in the manuscript all resolve in PubMed with matching title, journal, publication date, and DOI.

| Citation key | PMID / ID | Verification result |
|---|---|---|
| `Jenniskens2026pmid42296505` | PMID 42296505 | PubMed resolves: *Annals of Internal Medicine*, 2026 Jun 16, DOI `10.7326/ANNALS-24-03766` |
| `Alts2026pmid42250076` | PMID 42250076 | PubMed resolves: *Advances in Therapy*, 2026 Jun 6, DOI `10.1007/s12325-026-03644-x` |
| `ZavaletaMonestel2026pmid42160088` | PMID 42160088 | PubMed resolves: *JAMA Cardiology*, 2026 May 20, DOI `10.1001/jamacardio.2026.1360` |
| `Hennessy2026pmid42160096` | PMID 42160096 | PubMed resolves: *JAMA Cardiology*, 2026 May 20, DOI `10.1001/jamacardio.2026.0710` |
| `Annemans2026pmid42021523` | PMID 42021523 | PubMed resolves: *Journal of Medical Economics*, 2026 Dec issue metadata, DOI `10.1080/13696998.2026.2646079` |
| `EmergingRiskFactors2023pmid37708900` | PMID 37708900 | PubMed resolves: *The Lancet Diabetes & Endocrinology*, 2023 Oct, DOI `10.1016/S2213-8587(23)00223-1` |
| `DiabetesUtilityReview2024pmc11380328` | PMID 39244536 / PMCID PMC11380328 | PubMed and PMC resolve; PMID added to `references.bib` |
| `Wang2024pmc10935790` | PMCID PMC10935790 | PMC resolves; PMCID retained in `references.bib` |

## Bibliography Cleanup

The following 18 previously orphaned entries were removed from `references.bib` because they were not cited in the manuscript and were not needed for Supplementary Table S1 provenance after the Methods citation fix:

`Abbasi2026pmid42180536`, `Abdeen2026pmid42348222`, `Abegaz2026pmid42012431`, `Awadalla2026pmid42013575`, `Chen2026pmid42268869`, `ClinicalTrialsSemaglutideObesity2026`, `Doan2026pmid42233337`, `Durand2026pmid42289317`, `Estler2026pmid42155673`, `Estler2026pmid42228345`, `Johansson2026pmid42012820`, `Leah2026pmid42340212`, `Li2026pmid42339050`, `Mathew2026pmid42143746`, `NovoCareWegovyPrice2026`, `NovoNordiskPriceReduction2027`, `Ramachandran2026pmid42166309`, and `Torre2026pmid42099530`.

## Core Cited Source Groups

| Source group | Citation keys | Manuscript use | Audit status |
|---|---|---|---|
| Semaglutide trial inputs | `Wilding2021pmid33567185`; `Rubino2021pmid33755728` | STEP 1 and STEP 4 weight-loss inputs | PubMed source present |
| HTA / public benchmark | `CADTHSemaglutideObesity2022`; `CADTHGuidelines2017` | Drug cost, CADTH benchmark ICER, price-reduction reference, discount rate | Public CADTH/NCBI source present |
| Utility mapping | `Breeze2022pmid35796997`; `Kral2024pmc11480186` | Baseline utility and conservative weight-loss utility mapping | PubMed/PMC metadata present |
| Diabetes incidence and cost | `Bilandzic2017DiabetesCanada`; `CANRISKPublicHealthCanada`; `Rosella2016pmid26201986` | Diabetes incidence and annual cost scenario | Public Canadian / PubMed source present |
| Diabetes utility | `Lung2011pmid21472392`; `DiabetesUtilityReview2024pmc11380328` | Diabetes disutility scenario | PubMed/PMC metadata present |
| Mortality | `StatisticsCanadaLifeTable2022to2024`; `EmergingRiskFactors2023pmid37708900`; `Wang2024pmc10935790` | Background mortality, mortality growth, diabetes mortality multiplier | Official table / PubMed-PMC source present |
| Monitoring cost | `OntarioScheduleBenefits2025` | Monitoring-cost scenario | Public fee-schedule source present |
| Reporting standard | `Husereau2022CHEERS` | CHEERS 2022 reporting alignment | PubMed citation present |

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

## Remaining Portal Items

Citation and parameter-source integrity issues are resolved. Remaining live-portal items are the corresponding-author email, APC/waiver choice, article type/editor selections, and ORCID registration/linking if the Frontiers portal requires it.
