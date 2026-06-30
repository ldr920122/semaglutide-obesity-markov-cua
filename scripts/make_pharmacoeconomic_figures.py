from pathlib import Path
import csv

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    fig.savefig(FIG_DIR / f"{name}.tiff", dpi=dpi, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def add_box(
    ax,
    xy,
    width,
    height,
    label,
    sublabel="",
    fc="#F8FAFC",
    ec="#334155",
    label_size=7.5,
    sublabel_size=6.2,
):
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
    ax.text(x + width / 2, y + height * 0.58, label, ha="center", va="center", weight="bold", fontsize=label_size)
    if sublabel:
        ax.text(x + width / 2, y + height * 0.32, sublabel, ha="center", va="center", fontsize=sublabel_size, color=COLORS["neutral"])
    return box


def add_arrow(ax, start, end, label=None, rad=0.0, color="#374151", style="-|>", label_offset=(0, 0.025), label_size=5.8):
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
        ax.text(mx + label_offset[0], my + label_offset[1], label, ha="center", va="bottom", fontsize=label_size, color=COLORS["neutral"])


def make_markov_structure():
    fig, ax = plt.subplots(figsize=(7.2, 2.85))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.02, 0.94, "a", weight="bold", fontsize=9, va="top")
    ax.text(0.07, 0.94, "Cohort Markov structure", weight="bold", fontsize=9, va="top")
    ax.text(0.07, 0.86, "Annual cycles; type 2 diabetes is the modeled complication; death is absorbing.", fontsize=6.7, color=COLORS["neutral"])

    box_y = 0.47
    box_h = 0.18
    add_box(ax, (0.075, box_y), 0.19, box_h, "No diabetes", "starting cohort", COLORS["blue_light"], COLORS["blue"], 7.9, 6.1)
    add_box(ax, (0.405, box_y), 0.19, box_h, "Type 2 diabetes", "chronic state", COLORS["gold_light"], COLORS["gold"], 7.9, 6.1)
    add_box(ax, (0.735, box_y), 0.19, box_h, "Death", "absorbing state", COLORS["red_light"], COLORS["red"], 7.9, 6.1)

    state_mid_y = box_y + box_h / 2
    add_arrow(ax, (0.265, state_mid_y), (0.405, state_mid_y))
    ax.text(0.335, state_mid_y + 0.047, "T2D onset", ha="center", va="bottom", fontsize=5.8, color=COLORS["neutral"])
    add_arrow(ax, (0.595, state_mid_y), (0.735, state_mid_y))
    ax.text(0.665, state_mid_y + 0.047, "mortality", ha="center", va="bottom", fontsize=5.8, color=COLORS["neutral"])
    add_arrow(ax, (0.25, 0.69), (0.83, 0.69), rad=-0.08)
    ax.text(0.54, 0.785, "background mortality", ha="center", va="bottom", fontsize=5.8, color=COLORS["neutral"])

    sem_box = FancyBboxPatch(
        (0.10, 0.16),
        0.36,
        0.20,
        boxstyle="round,pad=0.018,rounding_size=0.020",
        linewidth=0.9,
        edgecolor=COLORS["teal"],
        facecolor=COLORS["teal_light"],
    )
    comp_box = FancyBboxPatch(
        (0.54, 0.16),
        0.36,
        0.20,
        boxstyle="round,pad=0.018,rounding_size=0.020",
        linewidth=0.9,
        edgecolor="#64748B",
        facecolor="#EEF2F7",
    )
    ax.add_patch(sem_box)
    ax.add_patch(comp_box)
    ax.text(0.28, 0.295, "Semaglutide modifiers", ha="center", va="center", fontsize=6.9, weight="bold")
    ax.text(0.28, 0.245, "drug and monitoring cost", ha="center", va="center", fontsize=5.8, color=COLORS["neutral"])
    ax.text(0.28, 0.205, "utility gain; lower T2D incidence", ha="center", va="center", fontsize=5.8, color=COLORS["neutral"])
    ax.text(0.72, 0.295, "Comparator modifiers", ha="center", va="center", fontsize=6.9, weight="bold")
    ax.text(0.72, 0.245, "usual non-GLP-1 care", ha="center", va="center", fontsize=5.8, color=COLORS["neutral"])
    ax.text(0.72, 0.205, "baseline T2D incidence", ha="center", va="center", fontsize=5.8, color=COLORS["neutral"])
    ax.text(0.10, 0.095, "Treatment arms modify costs, utility, and transition probabilities; they are not additional health states.", fontsize=5.8, color=COLORS["neutral"])
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
    ax.text(0.0, 1.14, "h", transform=ax.transAxes, weight="bold", fontsize=9, va="bottom")
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


def make_value_frontier_and_drivers():
    frontier_rows = read_rows(TABLE_DIR / "benefit_price_frontier_grid.csv")
    driver_rows = read_rows(TABLE_DIR / "psa_driver_correlations.csv")
    write_rows(
        FIG_DIR / "value_frontier_source.csv",
        frontier_rows,
        [
            "price_reduction_pct",
            "additional_non_diabetes_qaly_multiplier",
            "total_incremental_qaly",
            "modeled_incremental_qaly",
            "incremental_cost",
            "nmb_50000",
            "nmb_150000",
            "cost_effective_at_50000",
            "cost_effective_at_150000",
        ],
    )
    write_rows(
        FIG_DIR / "psa_driver_correlations_source.csv",
        driver_rows,
        [
            "parameter",
            "label",
            "spearman_nmb_50000",
            "spearman_nmb_150000",
            "spearman_icer",
            "mean_value",
            "p2_5",
            "p97_5",
        ],
    )

    x_vals = sorted({float(row["price_reduction_pct"]) for row in frontier_rows})
    y_vals = sorted({float(row["additional_non_diabetes_qaly_multiplier"]) for row in frontier_rows})
    x_index = {value: index for index, value in enumerate(x_vals)}
    y_index = {value: index for index, value in enumerate(y_vals)}
    nmb_150 = np.empty((len(y_vals), len(x_vals)), dtype=float)
    nmb_50 = np.empty((len(y_vals), len(x_vals)), dtype=float)
    for row in frontier_rows:
        xi = x_index[float(row["price_reduction_pct"])]
        yi = y_index[float(row["additional_non_diabetes_qaly_multiplier"])]
        nmb_150[yi, xi] = float(row["nmb_150000"]) / 1000
        nmb_50[yi, xi] = float(row["nmb_50000"]) / 1000

    fig, (ax0, ax1) = plt.subplots(
        2,
        1,
        figsize=(7.2, 5.7),
        gridspec_kw={"height_ratios": [1.35, 1.0], "hspace": 0.58},
    )
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "frontier",
        ["#B64342", "#F7F7F7", COLORS["teal"]],
    )
    norm = mcolors.TwoSlopeNorm(vmin=-9.5, vcenter=0.0, vmax=8.0)
    im = ax0.imshow(
        nmb_150,
        origin="lower",
        aspect="auto",
        extent=[min(x_vals), max(x_vals), min(y_vals) * 100, max(y_vals) * 100],
        cmap=cmap,
        norm=norm,
    )
    xx, yy = np.meshgrid(x_vals, [value * 100 for value in y_vals])
    ax0.contour(xx, yy, nmb_150, levels=[0], colors=[COLORS["threshold_high"]], linewidths=1.15)
    ax0.contour(xx, yy, nmb_50, levels=[0], colors=[COLORS["threshold_low"]], linewidths=1.15, linestyles="--")
    ax0.set_title("f  Benefit-price frontier", loc="left", fontsize=8.5, weight="bold", pad=10)
    ax0.text(
        0.0,
        1.01,
        "Color shows NMB at CAD$150k/QALY; contours mark break-even at CAD$150k and CAD$50k.",
        transform=ax0.transAxes,
        fontsize=5.9,
        color=COLORS["neutral"],
    )
    ax0.set_xlabel("Annual drug-price reduction (%)", fontsize=7)
    ax0.set_ylabel("Additional non-diabetes QALY gain (% of modeled gain)", fontsize=7)
    ax0.set_xlim(min(x_vals), max(x_vals))
    ax0.set_ylim(min(y_vals) * 100, max(y_vals) * 100)
    ax0.tick_params(labelsize=6.3)
    cbar = fig.colorbar(im, ax=ax0, fraction=0.030, pad=0.018)
    cbar.ax.tick_params(labelsize=5.8)
    cbar.set_label("NMB at CAD$150k/QALY (thousand CAD)", fontsize=6.2)
    ax0.plot([], [], color=COLORS["threshold_high"], linewidth=1.2, label="CAD$150k break-even")
    ax0.plot([], [], color=COLORS["threshold_low"], linewidth=1.2, linestyle="--", label="CAD$50k break-even")
    ax0.legend(loc="lower left", fontsize=5.7, frameon=False)

    top_drivers = driver_rows[:7][::-1]
    labels = [row["label"] for row in top_drivers]
    values = np.array([float(row["spearman_nmb_150000"]) for row in top_drivers])
    colors = [COLORS["teal"] if value > 0 else COLORS["red"] for value in values]
    y = np.arange(len(labels))
    ax1.axvline(0, color="#9CA3AF", linewidth=0.8)
    ax1.barh(y, values, color=colors, alpha=0.85, height=0.54)
    for yi, value in zip(y, values):
        ax1.text(
            value + (0.025 if value >= 0 else -0.025),
            yi,
            f"{value:+.2f}",
            va="center",
            ha="left" if value >= 0 else "right",
            fontsize=5.8,
            color=COLORS["neutral"],
        )
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, fontsize=6.1)
    ax1.set_xlim(-0.82, 0.82)
    ax1.set_xlabel("Spearman correlation with NMB at CAD$150k/QALY", fontsize=7)
    ax1.set_title("g  Probabilistic drivers", loc="left", fontsize=8.5, weight="bold", pad=10)
    ax1.text(
        0.0,
        1.01,
        "PSA ranks show which inputs move net benefit most.",
        transform=ax1.transAxes,
        fontsize=5.9,
        color=COLORS["neutral"],
    )
    ax1.tick_params(axis="x", labelsize=6.3)
    ax1.tick_params(axis="y", length=0)
    ax1.spines["left"].set_visible(False)
    save_pub(fig, "value_frontier_and_drivers")


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
    make_value_frontier_and_drivers()
    make_icer_scenarios()
    make_price_stress()
