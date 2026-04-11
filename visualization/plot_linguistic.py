"""
Linguistic Analysis Plots
==========================
1. Sympathy density bar chart
2. Reasoning type distribution (stacked)
3. Emotion-logic ratio vs donation scatter
4. Feature correlation heatmap
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from visualization.style import set_paper_style, save_figure, PALETTE


def plot_sympathy_density(df):
    """Grouped bar: sympathy density by condition."""
    set_paper_style()

    plot_df = df.dropna(subset=["sympathy_density"]).copy()
    if plot_df.empty or "condition_identifiability" not in plot_df.columns:
        return

    fig, ax = plt.subplots(figsize=(6, 4.5))

    conditions = ["statistical", "identifiable"]
    cond_present = [c for c in conditions if c in plot_df["condition_identifiability"].values]
    if not cond_present:
        return

    means, sems = [], []
    for cond in cond_present:
        s = plot_df[plot_df["condition_identifiability"] == cond]["sympathy_density"]
        means.append(s.mean())
        sems.append(s.sem() if len(s) > 1 else 0)

    colors = [PALETTE.get(c, "#999") for c in cond_present]
    ax.bar(range(len(cond_present)), means, yerr=sems, color=colors,
           edgecolor="white", capsize=4, width=0.5)
    ax.set_xticks(range(len(cond_present)))
    ax.set_xticklabels([c.title() for c in cond_present])
    ax.set_ylabel("Sympathy Density (per 100 words)")
    ax.set_title("Sympathy Language in LLM Justifications")
    fig.tight_layout()
    save_figure(fig, "ling_sympathy_density")


def plot_reasoning_type_distribution(df):
    """Stacked bar: reasoning type proportions."""
    set_paper_style()

    plot_df = df.dropna(subset=["reasoning_type"]).copy()
    if plot_df.empty:
        return

    conds = [c for c in ["statistical", "identifiable"] if c in plot_df["condition_identifiability"].values]
    if not conds:
        return

    types = ["emotional", "utilitarian", "mixed", "neutral"]
    type_colors = ["#E63946", "#457B9D", "#2A9D8F", "#CCCCCC"]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    bottom = np.zeros(len(conds))

    for rtype, color in zip(types, type_colors):
        proportions = []
        for cond in conds:
            subset = plot_df[plot_df["condition_identifiability"] == cond]
            pct = (subset["reasoning_type"] == rtype).mean() * 100
            proportions.append(pct)
        ax.bar(range(len(conds)), proportions, bottom=bottom, color=color,
               label=rtype.title(), edgecolor="white", width=0.5)
        bottom += proportions

    ax.set_xticks(range(len(conds)))
    ax.set_xticklabels([c.title() for c in conds])
    ax.set_ylabel("Proportion (%)")
    ax.set_ylim(0, 105)
    ax.set_title("Reasoning Type Distribution")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save_figure(fig, "ling_reasoning_types")


def plot_emotion_logic_scatter(df):
    """Scatter: emotion-vs-logic ratio vs donation."""
    set_paper_style()

    plot_df = df.dropna(subset=["emotion_vs_logic_ratio", "donation_amount"]).copy()
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 5))

    for cond, color in [("statistical", PALETTE["statistical"]),
                         ("identifiable", PALETTE["identifiable"])]:
        sub = plot_df[plot_df["condition_identifiability"] == cond]
        if sub.empty:
            continue
        # Clip extreme values for visualization
        x = sub["emotion_vs_logic_ratio"].clip(upper=50)
        ax.scatter(x, sub["donation_amount"], alpha=0.3, s=20, color=color, label=cond.title())

    ax.set_xlabel("Emotion-to-Logic Ratio")
    ax.set_ylabel("Donation ($)")
    ax.set_title("Linguistic Markers vs. Donation Behavior")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "ling_emotion_logic_scatter")


def plot_feature_correlation(df):
    """Heatmap: correlation of linguistic features with DV."""
    set_paper_style()

    cols = [
        "donation_amount", "feelings_composite",
        "sympathy_density", "utilitarian_density", "hedging_density",
        "sentiment_polarity", "sentiment_subjectivity",
        "emotion_vs_logic_ratio",
    ]
    available = [c for c in cols if c in df.columns]
    plot_df = df[available].dropna()

    if plot_df.empty or len(available) < 3:
        return

    corr = plot_df.corr()

    fig, ax = plt.subplots(figsize=(8, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr, mask=mask, cmap="RdBu_r", vmin=-1, vmax=1,
        annot=True, fmt=".2f", linewidths=0.5, ax=ax,
        annot_kws={"fontsize": 9},
    )
    ax.set_title("Feature Correlation Matrix")
    fig.tight_layout()
    save_figure(fig, "ling_correlation_heatmap")


def plot_linguistic_all(df):
    plot_sympathy_density(df)
    plot_reasoning_type_distribution(df)
    plot_emotion_logic_scatter(df)
    plot_feature_correlation(df)
