"""
Experiment 4 Plots — Joint vs. Separate Presentation
=====================================================
1. Bar chart (3 conditions)
2. Stacked bar for allocation task
3. Paired comparison (waterfall)
"""

import matplotlib.pyplot as plt
import numpy as np
from visualization.style import (
    set_paper_style, save_figure, add_significance_bracket, PALETTE, format_pvalue,
)


def plot_exp4_main_bars(df, stats_results):
    """3-condition bar chart: Statistical, Identifiable, Combined."""
    set_paper_style()

    conditions = ["statistical", "identifiable", "combined"]
    labels = ["Statistical\nOnly", "Identifiable\nOnly", "Combined"]
    colors = [PALETTE["statistical"], PALETTE["identifiable"], PALETTE["combined"]]

    # Filter out allocation task rows
    ddf = df[df.get("rokia_donation", df["donation_amount"]).isna() |
             df["donation_amount"].notna()].copy()

    means, sems = [], []
    for cond in conditions:
        cell = ddf[ddf["condition_identifiability"] == cond]["donation_amount"].dropna()
        means.append(cell.mean() if len(cell) > 0 else 0)
        sems.append(cell.sem() if len(cell) > 1 else 0)

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(range(len(conditions)), means, yerr=sems,
                  color=colors, edgecolor="white", capsize=4, width=0.6)
    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Joint vs. Separate Presentation")

    # Significance brackets
    pw = stats_results.get("pairwise", {})
    pairs_to_show = [
        ("identifiable", "combined", 0, 1, 2),
    ]
    for a, b, _, idx_a, idx_b in pairs_to_show:
        key = f"{a}_vs_{b}"
        if key in pw and pw[key].get("t_p") is not None:
            y_max = max(means[idx_a] + sems[idx_a], means[idx_b] + sems[idx_b])
            add_significance_bracket(ax, idx_a, idx_b, y_max + 0.15, pw[key]["t_p"])

    fig.tight_layout()
    save_figure(fig, "exp4_main_bars")


def plot_exp4_allocation(df, stats_results):
    """Stacked horizontal bar: allocation (Rokia vs General Fund vs Kept)."""
    set_paper_style()

    alloc_df = df[df["rokia_donation"].notna()].copy()
    if alloc_df.empty:
        return

    models = sorted(alloc_df["model_key"].unique())
    fig, ax = plt.subplots(figsize=(8, max(3, len(models) * 0.8)))

    for i, model in enumerate(models):
        m = alloc_df[alloc_df["model_key"] == model]
        rokia = m["rokia_donation"].mean()
        general = m["general_fund"].mean()
        kept = m["amount_kept"].mean() if "amount_kept" in m and m["amount_kept"].notna().any() else 5 - rokia - general

        ax.barh(i, rokia, color=PALETTE["identifiable"], edgecolor="white",
                label="Rokia" if i == 0 else "")
        ax.barh(i, general, left=rokia, color=PALETTE["statistical"],
                edgecolor="white", label="General Fund" if i == 0 else "")
        ax.barh(i, kept, left=rokia + general, color="#CCCCCC",
                edgecolor="white", label="Kept" if i == 0 else "")

    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_xlabel("Amount ($)")
    ax.set_xlim(0, 5.2)
    ax.set_title("Allocation: Rokia vs. General Fund")
    ax.legend(loc="lower right")
    fig.tight_layout()
    save_figure(fig, "exp4_allocation")


def plot_exp4_all(df, stats_results):
    plot_exp4_main_bars(df, stats_results)
    plot_exp4_allocation(df, stats_results)
