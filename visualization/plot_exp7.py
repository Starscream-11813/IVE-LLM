"""
Experiment 7 Plots — Psychophysical Numbing (NOVEL)
====================================================
1. Numbing curve: donation vs log(n_victims)
2. Feelings numbing curve
3. Dual panel: raw vs contextualized
4. Marginal sensitivity bar chart
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from visualization.style import set_paper_style, save_figure, MODEL_COLORS, PALETTE


def plot_exp7_numbing_curve(df, stats_results):
    """Donation vs log(n_victims) per model."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(8, 5))
    models = sorted(df["model_key"].unique())

    scales = sorted(df["n_victims"].dropna().unique())

    for model in models:
        mdf = df[df["model_key"] == model]
        means = []
        for n in scales:
            cell = mdf[mdf["n_victims"] == n]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else np.nan)

        color = MODEL_COLORS.get(model, "#333333")
        ax.plot(scales, means, "o-", color=color, label=model,
                linewidth=2, markersize=7)

    ax.set_xscale("log")
    ax.set_xlabel("Number of Victims (log scale)")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Psychophysical Numbing: Donations vs. Victim Count")
    ax.legend()

    # Add log fit line (pooled)
    reg = stats_results.get("regression", {}).get("log_fit", {})
    if reg:
        r2 = reg.get("r_squared", 0)
        ax.text(0.02, 0.02, f"Pooled log-fit R² = {r2:.3f}",
                transform=ax.transAxes, fontsize=10,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    fig.tight_layout()
    save_figure(fig, "exp7_numbing_curve")


def plot_exp7_feelings_numbing(df, stats_results):
    """Feelings composite vs log(n_victims)."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(8, 5))
    models = sorted(df["model_key"].unique())
    scales = sorted(df["n_victims"].dropna().unique())

    for model in models:
        mdf = df[df["model_key"] == model]
        means = []
        for n in scales:
            cell = mdf[mdf["n_victims"] == n]["feelings_composite"].dropna()
            means.append(cell.mean() if len(cell) > 0 else np.nan)
        color = MODEL_COLORS.get(model, "#333333")
        ax.plot(scales, means, "s--", color=color, label=model,
                linewidth=2, markersize=7)

    ax.set_xscale("log")
    ax.set_xlabel("Number of Victims (log scale)")
    ax.set_ylabel("Feelings Composite (1–5)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Affective Numbing: Feelings vs. Victim Count")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "exp7_feelings_numbing")


def plot_exp7_contextualization(df, stats_results):
    """Dual panel: raw vs contextualized numbing."""
    set_paper_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    scales = sorted(df["n_victims"].dropna().unique())

    for ax, ctx, title in [
        (ax1, False, "Raw Numbers"),
        (ax2, True, "Contextualized"),
    ]:
        sub = df[df["contextualized"] == ctx]
        models = sorted(sub["model_key"].unique())
        for model in models:
            mdf = sub[sub["model_key"] == model]
            means = []
            for n in scales:
                cell = mdf[mdf["n_victims"] == n]["donation_amount"].dropna()
                means.append(cell.mean() if len(cell) > 0 else np.nan)
            color = MODEL_COLORS.get(model, "#333333")
            ax.plot(scales, means, "o-", color=color, label=model,
                    linewidth=2, markersize=6)
        ax.set_xscale("log")
        ax.set_xlabel("Number of Victims (log scale)")
        ax.set_title(title, fontweight="bold")
        ax.set_ylim(0, 5.5)
        ax.legend(fontsize=8)

    ax1.set_ylabel("Mean Donation ($)")
    fig.suptitle("Effect of Contextualization on Numbing", fontweight="bold", y=1.02)
    fig.tight_layout()
    save_figure(fig, "exp7_contextualization")


def plot_exp7_marginal_sensitivity(df, stats_results):
    """Bar chart: marginal sensitivity (slope) per model."""
    set_paper_style()

    models = sorted(df["model_key"].unique())
    slopes = []
    for model in models:
        mdf = df[df["model_key"] == model].dropna(subset=["donation_amount", "n_victims"])
        if len(mdf) > 3:
            log_v = np.log10(mdf["n_victims"].clip(lower=1))
            slope, _, _, _, _ = sp_stats.linregress(log_v, mdf["donation_amount"])
            slopes.append(slope)
        else:
            slopes.append(0)

    fig, ax = plt.subplots(figsize=(6, 4))
    colors = [MODEL_COLORS.get(m, "#333") for m in models]
    ax.bar(range(len(models)), slopes, color=colors, edgecolor="white", width=0.6)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=30, ha="right")
    ax.set_ylabel("Slope (donation per log₁₀ victims)")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Marginal Sensitivity to Victim Count")

    for i, val in enumerate(slopes):
        ax.text(i, val + 0.01 * (1 if val >= 0 else -1), f"{val:.3f}",
                ha="center", fontsize=9)

    fig.tight_layout()
    save_figure(fig, "exp7_marginal_sensitivity")


def plot_exp7_all(df, stats_results):
    plot_exp7_numbing_curve(df, stats_results)
    plot_exp7_feelings_numbing(df, stats_results)
    plot_exp7_contextualization(df, stats_results)
    plot_exp7_marginal_sensitivity(df, stats_results)
