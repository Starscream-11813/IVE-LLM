"""
Experiment 10 Visualizations — In-group / Out-group (AI Fairness)
=================================================================
  1. Grouped bar (cultural distance × identifiability)
  2. IVE magnitude bar chart
  3. Emotion heatmap across cultural conditions
  4. Fairness radar chart (per model)
  5. Parity analysis bar chart
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from visualization.style import (
    set_paper_style, save_figure, PALETTE, MODEL_COLORS,
)

DISTANCES = ["near", "middle", "far"]
DISTANCE_LABELS = ["Near\n(US)", "Middle\n(Moldova)", "Far\n(Mali)"]


# ═══════════════════════════════════════════════════════════════════════════════
#  1. GROUPED BAR — Cultural distance × Identifiability
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp10_cultural_ive(df, stats_results=None):
    set_paper_style()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.arange(len(DISTANCES))
    width = 0.35

    # Panel 1: raw donations
    ax = axes[0]
    for ident, offset, color, label in [
        ("identifiable", -width / 2, PALETTE["identifiable"], "Identifiable"),
        ("statistical", width / 2, PALETTE["statistical"], "Statistical"),
    ]:
        means, sems = [], []
        for dist in DISTANCES:
            subset = df[(df["cultural_distance"] == dist) &
                        (df["condition_identifiability"] == ident)]
            means.append(subset["donation_amount"].mean() if len(subset) else 0)
            sems.append(subset["donation_amount"].sem() if len(subset) > 1 else 0)
        ax.bar(x + offset, means, width, yerr=sems, capsize=3, color=color,
               label=label, edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(DISTANCE_LABELS)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Cultural Distance × Identifiability")
    ax.legend()
    ax.set_ylim(0, 5.5)

    # Panel 2: IVE magnitude
    ax = axes[1]
    ive_vals, ive_errs = [], []
    for dist in DISTANCES:
        ident = df[(df["cultural_distance"] == dist) &
                   (df["condition_identifiability"] == "identifiable")]["donation_amount"]
        stat = df[(df["cultural_distance"] == dist) &
                  (df["condition_identifiability"] == "statistical")]["donation_amount"]
        ive = ident.mean() - stat.mean() if len(ident) and len(stat) else 0

        # Bootstrap CI
        diffs = []
        rng = np.random.RandomState(42)
        for _ in range(1000):
            bi = rng.choice(ident.values, size=len(ident), replace=True) if len(ident) else np.array([0])
            bs = rng.choice(stat.values, size=len(stat), replace=True) if len(stat) else np.array([0])
            diffs.append(bi.mean() - bs.mean())
        ci_lo = np.percentile(diffs, 2.5) if diffs else 0
        ci_hi = np.percentile(diffs, 97.5) if diffs else 0

        ive_vals.append(ive)
        ive_errs.append((ive - ci_lo, ci_hi - ive))

    colors = [PALETTE["identifiable"] if v > 0 else PALETTE["statistical"]
              for v in ive_vals]
    ax.bar(x, ive_vals, 0.5, yerr=np.array(ive_errs).T, capsize=4,
           color=colors, edgecolor="white", linewidth=0.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(DISTANCE_LABELS)
    ax.set_ylabel("IVE Magnitude\n(Identifiable − Statistical)")
    ax.set_title("Identifiable Victim Effect by Cultural Distance")

    plt.tight_layout()
    save_figure(fig, "fig_exp10_cultural_ive")


# ═══════════════════════════════════════════════════════════════════════════════
#  2. FAIRNESS RADAR CHART
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp10_fairness_radar(df, stats_results=None):
    set_paper_style()

    models = sorted(df["model_key"].unique())
    n_models = len(models)
    cols = min(4, n_models)
    rows = (n_models + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows),
                              subplot_kw=dict(polar=True))
    if n_models == 1:
        axes = np.array([axes])
    axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

    categories = DISTANCE_LABELS
    n_cat = len(categories)
    angles = np.linspace(0, 2 * np.pi, n_cat, endpoint=False).tolist()
    angles += angles[:1]

    for i, model in enumerate(models):
        if i >= len(axes_flat):
            break
        ax = axes_flat[i]
        mdf = df[(df["model_key"] == model) &
                 (df["condition_identifiability"] == "identifiable")]
        vals = []
        for dist in DISTANCES:
            subset = mdf[mdf["cultural_distance"] == dist]
            vals.append(subset["donation_amount"].mean() if len(subset) else 0)
        vals += vals[:1]

        ax.plot(angles, vals, "o-", linewidth=2,
                color=MODEL_COLORS.get(model, "gray"))
        ax.fill(angles, vals, alpha=0.15,
                color=MODEL_COLORS.get(model, "gray"))
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=8)
        ax.set_ylim(0, 5.5)
        ax.set_title(model, fontsize=10, pad=15)

    # Hide unused axes
    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].set_visible(False)

    fig.suptitle("Fairness Radar: Donations to Identified Victims by Culture",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    save_figure(fig, "fig_exp10_fairness_radar")


# ═══════════════════════════════════════════════════════════════════════════════
#  3. PARITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp10_parity(df, stats_results=None):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(8, 5))

    ident_df = df[df["condition_identifiability"] == "identifiable"]
    means = ident_df.groupby("cultural_distance")["donation_amount"].mean()
    means = means.reindex(DISTANCES)
    overall_mean = ident_df["donation_amount"].mean()

    x = np.arange(len(DISTANCES))
    colors_cond = ["#2A9D8F", "#E9C46A", "#E76F51"]
    ax.bar(x, means.values, 0.5, color=colors_cond,
           edgecolor="white", linewidth=0.5)
    ax.axhline(overall_mean, color="black", linestyle="--", alpha=0.7,
               label=f"Overall mean: ${overall_mean:.2f}")

    for i, (val, dist) in enumerate(zip(means.values, DISTANCES)):
        pct = ((val - overall_mean) / overall_mean * 100) if overall_mean else 0
        ax.text(i, val + 0.1, f"{pct:+.1f}%", ha="center", fontsize=10,
                fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(DISTANCE_LABELS)
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Cultural Parity: Donations to Identified Victims")
    ax.set_ylim(0, 5.5)
    ax.legend()
    plt.tight_layout()
    save_figure(fig, "fig_exp10_parity")


# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp10_all(df, stats_results=None):
    plot_exp10_cultural_ive(df, stats_results)
    plot_exp10_fairness_radar(df, stats_results)
    plot_exp10_parity(df, stats_results)
