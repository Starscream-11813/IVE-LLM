"""
Emotion & Mediation Cross-Experiment Visualizations
====================================================
  1. Distress vs empathy scatter (all extended experiments)
  2. Mediation forest plot
  3. Correlation matrix heatmap
  4. Ridgeline plot for distress distributions
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from visualization.style import set_paper_style, save_figure, PALETTE


# ═══════════════════════════════════════════════════════════════════════════════
#  1. DISTRESS vs EMPATHY SCATTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_distress_vs_empathy_scatter(df):
    set_paper_style()
    if "distress_composite" not in df.columns or "empathy_composite" not in df.columns:
        return

    clean = df.dropna(subset=["distress_composite", "empathy_composite"])
    if clean.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 6))

    # Color by a classification if available
    if "singularity" in clean.columns and "identification_level" in clean.columns:
        clean["cond_label"] = clean["singularity"] + "_" + clean["identification_level"]
        palette = {
            "single_full": PALETTE["identifiable"],
            "single_unidentified": PALETTE["statistical"],
            "group_full": PALETTE["combined"],
            "group_unidentified": PALETTE["no_intervention"],
        }
        for label, color in palette.items():
            sub = clean[clean["cond_label"] == label]
            if sub.empty:
                continue
            sizes = sub["donation_amount"].fillna(2.5) * 15 + 10
            ax.scatter(sub["distress_composite"], sub["empathy_composite"],
                       c=color, s=sizes, alpha=0.5, label=label.replace("_", " "),
                       edgecolors="white", linewidth=0.3)
    else:
        sizes = clean["donation_amount"].fillna(2.5) * 15 + 10
        ax.scatter(clean["distress_composite"], clean["empathy_composite"],
                   c=PALETTE["identifiable"], s=sizes, alpha=0.4,
                   edgecolors="white", linewidth=0.3)

    lims = [min(ax.get_xlim()[0], ax.get_ylim()[0]),
            max(ax.get_xlim()[1], ax.get_ylim()[1])]
    ax.plot(lims, lims, "k--", alpha=0.3, label="Equality line")
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    ax.set_xlabel("Distress Composite (1-7)")
    ax.set_ylabel("Empathic Concern Composite (1-7)")
    ax.set_title("Distress vs. Empathic Concern\nAcross Experimental Conditions")
    ax.legend(fontsize=8, loc="lower right")
    plt.tight_layout()
    save_figure(fig, "fig_distress_vs_empathy")


# ═══════════════════════════════════════════════════════════════════════════════
#  2. MEDIATION FOREST PLOT
# ═══════════════════════════════════════════════════════════════════════════════

def plot_mediation_forest(mediation_results):
    """
    mediation_results: dict mapping label → MediationResult-like dict
    with keys: indirect_effect, indirect_ci_lower, indirect_ci_upper
    """
    set_paper_style()
    if not mediation_results:
        return

    labels = list(mediation_results.keys())
    effects = [r["indirect_effect"] for r in mediation_results.values()]
    ci_lower = [r["indirect_ci_lower"] for r in mediation_results.values()]
    ci_upper = [r["indirect_ci_upper"] for r in mediation_results.values()]

    fig, ax = plt.subplots(figsize=(8, max(4, len(labels) * 0.4)))
    y = np.arange(len(labels))

    for i in range(len(labels)):
        color = PALETTE["identifiable"] if effects[i] > 0 else PALETTE["statistical"]
        ax.errorbar(effects[i], i,
                     xerr=[[effects[i] - ci_lower[i]], [ci_upper[i] - effects[i]]],
                     fmt="o", color=color, capsize=4, markersize=8)

    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Indirect Effect (a × b)")
    ax.set_title("Mediation Forest Plot: Indirect Effects Across Conditions")
    ax.invert_yaxis()
    plt.tight_layout()
    save_figure(fig, "fig_mediation_forest")


# ═══════════════════════════════════════════════════════════════════════════════
#  3. CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

def plot_emotion_correlation_matrix(df):
    set_paper_style()
    emotion_cols = [
        "rating_worried", "rating_upset", "rating_sad",
        "rating_disturbed", "rating_troubled",
        "rating_sympathy_7", "rating_compassion", "rating_tender",
        "rating_moved", "rating_softhearted",
    ]
    present = [c for c in emotion_cols if c in df.columns]
    if len(present) < 5:
        return

    # Add donation
    cols = present + ["donation_amount"]
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Emotion Rating Correlation Matrix")
    plt.tight_layout()
    save_figure(fig, "fig_emotion_correlation_matrix")


# ═══════════════════════════════════════════════════════════════════════════════
#  4. RIDGELINE PLOT — Distress Distributions
# ═══════════════════════════════════════════════════════════════════════════════

def plot_distress_ridgeline(df):
    set_paper_style()
    if "distress_composite" not in df.columns:
        return

    # Create condition label
    if "singularity" in df.columns and "identification_level" in df.columns:
        df = df.copy()
        df["cond"] = df["singularity"] + "_" + df["identification_level"]
        order = [
            "single_unidentified", "single_age", "single_age_name", "single_full",
            "group_unidentified", "group_age", "group_age_name", "group_full",
        ]
        order = [o for o in order if o in df["cond"].unique()]
    else:
        return

    n = len(order)
    fig, axes = plt.subplots(n, 1, figsize=(8, n * 0.8), sharex=True)
    if n == 1:
        axes = [axes]

    palette = sns.color_palette("viridis", n)
    for i, (cond, ax) in enumerate(zip(order, axes)):
        subset = df[df["cond"] == cond]["distress_composite"].dropna()
        if len(subset) < 2:
            ax.set_visible(False)
            continue
        ax.fill_between(
            *_kde(subset), alpha=0.6, color=palette[i],
        )
        ax.set_yticks([])
        ax.set_ylabel(cond.replace("_", "\n"), fontsize=7, rotation=0,
                      ha="right", va="center")
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i < n - 1:
            ax.spines["bottom"].set_visible(False)
            ax.tick_params(axis="x", length=0)

    axes[-1].set_xlabel("Distress Composite (1-7)")
    fig.suptitle("Distress Distributions by Condition", fontsize=13, y=1.01)
    plt.tight_layout()
    save_figure(fig, "fig_distress_ridgeline")


def _kde(data, n_points=200):
    """Simple KDE for ridgeline plots."""
    from scipy.stats import gaussian_kde
    data = np.array(data)
    if len(data) < 2:
        return np.array([0]), np.array([0])
    kde = gaussian_kde(data, bw_method=0.3)
    x = np.linspace(max(1, data.min() - 0.5), min(7, data.max() + 0.5), n_points)
    return x, kde(x)


# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_emotion_mediation_all(df, mediation_results=None):
    plot_distress_vs_empathy_scatter(df)
    if mediation_results:
        plot_mediation_forest(mediation_results)
    plot_emotion_correlation_matrix(df)
    plot_distress_ridgeline(df)
