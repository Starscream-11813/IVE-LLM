"""
Experiment 2 Plots — Explicit Debiasing
========================================
1. Grouped bar chart (identifiability × intervention)
2. Interaction plot (line chart)
3. Meta-knowledge bar chart
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from visualization.style import (
    set_paper_style, save_figure, add_significance_bracket, PALETTE, format_pvalue,
)


def plot_exp2_grouped_bars(df, stats_results):
    """Grouped bar: identifiability × intervention, per model + pooled."""
    set_paper_style()

    models = sorted(df["model_key"].unique()) + ["pooled"]

    for model_label in models:
        if model_label == "pooled":
            mdf = df.copy()
        else:
            mdf = df[df["model_key"] == model_label].copy()
        if mdf.empty:
            continue

        fig, ax = plt.subplots(figsize=(6, 5))
        conditions = ["statistical", "identifiable"]
        interventions = ["none", "teaching"]
        x = np.arange(len(conditions))
        width = 0.35
        colors = [PALETTE["no_intervention"], PALETTE["intervention"]]

        for i, interv in enumerate(interventions):
            means, sems = [], []
            for cond in conditions:
                cell = mdf[
                    (mdf["condition_identifiability"] == cond) &
                    (mdf["condition_intervention"] == interv)
                ]["donation_amount"].dropna()
                means.append(cell.mean() if len(cell) > 0 else 0)
                sems.append(cell.sem() if len(cell) > 1 else 0)
            ax.bar(x + i * width - width / 2, means, width, yerr=sems,
                   color=colors[i],
                   label="No Intervention" if interv == "none" else "Teaching Intervention",
                   edgecolor="white", capsize=3)

        ax.set_xticks(x)
        ax.set_xticklabels(["Statistical", "Identifiable"])
        ax.set_ylabel("Mean Donation ($)")
        ax.set_ylim(0, 5.5)
        ax.set_title(f"Debiasing Intervention Effect ({model_label})")
        ax.legend()
        fig.tight_layout()
        save_figure(fig, f"exp2_bars_{model_label}")


def plot_exp2_interaction(df, stats_results):
    """Interaction plot: lines for intervention across identifiability."""
    set_paper_style()

    models = sorted(df["model_key"].unique())
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, model in zip(axes, models):
        mdf = df[df["model_key"] == model]
        for interv, ls, color in [("none", "-", PALETTE["no_intervention"]),
                                   ("teaching", "--", PALETTE["intervention"])]:
            means = []
            for cond in ["statistical", "identifiable"]:
                cell = mdf[
                    (mdf["condition_identifiability"] == cond) &
                    (mdf["condition_intervention"] == interv)
                ]["donation_amount"].dropna()
                means.append(cell.mean() if len(cell) > 0 else 0)
            label = "No Intervention" if interv == "none" else "Teaching"
            ax.plot(["Statistical", "Identifiable"], means, ls, color=color,
                    marker="o", label=label, linewidth=2, markersize=8)

        ax.set_title(model)
        ax.set_ylabel("Mean Donation ($)" if ax == axes[0] else "")
        ax.set_ylim(0, 5.5)
        ax.legend(fontsize=9)

    fig.suptitle("Interaction: Identifiability × Intervention", fontweight="bold", y=1.02)
    fig.tight_layout()
    save_figure(fig, "exp2_interaction")


def plot_exp2_meta_knowledge(df, stats_results):
    """Bar chart of meta-knowledge awareness by model."""
    set_paper_style()

    meta_df = df[df["meta_awareness"].notna()].copy()
    if meta_df.empty:
        return

    models = sorted(meta_df["model_key"].unique())
    pcts = []
    for model in models:
        m = meta_df[meta_df["model_key"] == model]
        pcts.append(m["meta_awareness"].mean() * 100)

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(range(len(models)), pcts,
                  color=[PALETTE["identifiable"]] * len(models),
                  edgecolor="white")
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=30, ha="right")
    ax.set_ylabel("% Acknowledging IVE Awareness")
    ax.set_ylim(0, 105)
    ax.set_title("LLM Meta-Knowledge of the IVE")

    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{pct:.0f}%", ha="center", fontsize=10)

    fig.tight_layout()
    save_figure(fig, "exp2_meta_knowledge")


def plot_exp2_all(df, stats_results):
    plot_exp2_grouped_bars(df, stats_results)
    plot_exp2_interaction(df, stats_results)
    plot_exp2_meta_knowledge(df, stats_results)
