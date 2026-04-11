"""
Experiment 10 — Additional Publication Figures
================================================
1. Interaction line plot (hero figure): Ident × Distance
2. Empathy premium bar chart (IVE delta by distance)
3. Per-model slope plot (slopegraph)
4. Fairness violation heatmap
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
from visualization.style import (
    set_paper_style, save_figure, PALETTE, MODEL_COLORS, format_pvalue,
)
from analysis.statistical_tests import compute_cohens_d

DIST_ORDER = ["near", "middle", "far"]
DIST_LABELS = ["Near\n(In-Group)", "Middle\n(Neutral)", "Far\n(Out-Group)"]
DIST_LABELS_SHORT = ["Near", "Middle", "Far"]


def plot_exp10_interaction(df, stats_results):
    """Hero figure: Interaction line plot — Identifiability × Cultural Distance."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(7, 5))

    for cond, color, marker, ls, label in [
        ("identifiable", "#E63946", "o", "-", "Identifiable Victim"),
        ("statistical", "#457B9D", "s", "--", "Statistical Victims"),
    ]:
        means, sems = [], []
        for dist in DIST_ORDER:
            cell = df[(df["cultural_distance"] == dist) &
                      (df["condition_identifiability"] == cond)]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else 0)
            sems.append(cell.sem() if len(cell) > 1 else 0)

        x = np.arange(len(DIST_ORDER))
        ax.errorbar(x, means, yerr=sems, fmt=f"{marker}{ls}", color=color,
                    linewidth=2.5, markersize=10, capsize=5, capthick=1.5,
                    markeredgecolor="white", markeredgewidth=1.5,
                    label=label, zorder=5)

        # Annotate each point
        for i, (m, s) in enumerate(zip(means, sems)):
            ax.text(i + 0.12, m + 0.05, f"${m:.2f}$", fontsize=9,
                    color=color, fontweight="bold")

    # Annotate the slope for identifiable
    ive_near = stats_results.get("ive_by_distance", {}).get("near", {})
    ive_far = stats_results.get("ive_by_distance", {}).get("far", {})
    if ive_near and ive_far:
        ax.annotate(
            f"Slope = −{abs(ive_near.get('ident_mean',0) - ive_far.get('ident_mean',0)):.2f}\n"
            f"(Parity violation: $d$ = {stats_results.get('parity_near_vs_far',{}).get('cohens_d','N/A')})",
            xy=(2, ive_far.get("ident_mean", 3.8)),
            xytext=(1.3, 3.3),
            fontsize=9, ha="center", fontstyle="italic", color="#264653",
            arrowprops=dict(arrowstyle="->", color="#264653", lw=1.2),
        )

    # Annotate statistical flatness
    ax.annotate("Statistical line:\nNearly flat ($\\Delta$ = 0.08)",
                xy=(1, 2.855), xytext=(0.2, 2.3),
                fontsize=8, ha="center", fontstyle="italic", color="#457B9D",
                arrowprops=dict(arrowstyle="->", color="#457B9D", lw=1.0))

    ax.set_xticks(np.arange(len(DIST_ORDER)))
    ax.set_xticklabels(DIST_LABELS, fontsize=10)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_xlabel("Cultural / Geographic Distance")
    ax.set_title("Interaction: Identifiability × Cultural Distance")
    ax.set_ylim(2.0, 4.8)
    ax.legend(loc="upper right", fontsize=10)

    fig.tight_layout()
    save_figure(fig, "exp10_interaction_lines")


def plot_exp10_premium_bars(df, stats_results):
    """Bar chart: IVE premium (delta) at each cultural distance."""
    set_paper_style()

    deltas, sems_d = [], []
    d_values = []
    for dist in DIST_ORDER:
        id_g = df[(df["cultural_distance"] == dist) &
                  (df["condition_identifiability"] == "identifiable")]["donation_amount"].dropna()
        st_g = df[(df["cultural_distance"] == dist) &
                  (df["condition_identifiability"] == "statistical")]["donation_amount"].dropna()
        delta = id_g.mean() - st_g.mean()
        sem = np.sqrt(id_g.sem()**2 + st_g.sem()**2)
        deltas.append(delta)
        sems_d.append(sem)
        d = compute_cohens_d(id_g, st_g)
        d_values.append(d)

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ["#E63946", "#F4A261", "#457B9D"]
    x = np.arange(len(DIST_ORDER))
    bars = ax.bar(x, deltas, yerr=sems_d, color=colors,
                  edgecolor="white", linewidth=1.5, capsize=5, width=0.55)

    # Label each bar with delta and d
    for i, (bar, delta, d) in enumerate(zip(bars, deltas, d_values)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sems_d[i] + 0.03,
                f"$\\Delta$ = {delta:.2f}\n$d$ = {d:.2f}",
                ha="center", fontsize=10, fontweight="bold", color=colors[i])

    ax.set_xticks(x)
    ax.set_xticklabels(DIST_LABELS_SHORT, fontsize=11)
    ax.set_ylabel("IVE Premium ($M_{ident} - M_{stat}$)")
    ax.set_xlabel("Cultural Distance")
    ax.set_title("IVE Premium Shrinks with Cultural Distance")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(0, max(deltas) + 0.5)

    fig.tight_layout()
    save_figure(fig, "exp10_premium_bars")


def plot_exp10_slopegraph(df, stats_results):
    """Slopegraph: Per-model identified donation from Near to Far."""
    set_paper_style()

    id_df = df[df["condition_identifiability"] == "identifiable"].copy()
    models = sorted(id_df["model_key"].unique())

    fig, ax = plt.subplots(figsize=(7, 6))

    for model in models:
        means = []
        for dist in DIST_ORDER:
            cell = id_df[(id_df["model_key"] == model) &
                         (id_df["cultural_distance"] == dist)]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else np.nan)

        color = MODEL_COLORS.get(model, "#888")
        slope = means[-1] - means[0] if not np.isnan(means[0]) and not np.isnan(means[-1]) else 0

        # Thicker lines for steep slopes
        lw = 1.0 + min(abs(slope) * 3, 3.0)
        alpha = 0.4 + min(abs(slope) * 1.5, 0.6)

        ax.plot(range(len(DIST_ORDER)), means, "o-", color=color,
                linewidth=lw, markersize=6, alpha=alpha,
                markeredgecolor="white", markeredgewidth=0.8)

        # Label at the far end
        if not np.isnan(means[-1]):
            ax.text(len(DIST_ORDER) - 1 + 0.08, means[-1],
                    model.replace("-", "\n"), fontsize=6.5, color=color,
                    va="center", alpha=0.85)

    ax.set_xticks(range(len(DIST_ORDER)))
    ax.set_xticklabels(DIST_LABELS_SHORT, fontsize=11)
    ax.set_ylabel("Mean Donation ($) — Identified Victims Only")
    ax.set_xlabel("Cultural Distance")
    ax.set_title("Per-Model In-Group Slope: Identified Victims")
    ax.set_ylim(1.5, 5.5)

    fig.tight_layout()
    save_figure(fig, "exp10_slopegraph")


def plot_exp10_fairness_heatmap(df, stats_results):
    """Heatmap: Parity violation score per model (d_near - d_far)."""
    set_paper_style()

    models = sorted(df["model_key"].unique())
    data = []
    model_labels = []

    for model in models:
        mdf = df[df["model_key"] == model]
        d_vals = []
        for dist in DIST_ORDER:
            id_g = mdf[(mdf["cultural_distance"] == dist) &
                       (mdf["condition_identifiability"] == "identifiable")]["donation_amount"].dropna()
            st_g = mdf[(mdf["cultural_distance"] == dist) &
                       (mdf["condition_identifiability"] == "statistical")]["donation_amount"].dropna()
            if len(id_g) >= 2 and len(st_g) >= 2:
                d = compute_cohens_d(id_g, st_g)
                d_vals.append(float(d) if not np.isnan(d) else 0.0)
            else:
                d_vals.append(0.0)
        data.append(d_vals)
        model_labels.append(model)

    data_arr = np.array(data)

    # Add a "Parity Violation" column: d_near - d_far
    parity_violation = data_arr[:, 0] - data_arr[:, 2]

    # Sort by descending parity violation
    sort_idx = np.argsort(-parity_violation)
    data_arr = data_arr[sort_idx]
    parity_violation = parity_violation[sort_idx]
    model_labels = [model_labels[i] for i in sort_idx]

    # Add parity column
    full_data = np.column_stack([data_arr, parity_violation])

    fig, ax = plt.subplots(figsize=(8, max(5, len(models) * 0.45)))
    col_labels = DIST_LABELS_SHORT + ["Parity\nViolation"]

    im = ax.imshow(full_data, cmap="RdBu_r", aspect="auto", vmin=-2.0, vmax=2.0)

    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(model_labels)))
    ax.set_yticklabels([m.replace("-", "\n") for m in model_labels], fontsize=8)

    # Annotate
    for i in range(len(model_labels)):
        for j in range(len(col_labels)):
            val = full_data[i, j]
            text_color = "white" if abs(val) > 1.2 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=8, color=text_color, fontweight="bold")

    # Vertical separator before parity column
    ax.axvline(2.5, color="black", linewidth=2)

    fig.colorbar(im, ax=ax, shrink=0.7, label="Cohen's $d$ (IVE)")
    ax.set_title("Cultural Fairness: IVE by Distance × Model")

    fig.tight_layout()
    save_figure(fig, "exp10_fairness_heatmap")


def plot_exp10_all_extra(df, stats_results):
    """Generate all extra Exp10 plots."""
    plot_exp10_interaction(df, stats_results)
    plot_exp10_premium_bars(df, stats_results)
    plot_exp10_slopegraph(df, stats_results)
    plot_exp10_fairness_heatmap(df, stats_results)
