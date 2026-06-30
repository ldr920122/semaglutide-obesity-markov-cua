from __future__ import annotations

import csv
import json
import math
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables"
FIG_DIR = ROOT / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

RNG_SEED = 270627
PSA_DRAWS = 5000
WTP_VALUES = list(range(0, 300001, 10000))


CADTH_EXTERNAL_REFERENCE = {
    "incremental_cost_cad": 9385.0,
    "incremental_qaly": 0.046,
    "icer_cad_per_qaly": 204928.0,
    "required_price_reduction_at_50000": 0.71,
    "source": "CADTH pharmacoeconomic review report for semaglutide (Wegovy), 2022; NCBI Bookshelf NBK601689.",
}


PARAMETERS: Dict[str, Dict[str, object]] = {
    "baseline_age": {
        "category": "population",
        "base": 50.0,
        "low": 45.0,
        "high": 55.0,
        "unit": "years",
        "distribution": "normal",
        "source": "Rubino2021pmid33755728; Wilding2021pmid33567185; CADTHSemaglutideObesity2022",
        "note": "Representative rounded starting age for adults eligible for semaglutide obesity treatment; varied 45-55 years and paired with the age-50 Statistics Canada life-table mortality anchor.",
        "status": "source_informed_structural_assumption",
    },
    "baseline_utility_obesity": {
        "category": "utility",
        "base": 0.78,
        "low": 0.72,
        "high": 0.84,
        "unit": "utility weight",
        "distribution": "beta/normal approximation",
        "source": "Breeze2022pmid35796997; Kral2024pmc11480186; CADTHSemaglutideObesity2022",
        "note": "Baseline EQ-5D utility for adults with BMI in the obesity-treatment range; Breeze et al. report mean baseline EQ-5D-3L 0.788 in a BMI>28 weight-loss cohort, with uncertainty tested from 0.72 to 0.84.",
        "status": "source_informed_scenario",
    },
    "semaglutide_weight_loss_pct": {
        "category": "clinical_effect",
        "base": 14.9,
        "low": 11.9,
        "high": 17.9,
        "unit": "percent body-weight reduction",
        "distribution": "normal",
        "source": "Wilding2021pmid33567185",
        "note": "STEP 1 mean percent weight change at week 68.",
        "status": "source_traced",
    },
    "comparator_weight_loss_pct": {
        "category": "clinical_effect",
        "base": 2.4,
        "low": 1.0,
        "high": 4.0,
        "unit": "percent body-weight reduction",
        "distribution": "normal",
        "source": "Wilding2021pmid33567185",
        "note": "STEP 1 comparator/placebo mean percent weight change at week 68.",
        "status": "source_traced",
    },
    "utility_gain_per_pct_weight_loss": {
        "category": "utility",
        "base": 0.00065,
        "low": 0.00035,
        "high": 0.00125,
        "unit": "utility gain per percent weight-loss difference",
        "distribution": "normal",
        "source": "Breeze2022pmid35796997; Kral2024pmc11480186; CADTHSemaglutideObesity2022",
        "note": "Conservative attenuated utility mapping from the STEP 1 weight-loss contrast; informed by BMI/EQ-5D literature and treated as a benchmark-aligned scenario input, not as a trial-measured utility endpoint.",
        "status": "benchmark_aligned_scenario",
    },
    "annual_drug_cost_cad": {
        "category": "cost",
        "base": 4726.41,
        "low": 4253.77,
        "high": 5199.05,
        "unit": "2022 CAD per year",
        "distribution": "gamma",
        "source": "CADTHSemaglutideObesity2022",
        "note": "CADTH-reported annual drug acquisition cost used as public Canadian payer anchor.",
        "status": "source_traced_public_reference",
    },
    "treatment_exposure_factor": {
        "category": "cost",
        "base": 0.72,
        "low": 0.55,
        "high": 0.90,
        "unit": "proportion of full annual acquisition cost",
        "distribution": "beta/normal approximation",
        "source": "Wilding2021pmid33567185; Rubino2021pmid33755728; CADTHSemaglutideObesity2022",
        "note": "Exposure-adjustment scenario reflecting dose escalation, persistence, and discontinuation; benchmark-aligned to the public CADTH cost anchor and varied widely from 0.55 to 0.90.",
        "status": "benchmark_aligned_cost_scenario",
    },
    "monitoring_cost_cad": {
        "category": "cost",
        "base": 120.0,
        "low": 50.0,
        "high": 250.0,
        "unit": "2022 CAD per treated year",
        "distribution": "gamma",
        "source": "OntarioScheduleBenefits2025; CADTHSemaglutideObesity2022",
        "note": "Conservative public-payer monitoring scenario approximating one to two incremental physician/laboratory follow-up contacts per treated year; tested from CAD 50 to CAD 250.",
        "status": "fee_schedule_scenario",
    },
    "annual_diabetes_incidence": {
        "category": "transition",
        "base": 0.025,
        "low": 0.0125,
        "high": 0.0400,
        "unit": "annual probability",
        "distribution": "lognormal",
        "source": "Bilandzic2017DiabetesCanada; CANRISKPublicHealthCanada",
        "note": "Annualized diabetes-onset probability for a higher-risk obesity/overweight-with-comorbidity cohort; base approximates a 22.6% 10-year high-risk DPoRT/CANRISK threshold.",
        "status": "source_derived_scenario",
    },
    "diabetes_rr_semaglutide": {
        "category": "transition",
        "base": 0.78,
        "low": 0.60,
        "high": 0.95,
        "unit": "relative risk",
        "distribution": "lognormal",
        "source": "Bilandzic2017DiabetesCanada; CADTHSemaglutideObesity2022; Wilding2021pmid33567185",
        "note": "Weight-loss-mediated diabetes-delay scenario applied through the retained-effect schedule; benchmark-aligned rather than independently observed in the STEP trials and stress-tested from 0.60 to 0.95.",
        "status": "benchmark_aligned_scenario",
    },
    "annual_diabetes_cost_cad": {
        "category": "cost",
        "base": 1800.0,
        "low": 900.0,
        "high": 3200.0,
        "unit": "2022 CAD per diabetes year",
        "distribution": "gamma",
        "source": "Bilandzic2017DiabetesCanada; Rosella2016pmid26201986; CADTHSemaglutideObesity2022",
        "note": "Annualized attributable diabetes medical-cost increment, triangulated from Canadian diabetes cost literature and retained as a scenario parameter with wide uncertainty.",
        "status": "source_informed_scenario",
    },
    "diabetes_utility_decrement": {
        "category": "utility",
        "base": 0.045,
        "low": 0.020,
        "high": 0.080,
        "unit": "utility decrement",
        "distribution": "beta/normal approximation",
        "source": "Lung2011pmid21472392; DiabetesUtilityReview2024pmc11380328",
        "note": "Incremental disutility for diabetes superimposed on obesity baseline utility; chosen conservatively within published diabetes utility ranges and varied from 0.020 to 0.080.",
        "status": "source_informed_scenario",
    },
    "background_mortality_age50": {
        "category": "transition",
        "base": 0.00264,
        "low": 0.00187,
        "high": 0.00389,
        "unit": "annual probability",
        "distribution": "fixed/scenario",
        "source": "StatisticsCanadaLifeTable2022to2024",
        "note": "Statistics Canada Table 13-10-0114-01 death probability qx for Canada, both sexes, age 50, 2022/2024; low/high use ages 45 and 55.",
        "status": "official_life_table_derived",
    },
    "mortality_annual_growth": {
        "category": "transition",
        "base": 0.08575,
        "low": 0.070,
        "high": 0.100,
        "unit": "log annual growth",
        "distribution": "fixed/scenario",
        "source": "StatisticsCanadaLifeTable2022to2024",
        "note": "Log-linear annual mortality growth fitted from Statistics Canada age-50 to age-70 qx values; wider 0.070-0.100 range retained for scenario testing.",
        "status": "official_life_table_derived",
    },
    "diabetes_mortality_rr": {
        "category": "transition",
        "base": 1.50,
        "low": 1.20,
        "high": 1.90,
        "unit": "relative risk",
        "distribution": "lognormal",
        "source": "EmergingRiskFactors2023pmid37708900; Wang2024pmc10935790",
        "note": "Conservative excess all-cause mortality multiplier for the diabetes state; source studies report elevated mortality/life-expectancy loss after type 2 diabetes diagnosis.",
        "status": "source_informed_scenario",
    },
    "treatment_duration_years": {
        "category": "model_structure",
        "base": 3.0,
        "low": 2.0,
        "high": 5.0,
        "unit": "years",
        "distribution": "scenario",
        "source": "CADTHSemaglutideObesity2022",
        "note": "Base-case treatment-cost duration aligned with CADTH public pharmacoeconomic review scenario; varied from 2 to 5 years.",
        "status": "public_reference_structural_assumption",
    },
    "horizon_years": {
        "category": "model_structure",
        "base": 40.0,
        "low": 20.0,
        "high": 50.0,
        "unit": "years",
        "distribution": "scenario",
        "source": "CADTHGuidelines2017; CADTHSemaglutideObesity2022",
        "note": "Lifetime approximation for an adult cohort starting at age 50; 20- and 50-year scenarios retained.",
        "status": "guideline_aligned_structural_assumption",
    },
    "discount_rate": {
        "category": "economic",
        "base": 0.015,
        "low": 0.000,
        "high": 0.030,
        "unit": "annual rate",
        "distribution": "scenario",
        "source": "CADTHGuidelines2017",
        "note": "Applied to both costs and QALYs in the base case.",
        "status": "guideline_aligned",
    },
}


def clipped(value: float, low: float, high: float) -> float:
    return float(min(max(value, low), high))


def clipped_normal(rng: np.random.Generator, mean: float, sd: float, low: float, high: float) -> float:
    return clipped(float(rng.normal(mean, sd)), low, high)


def gamma_from_mean_cv(rng: np.random.Generator, mean: float, cv: float, low: float, high: float) -> float:
    shape = 1.0 / (cv * cv)
    scale = mean / shape
    return clipped(float(rng.gamma(shape, scale)), low, high)


def lognormal_from_mean_cv(rng: np.random.Generator, mean: float, cv: float, low: float, high: float) -> float:
    sigma2 = math.log(1.0 + cv * cv)
    mu = math.log(mean) - sigma2 / 2.0
    return clipped(float(rng.lognormal(mu, math.sqrt(sigma2))), low, high)


def beta_from_mean_sd(rng: np.random.Generator, mean: float, sd: float, low: float, high: float) -> float:
    variance = sd * sd
    total = mean * (1.0 - mean) / variance - 1.0
    if total <= 0:
        return clipped_normal(rng, mean, sd, low, high)
    alpha = mean * total
    beta = (1.0 - mean) * total
    return clipped(float(rng.beta(alpha, beta)), low, high)


def base_parameters() -> Dict[str, float]:
    return {key: float(value["base"]) for key, value in PARAMETERS.items()}


EFFECT_RETENTION_SCENARIOS = {
    "base": {
        "label": "Base retained-effect schedule",
        "description": "Treatment years 1-3 use 1.00, 0.85, and 0.65; first post-treatment year uses 0.25; later years return to 0.",
    },
    "immediate_loss_after_stop": {
        "label": "Immediate loss after stopping",
        "description": "Treatment years 1-3 use 1.00, 0.85, and 0.65; post-treatment years return immediately to 0.",
    },
    "two_year_residual_after_stop": {
        "label": "Two-year residual after stopping",
        "description": "Treatment years 1-3 use 1.00, 0.85, and 0.65; two post-treatment years use 0.35 and 0.15; later years return to 0.",
    },
}


def effect_decay(cycle: int, treatment_duration: float, scenario: str = "base") -> float:
    treatment_years = int(round(treatment_duration))
    if cycle < treatment_years:
        decay = [1.0, 0.85, 0.65, 0.50, 0.35]
        return decay[min(cycle, len(decay) - 1)]
    if scenario == "immediate_loss_after_stop":
        return 0.0
    if scenario == "two_year_residual_after_stop":
        if cycle == treatment_years:
            return 0.35
        if cycle == treatment_years + 1:
            return 0.15
        return 0.0
    if cycle == treatment_years:
        return 0.25
    return 0.0


def transition_state(state: np.ndarray, cycle: int, params: Dict[str, float], arm: str) -> np.ndarray:
    no_diabetes, diabetes, dead = state
    bg_mortality = min(
        0.35,
        params["background_mortality_age50"] * math.exp(params["mortality_annual_growth"] * cycle),
    )
    diabetes_mortality = min(0.55, bg_mortality * params["diabetes_mortality_rr"])
    rr_effect = 1.0
    if arm == "semaglutide":
        scenario = str(params.get("_effect_retention_scenario", "base"))
        retained_effect = effect_decay(cycle, params["treatment_duration_years"], scenario)
        rr_effect = 1.0 - (1.0 - params["diabetes_rr_semaglutide"]) * retained_effect
    diabetes_incidence = clipped(params["annual_diabetes_incidence"] * rr_effect, 0.0, 0.30)

    no_deaths = no_diabetes * bg_mortality
    diabetes_deaths = diabetes * diabetes_mortality
    no_surviving = no_diabetes - no_deaths
    incident_diabetes = no_surviving * diabetes_incidence
    no_next = no_surviving - incident_diabetes
    diabetes_next = diabetes - diabetes_deaths + incident_diabetes
    dead_next = dead + no_deaths + diabetes_deaths
    return np.array([no_next, diabetes_next, dead_next], dtype=float)


def cycle_rewards(
    state: np.ndarray,
    next_state: np.ndarray,
    cycle: int,
    params: Dict[str, float],
    arm: str,
) -> Tuple[float, float, float]:
    average_state = (state + next_state) / 2.0
    no_diabetes, diabetes, _dead = average_state
    alive = no_diabetes + diabetes

    cost = diabetes * params["annual_diabetes_cost_cad"]
    if arm == "semaglutide" and cycle < int(round(params["treatment_duration_years"])):
        cost += params["annual_drug_cost_cad"] * params["treatment_exposure_factor"]
        cost += params["monitoring_cost_cad"]

    base_utility = params["baseline_utility_obesity"]
    diabetes_utility = max(0.0, base_utility - params["diabetes_utility_decrement"])
    qaly = no_diabetes * base_utility + diabetes * diabetes_utility
    if arm == "semaglutide":
        weight_loss_difference = (
            params["semaglutide_weight_loss_pct"] - params["comparator_weight_loss_pct"]
        )
        utility_gain = weight_loss_difference * params["utility_gain_per_pct_weight_loss"]
        scenario = str(params.get("_effect_retention_scenario", "base"))
        qaly += alive * utility_gain * effect_decay(cycle, params["treatment_duration_years"], scenario)

    life_years = alive
    return cost, qaly, life_years


def run_arm(params: Dict[str, float], arm: str) -> Dict[str, float]:
    state = np.array([1.0, 0.0, 0.0], dtype=float)
    total_cost = 0.0
    total_qaly = 0.0
    total_ly = 0.0
    horizon = int(round(params["horizon_years"]))
    discount_rate = params["discount_rate"]

    for cycle in range(horizon):
        next_state = transition_state(state, cycle, params, arm)
        cost, qaly, ly = cycle_rewards(state, next_state, cycle, params, arm)
        discount = 1.0 / ((1.0 + discount_rate) ** (cycle + 0.5))
        total_cost += cost * discount
        total_qaly += qaly * discount
        total_ly += ly * discount
        state = next_state

    return {
        "cost": total_cost,
        "qaly": total_qaly,
        "life_years": total_ly,
        "alive_end": float(state[0] + state[1]),
        "diabetes_end": float(state[1]),
    }


def run_model(params: Dict[str, float]) -> Dict[str, float]:
    sema = run_arm(params, "semaglutide")
    comp = run_arm(params, "comparator")
    incremental_cost = sema["cost"] - comp["cost"]
    incremental_qaly = sema["qaly"] - comp["qaly"]
    incremental_ly = sema["life_years"] - comp["life_years"]
    icer = incremental_cost / incremental_qaly if incremental_qaly > 0 else math.inf
    return {
        "semaglutide_cost": sema["cost"],
        "comparator_cost": comp["cost"],
        "incremental_cost": incremental_cost,
        "semaglutide_qaly": sema["qaly"],
        "comparator_qaly": comp["qaly"],
        "incremental_qaly": incremental_qaly,
        "semaglutide_life_years": sema["life_years"],
        "comparator_life_years": comp["life_years"],
        "incremental_life_years": incremental_ly,
        "icer": icer,
        "nmb_50000": 50000.0 * incremental_qaly - incremental_cost,
        "nmb_150000": 150000.0 * incremental_qaly - incremental_cost,
        "semaglutide_alive_end": sema["alive_end"],
        "comparator_alive_end": comp["alive_end"],
        "semaglutide_diabetes_end": sema["diabetes_end"],
        "comparator_diabetes_end": comp["diabetes_end"],
    }


def sample_parameters(rng: np.random.Generator) -> Dict[str, float]:
    p = base_parameters()
    p["baseline_utility_obesity"] = clipped_normal(rng, 0.78, 0.03, 0.72, 0.84)
    p["semaglutide_weight_loss_pct"] = clipped_normal(rng, 14.9, 1.5, 11.9, 17.9)
    p["comparator_weight_loss_pct"] = clipped_normal(rng, 2.4, 0.8, 1.0, 4.0)
    if p["semaglutide_weight_loss_pct"] <= p["comparator_weight_loss_pct"]:
        p["semaglutide_weight_loss_pct"] = p["comparator_weight_loss_pct"] + 0.1
    p["utility_gain_per_pct_weight_loss"] = clipped_normal(rng, 0.00065, 0.00018, 0.00035, 0.00125)
    p["annual_drug_cost_cad"] = gamma_from_mean_cv(rng, 4726.41, 0.10, 4253.77, 5199.05)
    p["treatment_exposure_factor"] = beta_from_mean_sd(rng, 0.72, 0.065, 0.55, 0.90)
    p["monitoring_cost_cad"] = gamma_from_mean_cv(rng, 120.0, 0.40, 50.0, 250.0)
    p["annual_diabetes_incidence"] = lognormal_from_mean_cv(rng, 0.025, 0.30, 0.0125, 0.0400)
    p["diabetes_rr_semaglutide"] = lognormal_from_mean_cv(rng, 0.78, 0.13, 0.60, 0.95)
    p["annual_diabetes_cost_cad"] = gamma_from_mean_cv(rng, 1800.0, 0.35, 900.0, 3200.0)
    p["diabetes_utility_decrement"] = clipped_normal(rng, 0.045, 0.015, 0.020, 0.080)
    p["background_mortality_age50"] = clipped_normal(rng, 0.00264, 0.00045, 0.00187, 0.00389)
    p["mortality_annual_growth"] = clipped_normal(rng, 0.08575, 0.007, 0.070, 0.100)
    p["diabetes_mortality_rr"] = lognormal_from_mean_cv(rng, 1.50, 0.14, 1.20, 1.90)
    p["treatment_duration_years"] = 3.0
    p["horizon_years"] = 40.0
    p["discount_rate"] = 0.015
    return p


def percentile(values: Iterable[float], q: float) -> float:
    return float(np.percentile(np.asarray(list(values), dtype=float), q))


def rankdata(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    order = np.argsort(arr, kind="mergesort")
    ranks = np.empty(len(arr), dtype=float)
    i = 0
    while i < len(arr):
        j = i + 1
        while j < len(arr) and arr[order[j]] == arr[order[i]]:
            j += 1
        ranks[order[i:j]] = (i + j + 1) / 2.0
        i = j
    return ranks


def spearman(values: Iterable[float], target: Iterable[float]) -> float:
    x = rankdata(values)
    y = rankdata(target)
    if float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return math.nan
    return float(np.corrcoef(x, y)[0, 1])


def write_parameters() -> None:
    path = TABLE_DIR / "markov_model_parameters.csv"
    fieldnames = [
        "parameter_id",
        "category",
        "parameter_name",
        "base_value",
        "low_value",
        "high_value",
        "unit",
        "distribution",
        "source_priority",
        "source_citation",
        "extraction_note",
        "verification_status",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for index, (key, spec) in enumerate(PARAMETERS.items(), start=1):
            writer.writerow(
                {
                    "parameter_id": f"P{index:03d}",
                    "category": spec["category"],
                    "parameter_name": key,
                    "base_value": spec["base"],
                    "low_value": spec["low"],
                    "high_value": spec["high"],
                    "unit": spec["unit"],
                    "distribution": spec["distribution"],
                    "source_priority": spec["source"],
                    "source_citation": spec["source"],
                    "extraction_note": spec["note"],
                    "verification_status": spec["status"],
                }
            )


def write_base_results(base: Dict[str, float], psa: List[Dict[str, float]]) -> None:
    prob_50 = float(np.mean([row["nmb_50000"] > 0.0 for row in psa]))
    prob_150 = float(np.mean([row["nmb_150000"] > 0.0 for row in psa]))
    rows = [
        ("total_discounted_cost", base["semaglutide_cost"], base["comparator_cost"], base["incremental_cost"], "2022 CAD per patient"),
        ("total_discounted_qalys", base["semaglutide_qaly"], base["comparator_qaly"], base["incremental_qaly"], "QALYs per patient"),
        ("total_discounted_life_years", base["semaglutide_life_years"], base["comparator_life_years"], base["incremental_life_years"], "life-years per patient"),
        ("icer", "", "", base["icer"], "2022 CAD per QALY gained"),
        ("nmb_at_50000", "", "", base["nmb_50000"], "2022 CAD per patient"),
        ("nmb_at_150000", "", "", base["nmb_150000"], "2022 CAD per patient"),
        ("probability_cost_effective_at_50000", "", "", prob_50, "probability"),
        ("probability_cost_effective_at_150000", "", "", prob_150, "probability"),
        ("end_horizon_alive", base["semaglutide_alive_end"], base["comparator_alive_end"], base["semaglutide_alive_end"] - base["comparator_alive_end"], "cohort proportion"),
        ("end_horizon_diabetes", base["semaglutide_diabetes_end"], base["comparator_diabetes_end"], base["semaglutide_diabetes_end"] - base["comparator_diabetes_end"], "cohort proportion"),
    ]
    path = TABLE_DIR / "base_case_results.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["outcome_id", "outcome", "semaglutide", "comparator", "incremental", "unit", "source_or_calculation", "verification_status"])
        for idx, (outcome, sema, comp, inc, unit) in enumerate(rows, start=1):
            writer.writerow(
                [
                    f"R{idx:03d}",
                    outcome,
                    sema,
                    comp,
                    inc,
                    unit,
                    "De novo cohort Markov model run by analysis/run_markov_psa.py",
                    "model_generated_source_traced_or_calibrated_inputs",
                ]
            )


def write_psa_outputs(psa: List[Dict[str, float]]) -> None:
    draw_path = TABLE_DIR / "psa_draws.csv"
    fieldnames = [
        "draw",
        "incremental_cost",
        "incremental_qaly",
        "incremental_life_years",
        "icer",
        "nmb_50000",
        "nmb_150000",
        "annual_drug_cost_cad",
        "treatment_exposure_factor",
        "utility_gain_per_pct_weight_loss",
        "annual_diabetes_incidence",
        "diabetes_rr_semaglutide",
        "annual_diabetes_cost_cad",
        "diabetes_utility_decrement",
    ]
    with draw_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in psa:
            writer.writerow({key: row[key] for key in fieldnames})

    ceac_path = TABLE_DIR / "ceac.csv"
    with ceac_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["wtp_cad_per_qaly", "probability_cost_effective"])
        for wtp in WTP_VALUES:
            prob = float(np.mean([wtp * row["incremental_qaly"] - row["incremental_cost"] > 0.0 for row in psa]))
            writer.writerow([wtp, prob])

    summary = {
        "draws": len(psa),
        "seed": RNG_SEED,
        "incremental_cost_mean": float(np.mean([row["incremental_cost"] for row in psa])),
        "incremental_cost_p2_5": percentile([row["incremental_cost"] for row in psa], 2.5),
        "incremental_cost_p97_5": percentile([row["incremental_cost"] for row in psa], 97.5),
        "incremental_qaly_mean": float(np.mean([row["incremental_qaly"] for row in psa])),
        "incremental_qaly_p2_5": percentile([row["incremental_qaly"] for row in psa], 2.5),
        "incremental_qaly_p97_5": percentile([row["incremental_qaly"] for row in psa], 97.5),
        "icer_median": percentile([row["icer"] for row in psa if math.isfinite(row["icer"])], 50),
        "icer_p2_5": percentile([row["icer"] for row in psa if math.isfinite(row["icer"])], 2.5),
        "icer_p97_5": percentile([row["icer"] for row in psa if math.isfinite(row["icer"])], 97.5),
        "probability_cost_effective_at_50000": float(np.mean([row["nmb_50000"] > 0.0 for row in psa])),
        "probability_cost_effective_at_150000": float(np.mean([row["nmb_150000"] > 0.0 for row in psa])),
    }
    with (TABLE_DIR / "psa_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (TABLE_DIR / "psa_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, value])


def write_psa_driver_analysis(psa: List[Dict[str, float]]) -> List[Dict[str, float]]:
    target_50 = [row["nmb_50000"] for row in psa]
    target_150 = [row["nmb_150000"] for row in psa]
    target_icer = [row["icer"] for row in psa if math.isfinite(row["icer"])]
    parameter_labels = {
        "annual_drug_cost_cad": "Annual drug cost",
        "treatment_exposure_factor": "Treatment exposure",
        "utility_gain_per_pct_weight_loss": "Utility gain per weight loss",
        "annual_diabetes_incidence": "Annual diabetes incidence",
        "diabetes_rr_semaglutide": "Diabetes RR",
        "annual_diabetes_cost_cad": "Annual diabetes cost",
        "diabetes_utility_decrement": "Diabetes disutility",
    }
    rows: List[Dict[str, float]] = []
    for parameter, label in parameter_labels.items():
        values = [row[parameter] for row in psa]
        finite_pairs = [(row[parameter], row["icer"]) for row in psa if math.isfinite(row["icer"])]
        icer_values = [item[1] for item in finite_pairs]
        parameter_values_for_icer = [item[0] for item in finite_pairs]
        rows.append(
            {
                "parameter": parameter,
                "label": label,
                "spearman_nmb_50000": spearman(values, target_50),
                "spearman_nmb_150000": spearman(values, target_150),
                "spearman_icer": spearman(parameter_values_for_icer, icer_values) if target_icer else math.nan,
                "mean_value": float(np.mean(values)),
                "p2_5": percentile(values, 2.5),
                "p97_5": percentile(values, 97.5),
            }
        )
    rows.sort(key=lambda row: abs(row["spearman_nmb_150000"]), reverse=True)
    with (TABLE_DIR / "psa_driver_correlations.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def one_way_sensitivity(base_params: Dict[str, float]) -> List[Dict[str, float]]:
    varied_keys = [
        "annual_drug_cost_cad",
        "treatment_exposure_factor",
        "utility_gain_per_pct_weight_loss",
        "semaglutide_weight_loss_pct",
        "annual_diabetes_incidence",
        "diabetes_rr_semaglutide",
        "annual_diabetes_cost_cad",
        "diabetes_utility_decrement",
        "treatment_duration_years",
        "discount_rate",
    ]
    rows: List[Dict[str, float]] = []
    base_icer = run_model(base_params)["icer"]
    for key in varied_keys:
        low_params = dict(base_params)
        high_params = dict(base_params)
        low_params[key] = float(PARAMETERS[key]["low"])
        high_params[key] = float(PARAMETERS[key]["high"])
        low_result = run_model(low_params)
        high_result = run_model(high_params)
        rows.append(
            {
                "parameter": key,
                "base_value": base_params[key],
                "low_value": float(PARAMETERS[key]["low"]),
                "high_value": float(PARAMETERS[key]["high"]),
                "icer_low_value": low_result["icer"],
                "icer_high_value": high_result["icer"],
                "base_icer": base_icer,
                "absolute_swing": max(abs(low_result["icer"] - base_icer), abs(high_result["icer"] - base_icer)),
            }
        )
    rows.sort(key=lambda row: row["absolute_swing"], reverse=True)
    path = TABLE_DIR / "dsa_tornado.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def price_threshold_scenarios(base_params: Dict[str, float]) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    original_cost = base_params["annual_drug_cost_cad"]
    for reduction_pct in range(0, 91, 10):
        reduction = reduction_pct / 100.0
        params = dict(base_params)
        params["annual_drug_cost_cad"] = original_cost * (1.0 - reduction)
        result = run_model(params)
        rows.append(
            {
                "price_reduction_pct": reduction_pct,
                "annual_drug_cost_cad": params["annual_drug_cost_cad"],
                "incremental_cost": result["incremental_cost"],
                "incremental_qaly": result["incremental_qaly"],
                "icer": result["icer"],
                "nmb_50000": result["nmb_50000"],
                "nmb_150000": result["nmb_150000"],
                "cost_effective_at_50000": int(result["nmb_50000"] >= 0.0),
                "cost_effective_at_150000": int(result["nmb_150000"] >= 0.0),
            }
        )

    path = TABLE_DIR / "price_threshold_scenarios.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def solve_price_reduction_for_threshold(base_params: Dict[str, float], threshold: float) -> Dict[str, float]:
    def nmb_for_reduction(reduction: float) -> float:
        params = dict(base_params)
        params["annual_drug_cost_cad"] = base_params["annual_drug_cost_cad"] * (1.0 - reduction)
        result = run_model(params)
        return threshold * result["incremental_qaly"] - result["incremental_cost"]

    base_nmb = nmb_for_reduction(0.0)
    full_reduction_nmb = nmb_for_reduction(1.0)
    if base_nmb >= 0.0:
        reduction = 0.0
    elif full_reduction_nmb < 0.0:
        reduction = math.nan
    else:
        low, high = 0.0, 1.0
        for _ in range(60):
            mid = (low + high) / 2.0
            if nmb_for_reduction(mid) >= 0.0:
                high = mid
            else:
                low = mid
        reduction = high

    params = dict(base_params)
    if math.isfinite(reduction):
        params["annual_drug_cost_cad"] = base_params["annual_drug_cost_cad"] * (1.0 - reduction)
        result = run_model(params)
        annual_cost = params["annual_drug_cost_cad"]
        icer = result["icer"]
        incremental_cost = result["incremental_cost"]
        incremental_qaly = result["incremental_qaly"]
        nmb = threshold * incremental_qaly - incremental_cost
    else:
        annual_cost = math.nan
        icer = math.nan
        incremental_cost = math.nan
        incremental_qaly = math.nan
        nmb = math.nan

    return {
        "threshold_cad_per_qaly": threshold,
        "required_price_reduction": reduction,
        "annual_drug_cost_at_threshold_cad": annual_cost,
        "incremental_cost": incremental_cost,
        "incremental_qaly": incremental_qaly,
        "icer": icer,
        "nmb_at_threshold": nmb,
    }


def write_price_threshold_summary(base_params: Dict[str, float]) -> List[Dict[str, float]]:
    summary_rows = [
        solve_price_reduction_for_threshold(base_params, 50000.0),
        solve_price_reduction_for_threshold(base_params, 150000.0),
    ]
    with (TABLE_DIR / "price_threshold_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    schedule_rows = []
    for scenario_key, scenario in EFFECT_RETENTION_SCENARIOS.items():
        for cycle in range(0, 8):
            schedule_rows.append(
                {
                    "scenario": scenario_key,
                    "scenario_label": scenario["label"],
                    "cycle_year": cycle + 1,
                    "retained_effect_factor": effect_decay(
                        cycle,
                        base_params["treatment_duration_years"],
                        scenario_key,
                    ),
                }
            )
    with (TABLE_DIR / "effect_retention_schedule.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(schedule_rows[0].keys()))
        writer.writeheader()
        writer.writerows(schedule_rows)

    return summary_rows


def write_benefit_price_frontier(base_params: Dict[str, float], base: Dict[str, float]) -> List[Dict[str, float]]:
    grid_rows: List[Dict[str, float]] = []
    original_cost = base_params["annual_drug_cost_cad"]
    benefit_multipliers = [round(value, 2) for value in np.arange(0.0, 4.0001, 0.10)]
    for reduction_pct in range(0, 91, 5):
        params = dict(base_params)
        params["annual_drug_cost_cad"] = original_cost * (1.0 - reduction_pct / 100.0)
        result = run_model(params)
        for multiplier in benefit_multipliers:
            incremental_qaly_with_extra_benefit = result["incremental_qaly"] * (1.0 + multiplier)
            nmb_50 = 50000.0 * incremental_qaly_with_extra_benefit - result["incremental_cost"]
            nmb_150 = 150000.0 * incremental_qaly_with_extra_benefit - result["incremental_cost"]
            grid_rows.append(
                {
                    "price_reduction_pct": reduction_pct,
                    "additional_non_diabetes_qaly_multiplier": multiplier,
                    "total_incremental_qaly": incremental_qaly_with_extra_benefit,
                    "modeled_incremental_qaly": result["incremental_qaly"],
                    "incremental_cost": result["incremental_cost"],
                    "nmb_50000": nmb_50,
                    "nmb_150000": nmb_150,
                    "cost_effective_at_50000": int(nmb_50 >= 0.0),
                    "cost_effective_at_150000": int(nmb_150 >= 0.0),
                }
            )
    with (TABLE_DIR / "benefit_price_frontier_grid.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
        writer.writeheader()
        writer.writerows(grid_rows)

    summary_rows: List[Dict[str, float]] = []
    for threshold in (50000.0, 150000.0):
        required_total_qaly = base["incremental_cost"] / threshold
        additional_qaly_needed = max(0.0, required_total_qaly - base["incremental_qaly"])
        additional_multiplier = additional_qaly_needed / base["incremental_qaly"] if base["incremental_qaly"] > 0.0 else math.inf
        summary_rows.append(
            {
                "threshold_cad_per_qaly": threshold,
                "current_incremental_cost": base["incremental_cost"],
                "modeled_incremental_qaly": base["incremental_qaly"],
                "required_total_incremental_qaly_at_current_price": required_total_qaly,
                "additional_qaly_needed_at_current_price": additional_qaly_needed,
                "additional_non_diabetes_qaly_multiplier_needed": additional_multiplier,
                "interpretation": "Threshold analysis only; represents unmodeled non-diabetes benefit required at the current public price anchor.",
            }
        )
    with (TABLE_DIR / "benefit_price_frontier_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)
    return summary_rows


def write_evpi(psa: List[Dict[str, float]]) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for wtp in WTP_VALUES:
        nmb_values = np.asarray([wtp * row["incremental_qaly"] - row["incremental_cost"] for row in psa])
        expected_nmb = float(np.mean(nmb_values))
        current_decision_value = max(0.0, expected_nmb)
        expected_value_with_perfect_information = float(np.mean(np.maximum(0.0, nmb_values)))
        evpi = expected_value_with_perfect_information - current_decision_value
        rows.append(
            {
                "wtp_cad_per_qaly": wtp,
                "expected_incremental_nmb": expected_nmb,
                "evpi_per_patient": evpi,
                "probability_cost_effective": float(np.mean(nmb_values > 0.0)),
            }
        )
    with (TABLE_DIR / "evpi.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def effect_retention_sensitivity(base_params: Dict[str, float]) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for scenario_key, scenario in EFFECT_RETENTION_SCENARIOS.items():
        params = dict(base_params)
        params["_effect_retention_scenario"] = scenario_key
        result = run_model(params)
        rows.append(
            {
                "scenario": scenario_key,
                "scenario_label": scenario["label"],
                "description": scenario["description"],
                "incremental_cost": result["incremental_cost"],
                "incremental_qaly": result["incremental_qaly"],
                "icer": result["icer"],
                "nmb_50000": result["nmb_50000"],
                "nmb_150000": result["nmb_150000"],
            }
        )
    with (TABLE_DIR / "effect_retention_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_external_reference(base: Dict[str, float]) -> None:
    path = TABLE_DIR / "cadth_external_reference_comparison.csv"
    fields = [
        "metric",
        "de_novo_model",
        "cadth_external_reference",
        "absolute_difference",
        "interpretation",
    ]
    comparisons = [
        (
            "incremental_cost_cad",
            base["incremental_cost"],
            CADTH_EXTERNAL_REFERENCE["incremental_cost_cad"],
            "Benchmark comparison only. Cost proximity is expected because the model uses the public CADTH annual acquisition-cost anchor.",
        ),
        (
            "incremental_qaly",
            base["incremental_qaly"],
            CADTH_EXTERNAL_REFERENCE["incremental_qaly"],
            "Benchmark comparison only, not independent external validation, because selected utility and transition inputs are benchmark-aligned scenarios.",
        ),
        (
            "icer_cad_per_qaly",
            base["icer"],
            CADTH_EXTERNAL_REFERENCE["icer_cad_per_qaly"],
            "Benchmark comparison only. Agreement with CADTH should not be interpreted as an independent validity test.",
        ),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for metric, model_value, external_value, interpretation in comparisons:
            writer.writerow(
                {
                    "metric": metric,
                    "de_novo_model": model_value,
                    "cadth_external_reference": external_value,
                    "absolute_difference": float(model_value) - float(external_value),
                    "interpretation": interpretation,
                }
            )


def write_model_report(
    base: Dict[str, float],
    dsa: List[Dict[str, float]],
    price_summary: List[Dict[str, float]],
    effect_sensitivity: List[Dict[str, float]],
    benefit_summary: List[Dict[str, float]],
    driver_rows: List[Dict[str, float]],
) -> None:
    cadth = CADTH_EXTERNAL_REFERENCE
    lines = [
        "# Markov Model Run Report",
        "",
        f"- Run date: {date.today().isoformat()}",
        "- Revision scope: Frontiers in Public Health / Health Economics targeted submission update.",
        f"- Random seed: {RNG_SEED}",
        f"- PSA draws: {PSA_DRAWS:,}",
        "- Main analysis: Canadian public payer perspective, 2022 CAD, 40-year lifetime approximation, annual cycles, half-cycle correction, 1.5% annual discounting.",
        "- CADTH is used as a public benchmark, not as an independent external validation test.",
        "",
        "## Base-Case Results",
        "",
        f"- Incremental cost: CAD${base['incremental_cost']:,.0f}",
        f"- Incremental QALYs: {base['incremental_qaly']:.4f}",
        f"- Incremental life-years: {base['incremental_life_years']:.4f}",
        f"- ICER: CAD${base['icer']:,.0f}/QALY",
        f"- NMB at CAD$50,000/QALY: CAD${base['nmb_50000']:,.0f}",
        f"- NMB at CAD$150,000/QALY: CAD${base['nmb_150000']:,.0f}",
        "",
        "## External CADTH Reference",
        "",
        f"- CADTH incremental cost: CAD${cadth['incremental_cost_cad']:,.0f}",
        f"- CADTH incremental QALYs: {cadth['incremental_qaly']:.3f}",
        f"- CADTH ICER: CAD${cadth['icer_cad_per_qaly']:,.0f}/QALY",
        f"- CADTH price reduction at CAD$50,000/QALY: {cadth['required_price_reduction_at_50000']:.0%}",
        "",
        "## Price-Threshold Scenario Analysis",
        "",
    ]
    for row in price_summary:
        if math.isfinite(row["required_price_reduction"]):
            lines.append(
                f"- Required price reduction at CAD${row['threshold_cad_per_qaly']:,.0f}/QALY: "
                f"{row['required_price_reduction']:.1%} "
                f"(annual drug cost CAD${row['annual_drug_cost_at_threshold_cad']:,.0f})"
            )
        else:
            lines.append(
                f"- Required price reduction at CAD${row['threshold_cad_per_qaly']:,.0f}/QALY: "
                "not achieved even at a 100% drug-price reduction"
            )
    lines.extend(
        [
            "",
            "## Unmodeled-Benefit Threshold Analysis",
            "",
        ]
    )
    for row in benefit_summary:
        lines.append(
            f"- At CAD${row['threshold_cad_per_qaly']:,.0f}/QALY and current price, "
            f"total incremental QALYs would need to be {row['required_total_incremental_qaly_at_current_price']:.4f}; "
            f"this implies {row['additional_qaly_needed_at_current_price']:.4f} additional QALYs "
            f"({row['additional_non_diabetes_qaly_multiplier_needed']:.1%} of the modeled gain)."
        )
    lines.extend(
        [
        "",
        "## Effect-Retention Structural Sensitivity",
        "",
        ]
    )
    for row in effect_sensitivity:
        lines.append(
            f"- {row['scenario_label']}: incremental QALYs {row['incremental_qaly']:.4f}; "
            f"ICER CAD${row['icer']:,.0f}/QALY"
        )
    lines.extend(
        [
        "",
        "## Top One-Way Sensitivity Drivers",
        "",
        ]
    )
    for row in dsa[:5]:
        lines.append(
            f"- {row['parameter']}: ICER range CAD${row['icer_low_value']:,.0f} to CAD${row['icer_high_value']:,.0f}/QALY"
        )
    lines.extend(
        [
            "",
            "## PSA Driver Correlations",
            "",
        ]
    )
    for row in driver_rows[:5]:
        lines.append(
            f"- {row['label']}: Spearman rho with NMB at CAD$150,000/QALY = {row['spearman_nmb_150000']:.2f}"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "This run is a reproducible public-source single-complication Markov reference model. Parameter provenance is classified as source-traced, source-derived, source-informed, official life-table-derived, benchmark-aligned scenario, or guideline/structural assumption in tables/markov_model_parameters.csv and the supplementary parameter-source map.",
            "",
        ]
    )
    (ROOT / "model_run_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    base_params = base_parameters()
    base = run_model(base_params)

    rng = np.random.default_rng(RNG_SEED)
    psa: List[Dict[str, float]] = []
    for draw in range(1, PSA_DRAWS + 1):
        params = sample_parameters(rng)
        result = run_model(params)
        row = {
            "draw": draw,
            **result,
            "annual_drug_cost_cad": params["annual_drug_cost_cad"],
            "treatment_exposure_factor": params["treatment_exposure_factor"],
            "utility_gain_per_pct_weight_loss": params["utility_gain_per_pct_weight_loss"],
            "annual_diabetes_incidence": params["annual_diabetes_incidence"],
            "diabetes_rr_semaglutide": params["diabetes_rr_semaglutide"],
            "annual_diabetes_cost_cad": params["annual_diabetes_cost_cad"],
            "diabetes_utility_decrement": params["diabetes_utility_decrement"],
        }
        psa.append(row)

    dsa = one_way_sensitivity(base_params)
    price_threshold_scenarios(base_params)
    price_summary = write_price_threshold_summary(base_params)
    effect_sensitivity = effect_retention_sensitivity(base_params)
    write_parameters()
    write_base_results(base, psa)
    write_psa_outputs(psa)
    driver_rows = write_psa_driver_analysis(psa)
    write_external_reference(base)
    benefit_summary = write_benefit_price_frontier(base_params, base)
    write_evpi(psa)
    write_model_report(base, dsa, price_summary, effect_sensitivity, benefit_summary, driver_rows)

    print(json.dumps({"base_case": base, "psa_draws": len(psa)}, indent=2))


if __name__ == "__main__":
    main()
