"""
Experiment 3 Plots — Framing the Intervention
===============================================
1. Grouped bar chart (identifiability × frame)
2. Difference plot (IVE effect per frame)
"""

import matplotlib.pyplot as plt
import numpy as np
from visualization.style import set_paper_style, save_figure, PALETTE, format_pvalue


def plot_exp3_grouped_bars(df, stats_results):
    """Grouped bars: identifiability × frame."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(8, 5))
    conditions = ["statistical", "identifiable"]
    frames = ["frame_more", "frame_less", "frame_normative"]
    frame_labels = ["More to\nIdentifiable", "Less to\nStatistical", "Normative"]
    colors = [PALETTE["frame_more"], PALETTE["frame_less"], PALETTE["frame_normative"]]

    x = np.arange(len(conditions))
    width = 0.25

    for i, (frame, label, color) in enumerate(zip(frames, frame_labels, colors)):
        means, sems = [], []
        for cond in conditions:
            cell = df[
                (df["condition_identifiability"] == cond) &
                (df["condition_intervention"] == frame)
            ]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else 0)
            sems.append(cell.sem() if len(cell) > 1 else 0)
        ax.bar(x + i * width - width, means, width, yerr=sems,
               color=color, label=label, edgecolor="white", capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels(["Statistical", "Identifiable"])
    ax.set_ylabel("Mean Donation ($)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Effect of Intervention Frame on Donations")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "exp3_grouped_bars")


def plot_exp3_ive_difference(df, stats_results):
    """Horizontal bar: IVE effect (Cohen's d) per frame."""
    set_paper_style()

    frames = ["frame_more", "frame_less", "frame_normative"]
    frame_labels = ["More Identifiable", "Less Statistical", "Normative"]
    colors = [PALETTE["frame_more"], PALETTE["frame_less"], PALETTE["frame_normative"]]

    effects = []
    for frame in frames:
        d = stats_results.get(f"ive_effect_{frame}", 0.0)
        effects.append(d if d is not None else 0.0)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    y = range(len(frames))
    ax.barh(y, effects, color=colors, edgecolor="white", height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(frame_labels)
    ax.set_xlabel("IVE Effect Size (Cohen's d)")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("IVE Effect by Intervention Frame")

    for i, val in enumerate(effects):
        ax.text(val + 0.02 if val >= 0 else val - 0.02, i,
                f"{val:.2f}", va="center", fontsize=10,
                ha="left" if val >= 0 else "right")

    fig.tight_layout()
    save_figure(fig, "exp3_ive_difference")


def plot_exp3_all(df, stats_results):
    plot_exp3_grouped_bars(df, stats_results)
    plot_exp3_ive_difference(df, stats_results)
