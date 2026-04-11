"""
Experiment 5 Plots — Processing Mode Priming
==============================================
1. Grouped bar chart (identifiability × prime)
2. Interaction plot
"""

import matplotlib.pyplot as plt
import numpy as np
from visualization.style import set_paper_style, save_figure, PALETTE


def plot_exp5_grouped_bars(df, stats_results):
    """Grouped bar: identifiability × prime."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(6, 5))
    conditions = ["statistical", "identifiable"]
    primes = ["calculate", "feel"]
    prime_labels = ["Calculation Prime", "Feeling Prime"]
    colors = [PALETTE["calculate"], PALETTE["feel"]]

    x = np.arange(len(conditions))
    width = 0.35

    for i, (prime, label, color) in enumerate(zip(primes, prime_labels, colors)):
        means, sems = [], []
        for cond in conditions:
            cell = df[
                (df["condition_identifiability"] == cond) &
                (df["condition_prime"] == prime)
            ]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else 0)
            sems.append(cell.sem() if len(cell) > 1 else 0)
        ax.bar(x + i * width - width / 2, means, width, yerr=sems,
               color=color, label=label, edgecolor="white", capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels(["Statistical", "Identifiable"])
    ax.set_ylabel("Mean Donation ($)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Processing Mode Priming Effect")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "exp5_grouped_bars")


def plot_exp5_interaction(df, stats_results):
    """Interaction plot: lines for prime across identifiability."""
    set_paper_style()

    fig, ax = plt.subplots(figsize=(5, 4.5))

    for prime, ls, color, label in [
        ("calculate", "-", PALETTE["calculate"], "Calculation"),
        ("feel", "--", PALETTE["feel"], "Feeling"),
    ]:
        means = []
        for cond in ["statistical", "identifiable"]:
            cell = df[
                (df["condition_identifiability"] == cond) &
                (df["condition_prime"] == prime)
            ]["donation_amount"].dropna()
            means.append(cell.mean() if len(cell) > 0 else 0)
        ax.plot(["Statistical", "Identifiable"], means, ls, color=color,
                marker="o", label=label, linewidth=2.5, markersize=10)

    ax.set_ylabel("Mean Donation ($)")
    ax.set_ylim(0, 5.5)
    ax.set_title("Interaction: Identifiability × Prime")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "exp5_interaction")


def plot_exp5_all(df, stats_results):
    plot_exp5_grouped_bars(df, stats_results)
    plot_exp5_interaction(df, stats_results)
