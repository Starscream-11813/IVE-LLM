"""
Experiment 6 Plots — Chain-of-Thought as Deliberation (NOVEL)
==============================================================
1. Grouped bar chart: identifiability × CoT type (HERO FIGURE)
2. Faceted heatmap: CoT × Identifiability × Model
3. Radar chart of affective profiles under different CoT
4. Box plot of distribution shifts
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from visualization.style import (
    set_paper_style, save_figure, PALETTE, add_significance_bracket, format_pvalue,
)

COT_LABELS = {
    "none": "No CoT",
    "standard": "Standard",
    "empathetic": "Empathetic",
    "utilitarian": "Utilitarian",
}
COT_COLORS = [
    PALETTE["cot_none"], PALETTE["cot_standard"],
    PALETTE["cot_empathetic"], PALETTE["cot_utilitarian"],
]
COT_ORDER = ["none", "standard", "empathetic", "utilitarian"]


def plot_exp6_hero_bars(df, stats_results):
    """HERO FIGURE: grouped bars, identifiability × CoT type."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    conditions = ["statistical", "identifiable"]
    x = np.arange(len(conditions))
    n_cot = len(COT_ORDER)
    width = 0.8 / n_cot

    for i, cot in enumerate(COT_ORDER):
        means, sems = [], []
        for cond in conditions:
            cell = df[
                (df["condition_identifiability"] == cond) &
                (df["condition_cot"] == cot)
            ]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else 0)
            sems.append(cell.sem() if len(cell) > 1 else 0)
        offset = (i - (n_cot - 1) / 2) * width
        ax.bar(x + offset, means, width, yerr=sems,
               color=COT_COLORS[i], label=COT_LABELS[cot],
               edgecolor="white", capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels(["Statistical Victims", "Identifiable Victim"], fontsize=12)
    ax.set_ylabel("Mean Donation ($)", fontsize=12)
    ax.set_ylim(0, 5.5)
    ax.set_title("Chain-of-Thought as Deliberation:\nEffect on Identifiable Victim Donations",
                 fontsize=13, fontweight="bold")
    ax.legend(title="CoT Type", loc="upper left")
    fig.tight_layout()
    save_figure(fig, "exp6_hero_bars")


def plot_exp6_heatmap(df, stats_results):
    """Faceted heatmap: rows=CoT, cols=identifiability, facets=models."""
    set_paper_style()

    models = sorted(df["model_key"].unique())
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 3.5), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, model in zip(axes, models):
        mdf = df[df["model_key"] == model]
        data = []
        for cot in COT_ORDER:
            row = []
            for cond in ["statistical", "identifiable"]:
                cell = mdf[
                    (mdf["condition_identifiability"] == cond) &
                    (mdf["condition_cot"] == cot)
                ]["donation_amount"].dropna()
                row.append(cell.mean() if len(cell) > 0 else np.nan)
            data.append(row)
        arr = np.array(data)
        im = ax.imshow(arr, cmap="RdYlBu_r", aspect="auto", vmin=0, vmax=5)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Statistical", "Identifiable"], fontsize=9)
        ax.set_yticks(range(len(COT_ORDER)))
        ax.set_yticklabels([COT_LABELS[c] for c in COT_ORDER], fontsize=9)
        ax.set_title(model, fontsize=11, fontweight="bold")
        for i in range(len(COT_ORDER)):
            for j in range(2):
                if not np.isnan(arr[i, j]):
                    ax.text(j, i, f"{arr[i, j]:.1f}", ha="center", va="center",
                            fontsize=10, color="white" if arr[i, j] > 3 else "black")

    fig.colorbar(im, ax=axes, shrink=0.8, label="Mean Donation ($)")
    fig.suptitle("CoT Effect Across Models", fontweight="bold", y=1.02)
    fig.tight_layout()
    save_figure(fig, "exp6_heatmap")


def plot_exp6_boxplots(df, stats_results):
    """Box plots: faceted by identifiability × CoT."""
    set_paper_style()

    plot_df = df.dropna(subset=["donation_amount"]).copy()
    if plot_df.empty:
        return

    plot_df["cot_label"] = plot_df["condition_cot"].map(COT_LABELS)

    g = sns.catplot(
        data=plot_df, x="cot_label", y="donation_amount",
        col="condition_identifiability", kind="box",
        palette=dict(zip([COT_LABELS[c] for c in COT_ORDER], COT_COLORS)),
        order=[COT_LABELS[c] for c in COT_ORDER],
        col_order=["statistical", "identifiable"],
        height=4.5, aspect=1.2,
    )
    g.set_axis_labels("CoT Type", "Donation ($)")
    g.set_titles("{col_name}")
    g.fig.suptitle("Distribution of Donations by CoT Type", fontweight="bold", y=1.02)
    save_figure(g.fig, "exp6_boxplots")


def plot_exp6_all(df, stats_results):
    plot_exp6_hero_bars(df, stats_results)
    plot_exp6_heatmap(df, stats_results)
    plot_exp6_boxplots(df, stats_results)
