from pathlib import Path
import csv

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "legend.frameon": False,
    }
)


COLORS = {
    "blue": "#0F4D92",
    "blue_light": "#DCEBFA",
    "teal": "#42949E",
    "teal_light": "#DDEFF1",
    "gold": "#B8860B",
    "gold_light": "#FFF3C4",
    "red": "#B64342",
    "red_light": "#F8D9D6",
    "neutral": "#4D4D4D",
    "neutral_light": "#F2F3F5",
    "threshold_low": "#B64342",
    "threshold_high": "#B8860B",
}


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})


def base_incremental_results():
    rows = read_rows(TABLE_DIR / "base_case_results.csv")
    return {row["outcome"]: float(row["incremental"]) for row in rows if row["incremental"] not in ("", None)}


def pretty_parameter(name):
    labels = {
        "diabetes_rr_semaglutide": "Diabetes RR",
        "annual_diabetes_incidence": "Diabetes incidence",
        "utility_gain_per_pct_weight_loss": "Utility gain per weight loss",
        "treatment_duration_years": "Treatment duration",
        "treatment_exposure_factor": "Treatment exposure",
        "discount_rate": "Discount rate",
        "diabetes_utility_decrement": "Diabetes disutility",
        "semaglutide_weight_loss_pct": "Semaglutide weight loss",
        "annual_drug_cost_cad": "Drug cost",
        "annual_diabetes_cost_cad": "Diabetes cost",
    }
    return labels.get(name, name.replace("_", " ").title())


def save_pub(fig, name, dpi=600):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf"):
        fig.savefig(FIG_DIR / f"{name}.{ext}", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{name}.tiff", dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def add_box(ax, xy, width, height, label, sublabel="", fc="#F8FAFC", ec="#334155"):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=0.9,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(box)
    x, y = xy
    ax.text(x + width / 2, y + height * 0.58, label, ha="center", va="center", weight="bold", fontsize=7.5)
    if sublabel:
        ax.text(x + width / 2, y + height * 0.32, sublabel, ha="center", va="center", fontsize=6.2, color=COLORS["neutral"])
    return box


def add_arrow(ax, start, end, label=None, rad=0.0, color="#374151", style="-|>", label_offset=(0, 0.025)):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=10,
        linewidth=0.8,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arrow)
    if label:
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        ax.text(mx + label_offset[0], my + label_offset[1], label, ha="center", va="bottom", fontsize=5.8, color=COLORS["neutral"])


def make_markov_structure():
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.02, 0.96, "a", weight="bold", fontsize=9, va="top")
    ax.text(0.06, 0.96, "Implemented Markov model structure", weight="bold", fontsize=9, va="top")
    ax.text(0.06, 0.90, "Annual cycles; diabetes is the modeled obesity-related complication; death is absorbing.", fontsize=6.5, color=COLORS["neutral"])

    add_box(ax, (0.07, 0.56), 0.22, 0.13, "No diabetes", "starting cohort", COLORS["blue_light"], COLORS["blue"])
    add_box(ax, (0.39, 0.56), 0.22, 0.13, "Type 2 diabetes", "chronic complication", COLORS["gold_light"], COLORS["gold"])
    add_box(ax, (0.72, 0.56), 0.20, 0.13, "Death", "absorbing state", COLORS["red_light"], COLORS["red"])

    add_arrow(ax, (0.29, 0.625), (0.39, 0.625), "incident diabetes")
    add_arrow(ax, (0.61, 0.625), (0.72, 0.625), "excess mortality")
    add_arrow(ax, (0.30, 0.745), (0.82, 0.745), "background mortality", rad=-0.22, label_offset=(0, 0.075))
    add_arrow(ax, (0.13, 0.705), (0.21, 0.705), "remain", rad=-0.90)
    add_arrow(ax, (0.46, 0.705), (0.54, 0.705), "remain", rad=-0.90)

    add_box(ax, (0.07, 0.31), 0.38, 0.16, "Semaglutide arm", "drug + monitoring cost\nHRQoL gain; lower diabetes incidence", COLORS["teal_light"], COLORS["teal"])
    add_box(ax, (0.55, 0.31), 0.37, 0.16, "Comparator arm", "non-GLP-1 management\nbaseline diabetes incidence", "#EEF2F7", "#64748B")

    ax.text(
        0.07,
        0.17,
        "Costs, QALYs, and life-years accrue with half-cycle correction. The implemented public-source model is intentionally parsimonious; additional complications can be added in future versions.",
        fontsize=6.1,
        color=COLORS["neutral"],
        wrap=True,
    )
    save_pub(fig, "markov_structure")


def make_icer_scenarios():
    labels = [
        "CADTH reference case",
        "No prediabetes cost savings",
        "No delay in diabetes onset",
        "Full Health Canada indication",
    ]
    values = [204928, 209449, 241914, 223572]
    colors = [COLORS["blue"], COLORS["teal"], "#F97316", "#64748B"]

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    y = list(range(len(labels)))
    ax.barh(y, values, color=colors, height=0.58, edgecolor="white", linewidth=0.6)
    ax.axvline(50000, color=COLORS["threshold_low"], linestyle="--", linewidth=0.9)
    ax.axvline(150000, color=COLORS["threshold_high"], linestyle="--", linewidth=0.9)
    label_y = len(labels) - 0.55
    ax.text(50000, label_y, "CAD$50k/QALY", ha="center", va="bottom", fontsize=6, color=COLORS["threshold_low"])
    ax.text(150000, label_y, "CAD$150k/QALY", ha="center", va="bottom", fontsize=6, color=COLORS["threshold_high"])
    for i, v in enumerate(values):
        ax.text(v + 4500, i, f"CAD${v:,.0f}", va="center", fontsize=6.6)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 270000)
    ax.set_xlabel("ICER (CAD per QALY gained)", fontsize=7)
    ax.set_title("Public reference-case and scenario ICERs", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "e", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(0, 1.01, "All listed CADTH scenarios exceed common willingness-to-pay thresholds.", transform=ax.transAxes, fontsize=6.5, color=COLORS["neutral"])
    ax.tick_params(axis="x", labelsize=6.5)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_pub(fig, "icer_scenario_thresholds")


def make_price_stress():
    labels = [
        "Introductory self-pay scenario",
        "Standard self-pay scenario",
        "Announced 2027 list-price scenario",
    ]
    values = [160587, 167109, 337196]
    colors = [COLORS["teal"], COLORS["blue"], "#F97316"]

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    y = list(range(len(labels)))
    ax.barh(y, values, color=colors, height=0.58, edgecolor="white", linewidth=0.6)
    ax.axvline(50000, color=COLORS["threshold_low"], linestyle="--", linewidth=0.9)
    ax.axvline(150000, color=COLORS["threshold_high"], linestyle="--", linewidth=0.9)
    label_y = len(labels) - 0.52
    ax.text(50000, label_y, "US$50k/QALY", ha="center", va="bottom", fontsize=6, color=COLORS["threshold_low"])
    ax.text(150000, label_y, "US$150k/QALY", ha="center", va="bottom", fontsize=6, color=COLORS["threshold_high"])
    for i, v in enumerate(values):
        ax.text(v + 6500, i, f"US${v:,.0f}", va="center", fontsize=6.6)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 380000)
    ax.set_xlabel("Derived ICER (US$ per QALY gained)", fontsize=7)
    ax.set_title("Illustrative U.S. price-stress ICERs", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "f", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(0, 1.01, "Arithmetic stress tests anchored to the public QALY gain; not final U.S. payer results.", transform=ax.transAxes, fontsize=6.5, color=COLORS["neutral"])
    ax.tick_params(axis="x", labelsize=6.5)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_pub(fig, "price_stress_icer")


def make_price_threshold_curve():
    rows = read_rows(TABLE_DIR / "price_threshold_scenarios.csv")
    write_rows(
        FIG_DIR / "price_threshold_curve_source.csv",
        rows,
        [
            "price_reduction_pct",
            "annual_drug_cost_cad",
            "incremental_cost",
            "incremental_qaly",
            "icer",
            "nmb_50000",
            "nmb_150000",
            "cost_effective_at_50000",
            "cost_effective_at_150000",
        ],
    )

    x = np.array([float(row["price_reduction_pct"]) for row in rows])
    y = np.array([float(row["icer"]) / 1000 for row in rows])

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.plot(x, y, color=COLORS["blue"], linewidth=1.8, marker="o", markersize=3.8)
    ax.fill_between(x, y, y.min(), color=COLORS["blue_light"], alpha=0.55)
    ax.axhline(50, color=COLORS["threshold_low"], linestyle="--", linewidth=0.9)
    ax.axhline(150, color=COLORS["threshold_high"], linestyle="--", linewidth=0.9)
    ax.text(91, 50, "CAD$50k/QALY", ha="right", va="bottom", fontsize=6, color=COLORS["threshold_low"])
    ax.text(91, 150, "CAD$150k/QALY", ha="right", va="bottom", fontsize=6, color=COLORS["threshold_high"])
    for xi, yi in zip(x[::2], y[::2]):
        ax.text(xi, yi + 8, f"{yi:,.0f}", ha="center", va="bottom", fontsize=5.8, color=COLORS["neutral"])
    ax.set_xlim(-2, 92)
    ax.set_ylim(0, max(240, y.max() * 1.12))
    ax.set_xlabel("Semaglutide annual drug-price reduction (%)", fontsize=7)
    ax.set_ylabel("ICER (thousand 2022 CAD per QALY)", fontsize=7)
    ax.set_title("Price-threshold scenario analysis", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "e", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(
        0,
        1.01,
        "ICER declines with drug-price reductions; QALY gain is held constant within each price scenario.",
        transform=ax.transAxes,
        fontsize=6.5,
        color=COLORS["neutral"],
    )
    ax.tick_params(labelsize=6.5)
    fig.tight_layout()
    save_pub(fig, "price_threshold_curve")


def make_cost_effectiveness_plane():
    rows = read_rows(TABLE_DIR / "psa_draws.csv")
    base = base_incremental_results()
    fieldnames = ["draw", "incremental_qaly", "incremental_cost", "nmb_50000", "nmb_150000"]
    write_rows(FIG_DIR / "cost_effectiveness_plane_source.csv", rows, fieldnames)

    x = np.array([float(row["incremental_qaly"]) for row in rows])
    y = np.array([float(row["incremental_cost"]) for row in rows])
    x_max = max(0.10, float(np.percentile(x, 99.5)) * 1.12)
    y_max = max(14500, float(np.percentile(y, 99.5)) * 1.12)

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    colors = np.where(150000 * x - y > 0, COLORS["teal"], COLORS["blue"])
    ax.scatter(x, y, s=8, alpha=0.32, c=colors, linewidths=0, rasterized=True)

    xs = np.linspace(0, x_max, 100)
    ax.plot(xs, 50000 * xs, linestyle="--", color=COLORS["threshold_low"], linewidth=1.0, label="CAD$50k/QALY")
    ax.plot(xs, 150000 * xs, linestyle="--", color=COLORS["threshold_high"], linewidth=1.0, label="CAD$150k/QALY")
    ax.scatter([base["total_discounted_qalys"]], [base["total_discounted_cost"]], s=42, color=COLORS["red"], edgecolor="white", linewidth=0.7, zorder=5, label="Base case")

    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_xlabel("Incremental QALYs", fontsize=7)
    ax.set_ylabel("Incremental cost (2022 CAD)", fontsize=7)
    ax.set_title("Probabilistic cost-effectiveness plane", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "b", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(
        0,
        1.01,
        "Each point is one PSA draw; teal points are cost-effective at CAD$150k/QALY.",
        transform=ax.transAxes,
        fontsize=6.5,
        color=COLORS["neutral"],
    )
    ax.legend(loc="upper left", fontsize=6.4, ncol=3, handlelength=1.6)
    ax.tick_params(labelsize=6.5)
    fig.tight_layout()
    save_pub(fig, "cost_effectiveness_plane")


def make_ceac():
    rows = read_rows(TABLE_DIR / "ceac.csv")
    write_rows(FIG_DIR / "ceac_source.csv", rows, ["wtp_cad_per_qaly", "probability_cost_effective"])
    wtp = np.array([float(row["wtp_cad_per_qaly"]) for row in rows])
    prob = np.array([float(row["probability_cost_effective"]) for row in rows])
    prob_50 = prob[np.where(wtp == 50000)[0][0]]
    prob_150 = prob[np.where(wtp == 150000)[0][0]]

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(wtp, prob, color=COLORS["blue"], linewidth=2.0)
    ax.fill_between(wtp, prob, 0, color=COLORS["blue_light"], alpha=0.7)
    ax.axvline(50000, color=COLORS["threshold_low"], linestyle="--", linewidth=0.9)
    ax.axvline(150000, color=COLORS["threshold_high"], linestyle="--", linewidth=0.9)
    ax.scatter([50000, 150000], [prob_50, prob_150], color=[COLORS["threshold_low"], COLORS["threshold_high"]], s=28, zorder=5)
    ax.text(50000, min(0.94, prob_50 + 0.07), f"{prob_50:.1%}", ha="center", fontsize=6.5, color=COLORS["threshold_low"])
    ax.text(150000, min(0.94, prob_150 + 0.07), f"{prob_150:.1%}", ha="center", fontsize=6.5, color=COLORS["threshold_high"])
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0, 300000)
    ax.set_xlabel("Willingness-to-pay threshold (2022 CAD per QALY)", fontsize=7)
    ax.set_ylabel("Probability cost-effective", fontsize=7)
    ax.set_title("Cost-effectiveness acceptability curve", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "c", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(
        0,
        1.01,
        "PSA indicates low probability of cost-effectiveness at common Canadian threshold scenarios.",
        transform=ax.transAxes,
        fontsize=6.5,
        color=COLORS["neutral"],
    )
    ax.tick_params(labelsize=6.5)
    fig.tight_layout()
    save_pub(fig, "ceac")


def make_tornado_icer():
    rows = read_rows(TABLE_DIR / "dsa_tornado.csv")[:8]
    write_rows(
        FIG_DIR / "tornado_icer_source.csv",
        rows,
        ["parameter", "base_value", "low_value", "high_value", "icer_low_value", "icer_high_value", "base_icer", "absolute_swing"],
    )

    labels = [pretty_parameter(row["parameter"]) for row in rows][::-1]
    low = np.array([min(float(row["icer_low_value"]), float(row["icer_high_value"])) / 1000 for row in rows][::-1])
    high = np.array([max(float(row["icer_low_value"]), float(row["icer_high_value"])) / 1000 for row in rows][::-1])
    base = float(rows[0]["base_icer"]) / 1000
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.barh(y, high - low, left=low, color=COLORS["blue_light"], edgecolor=COLORS["blue"], linewidth=0.8, height=0.58)
    ax.axvline(base, color=COLORS["red"], linewidth=1.0, label=f"Base ICER CAD${base:,.0f}k/QALY")
    for yi, lo, hi in zip(y, low, high):
        ax.text(lo + 2, yi, f"{lo:,.0f}", va="center", ha="left", fontsize=5.8, color=COLORS["neutral"])
        ax.text(hi + 4, yi, f"{hi:,.0f}", va="center", ha="left", fontsize=5.8, color=COLORS["neutral"])
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.7)
    ax.set_xlabel("ICER (thousand 2022 CAD per QALY gained)", fontsize=7)
    ax.set_title("One-way sensitivity analysis", loc="left", fontsize=9, weight="bold", pad=18)
    ax.text(0.0, 1.14, "d", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
    ax.text(
        0,
        1.01,
        "Long bars indicate parameters with the largest impact on the base-case ICER.",
        transform=ax.transAxes,
        fontsize=6.5,
        color=COLORS["neutral"],
    )
    ax.legend(loc="lower right", fontsize=6.3)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_pub(fig, "tornado_icer")


if __name__ == "__main__":
    make_markov_structure()
    make_cost_effectiveness_plane()
    make_ceac()
    make_tornado_icer()
    make_price_threshold_curve()
    make_icer_scenarios()
    make_price_stress()
