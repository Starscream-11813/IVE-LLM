"""
Experiment 9 — Additional Publication Figures
===============================================
1. Annotated U-Curve line plot (hero figure)
2. Step-size waterfall chart
3. Per-model heatmap (6 levels × N models)
4. Distress vs Donation dual-axis dissociation plot
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
from visualization.style import (
    set_paper_style, save_figure, PALETTE, MODEL_COLORS, format_pvalue,
)

LEVELS_ORDER = ["bare", "age", "age_gender", "age_gender_name",
                "age_gender_name_location", "full_narrative"]
LEVEL_LABELS = ["Bare\n(No ID)", "+Age", "+Age\n+Gender", "+Age+Gender\n+Name",
                "+Age+Gender\n+Name+Loc", "Full\nNarrative"]
LEVEL_LABELS_SHORT = ["Bare", "+Age", "+Gen", "+Name", "+Loc", "Full"]


def plot_exp9_ucurve(df, stats_results):
    """Hero figure: Annotated U-curve of donation across identification levels."""
    set_paper_style()

    means, sems, ns = [], [], []
    for level in LEVELS_ORDER:
        cell = df[df["identification_level"] == level]["donation_amount"].dropna()
        means.append(cell.mean() if len(cell) > 0 else 0)
        sems.append(cell.sem() if len(cell) > 1 else 0)
        ns.append(len(cell))

    x = np.arange(len(LEVELS_ORDER))
    fig, ax = plt.subplots(figsize=(8, 5))

    # Baseline reference
    ax.axhline(means[0], color="#aaa", linestyle="--", linewidth=1, alpha=0.7,
               label=f"Bare baseline ($M = {means[0]:.2f}$)")

    # Main line
    ax.errorbar(x, means, yerr=sems, fmt="o-", color="#E63946", linewidth=2.5,
                markersize=9, capsize=5, capthick=1.5, markeredgecolor="white",
                markeredgewidth=1.5, zorder=5)

    # Shade the "dip" region
    ax.axvspan(1.5, 4.5, alpha=0.07, color="#457B9D", zorder=0)
    ax.text(3.0, ax.get_ylim()[0] + 0.05, "Information Dilution Zone",
            ha="center", fontsize=9, fontstyle="italic", color="#457B9D")

    # Annotate spikes and trough
    # Spike at Level 2 (Age)
    ax.annotate(f"↑ Age spike\n$\\Delta$ = +{means[1]-means[0]:.2f}***",
                xy=(1, means[1]), xytext=(1.4, means[1] + 0.25),
                fontsize=9, ha="left", color="#2A9D8F", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2A9D8F", lw=1.5))

    # Trough at Level 5 (Location)
    ax.annotate(f"↓ Location trough\n$\\Delta$ = {means[4]-means[1]:.2f}***",
                xy=(4, means[4]), xytext=(2.5, means[4] - 0.30),
                fontsize=9, ha="center", color="#E76F51", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#E76F51", lw=1.5))

    # Rebound at Level 6 (Narrative)
    ax.annotate(f"↑ Narrative rebound\n$\\Delta$ = +{means[5]-means[4]:.2f}***",
                xy=(5, means[5]), xytext=(4.6, means[5] + 0.25),
                fontsize=9, ha="left", color="#2A9D8F", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2A9D8F", lw=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(LEVEL_LABELS, fontsize=9)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_xlabel("Identification Level")
    ax.set_title("Identification Gradient: The Non-Monotonic 'U-Curve'")
    ax.set_ylim(min(means) - 0.5, max(means) + 0.6)
    ax.legend(loc="lower left", fontsize=9)

    fig.tight_layout()
    save_figure(fig, "exp9_ucurve_annotated")


def plot_exp9_waterfall(df, stats_results):
    """Waterfall chart: cumulative step-sizes from bare baseline."""
    set_paper_style()

    means = []
    for level in LEVELS_ORDER:
        cell = df[df["identification_level"] == level]["donation_amount"].dropna()
        means.append(cell.mean() if len(cell) > 0 else 0)

    deltas = [0] + [means[i+1] - means[i] for i in range(len(means)-1)]
    cumulative = [means[0]]
    for d in deltas[1:]:
        cumulative.append(cumulative[-1] + d)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#264653"] + ["#2A9D8F" if d > 0 else "#E63946" for d in deltas[1:]]

    # Draw bars from cumulative base
    for i in range(len(LEVELS_ORDER)):
        if i == 0:
            ax.bar(i, means[0], color=colors[0], edgecolor="white", linewidth=1)
        else:
            bottom = cumulative[i-1]
            height = deltas[i]
            ax.bar(i, height, bottom=bottom, color=colors[i],
                   edgecolor="white", linewidth=1)
            # Connector line
            ax.plot([i-0.4, i+0.4], [cumulative[i-1], cumulative[i-1]],
                    color="#888", linewidth=0.8, linestyle=":")

    # Annotate deltas
    for i in range(1, len(deltas)):
        d = deltas[i]
        y_pos = cumulative[i] + (0.06 if d > 0 else -0.12)
        sign = "+" if d > 0 else ""
        ax.text(i, y_pos, f"{sign}{d:.2f}", ha="center", fontsize=9,
                fontweight="bold", color=colors[i])

    ax.set_xticks(range(len(LEVELS_ORDER)))
    ax.set_xticklabels(LEVEL_LABELS_SHORT, fontsize=10)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_xlabel("Identification Level")
    ax.set_title("Step-Size Waterfall: Marginal Impact of Each Detail")

    legend_elements = [
        mpatches.Patch(facecolor="#2A9D8F", label="Positive step"),
        mpatches.Patch(facecolor="#E63946", label="Negative step (dilution)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    fig.tight_layout()
    save_figure(fig, "exp9_waterfall")


def plot_exp9_model_heatmap(df, stats_results):
    """Heatmap: Mean donation per model × identification level."""
    set_paper_style()

    models = sorted(df["model_key"].unique())
    data = []
    for model in models:
        row = []
        for level in LEVELS_ORDER:
            cell = df[(df["model_key"] == model) &
                      (df["identification_level"] == level)]["donation_amount"].dropna()
            row.append(cell.mean() if len(cell) > 0 else np.nan)
        data.append(row)

    data_arr = np.array(data)
    fig, ax = plt.subplots(figsize=(9, max(5, len(models) * 0.5)))

    im = ax.imshow(data_arr, cmap="RdYlGn", aspect="auto", vmin=2.0, vmax=5.0)

    ax.set_xticks(range(len(LEVELS_ORDER)))
    ax.set_xticklabels(LEVEL_LABELS_SHORT, fontsize=10)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([m.replace("-", "\n") for m in models], fontsize=8)

    # Annotate cells
    for i in range(len(models)):
        for j in range(len(LEVELS_ORDER)):
            val = data_arr[i, j]
            if not np.isnan(val):
                text_color = "white" if val > 4.0 or val < 2.5 else "black"
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                        fontsize=8, color=text_color, fontweight="bold")

    fig.colorbar(im, ax=ax, shrink=0.7, label="Mean Donation ($)")
    ax.set_title("Model × Identification Level: Donation Heatmap")
    ax.set_xlabel("Identification Level")

    fig.tight_layout()
    save_figure(fig, "exp9_model_heatmap")


def plot_exp9_dual_axis(df, stats_results):
    """Dual-axis plot: Donation and Distress Composite across levels."""
    set_paper_style()

    don_means, don_sems = [], []
    dis_means, dis_sems = [], []

    has_distress = "distress_composite" in df.columns

    for level in LEVELS_ORDER:
        cell_don = df[df["identification_level"] == level]["donation_amount"].dropna()
        don_means.append(cell_don.mean() if len(cell_don) > 0 else 0)
        don_sems.append(cell_don.sem() if len(cell_don) > 1 else 0)

        if has_distress:
            cell_dis = df[df["identification_level"] == level]["distress_composite"].dropna()
            dis_means.append(cell_dis.mean() if len(cell_dis) > 0 else 0)
            dis_sems.append(cell_dis.sem() if len(cell_dis) > 1 else 0)

    if not has_distress:
        print("  [!] No distress_composite column found; skipping dual-axis plot.")
        return

    x = np.arange(len(LEVELS_ORDER))
    fig, ax1 = plt.subplots(figsize=(8, 5))

    # Donation line (left axis)
    color1 = "#E63946"
    ax1.errorbar(x, don_means, yerr=don_sems, fmt="o-", color=color1,
                 linewidth=2.5, markersize=8, capsize=4, capthick=1.5,
                 markeredgecolor="white", markeredgewidth=1.2, label="Donation ($)",
                 zorder=5)
    ax1.set_ylabel("Mean Donation ($)", color=color1, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_ylim(min(don_means) - 0.4, max(don_means) + 0.5)

    # Distress line (right axis)
    ax2 = ax1.twinx()
    color2 = "#457B9D"
    ax2.errorbar(x, dis_means, yerr=dis_sems, fmt="s--", color=color2,
                 linewidth=2.5, markersize=8, capsize=4, capthick=1.5,
                 markeredgecolor="white", markeredgewidth=1.2, label="Distress Composite",
                 zorder=4)
    ax2.set_ylabel("Distress Composite (1–7)", color=color2, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color2)

    # Highlight dissociation region
    ax1.annotate("Dissociation:\nDonation ↑ despite Distress ↓",
                 xy=(5, don_means[5]), xytext=(3.5, don_means[5] + 0.35),
                 fontsize=9, ha="center", fontstyle="italic",
                 arrowprops=dict(arrowstyle="->", color="#264653", lw=1.2),
                 color="#264653")

    ax1.set_xticks(x)
    ax1.set_xticklabels(LEVEL_LABELS_SHORT, fontsize=10)
    ax1.set_xlabel("Identification Level")
    ax1.set_title("Mechanistic Dissociation: Donation vs. Distress")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left", fontsize=9)

    fig.tight_layout()
    save_figure(fig, "exp9_dissociation_dual")


def plot_exp9_all_extra(df, stats_results):
    """Generate all extra Exp9 plots."""
    plot_exp9_ucurve(df, stats_results)
    plot_exp9_waterfall(df, stats_results)
    plot_exp9_model_heatmap(df, stats_results)
    plot_exp9_dual_axis(df, stats_results)
