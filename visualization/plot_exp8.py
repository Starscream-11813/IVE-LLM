"""
Experiment 8 Visualizations — Singularity × Identification Interaction
=======================================================================
Core figures for the Kogut & Ritov replication:
  1. Grouped bar chart (singularity × identification interaction)
  2. Triple panel (donation / distress / empathy)
  3. Mediation path diagrams
  4. Victim invariance bar chart
  5. Emotion heatmap
  6. Quantity neglect chart
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from visualization.style import (
    set_paper_style, save_figure, PALETTE, add_significance_bracket,
)

LEVEL_ORDER = ["unidentified", "age", "age_name", "full"]
LEVEL_LABELS = ["Unidentified", "Age", "Age + Name", "Full Description"]


def _summarize(df, dv, groupby_cols):
    return df.groupby(groupby_cols).agg(
        mean_val=(dv, "mean"), sem_val=(dv, "sem"), n=(dv, "count"),
    ).reset_index()


# ═══════════════════════════════════════════════════════════════════════════════
#  1. CORE INTERACTION GROUPED BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_core_interaction(df, stats_results=None):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(8, 5))

    summary = _summarize(df, "donation_amount", ["singularity", "identification_level"])
    summary["identification_level"] = pd.Categorical(
        summary["identification_level"], categories=LEVEL_ORDER, ordered=True,
    )
    summary = summary.sort_values("identification_level")

    x = np.arange(len(LEVEL_ORDER))
    width = 0.35
    single = summary[summary["singularity"] == "single"]
    group = summary[summary["singularity"] == "group"]

    ax.bar(x - width / 2, single["mean_val"], width, yerr=single["sem_val"],
           capsize=3, label="Single victim", color=PALETTE["identifiable"],
           edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2, group["mean_val"], width, yerr=group["sem_val"],
           capsize=3, label="Group of 8", color=PALETTE["statistical"],
           edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Level of Identification")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Singularity × Identification Interaction")
    ax.set_xticks(x)
    ax.set_xticklabels(LEVEL_LABELS)
    ax.legend()
    ax.set_ylim(0, 5.5)
    plt.tight_layout()
    save_figure(fig, "fig_exp8_core_interaction")


# ═══════════════════════════════════════════════════════════════════════════════
#  2. TRIPLE PANEL — Donation / Distress / Empathy
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_triple_panel(df, stats_results=None):
    set_paper_style()
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)

    dvs = [
        ("donation_amount", "Mean Donation ($)", "Donation"),
        ("distress_composite", "Mean Distress (1-7)", "Distress"),
        ("empathy_composite", "Mean Empathic Concern (1-7)", "Empathic Concern"),
    ]
    x = np.arange(len(LEVEL_ORDER))
    width = 0.35

    for ax, (dv, ylabel, title) in zip(axes, dvs):
        if dv not in df.columns:
            ax.set_visible(False)
            continue
        summary = _summarize(df, dv, ["singularity", "identification_level"])
        summary["identification_level"] = pd.Categorical(
            summary["identification_level"], categories=LEVEL_ORDER, ordered=True,
        )
        summary = summary.sort_values("identification_level")
        single = summary[summary["singularity"] == "single"]
        group = summary[summary["singularity"] == "group"]

        ax.bar(x - width / 2, single["mean_val"], width, yerr=single["sem_val"],
               capsize=3, color=PALETTE["identifiable"], label="Single",
               edgecolor="white", linewidth=0.5)
        ax.bar(x + width / 2, group["mean_val"], width, yerr=group["sem_val"],
               capsize=3, color=PALETTE["statistical"], label="Group of 8",
               edgecolor="white", linewidth=0.5)

        ax.set_xlabel("Identification Level")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(["None", "Age", "+Name", "+Full"], fontsize=9)
        if ax == axes[0]:
            ax.legend(loc="upper left")

    plt.tight_layout()
    save_figure(fig, "fig_exp8_triple_panel")


# ═══════════════════════════════════════════════════════════════════════════════
#  3. MEDIATION PATH DIAGRAMS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_mediation_diagram(stats_results=None):
    set_paper_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, cond_label in zip(axes, ["Single Victim", "Group of 8"]):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(cond_label, fontsize=14, fontweight="bold")

        # IV box
        iv = mpatches.FancyBboxPatch(
            (0.5, 5.5), 3, 1.5, boxstyle="round,pad=0.2",
            facecolor="#D4E6F1", edgecolor="black",
        )
        ax.add_patch(iv)
        ax.text(2, 6.25, "Identification\n(Unid. vs Full)",
                ha="center", va="center", fontsize=9)

        # Mediator box
        med = mpatches.FancyBboxPatch(
            (6, 5.5), 3, 1.5, boxstyle="round,pad=0.2",
            facecolor="#FEF9E7", edgecolor="black",
        )
        ax.add_patch(med)
        ax.text(7.5, 6.25, "Distress", ha="center", va="center", fontsize=9)

        # DV box
        dv = mpatches.FancyBboxPatch(
            (3.25, 1), 3, 1.5, boxstyle="round,pad=0.2",
            facecolor="#D5F5E3", edgecolor="black",
        )
        ax.add_patch(dv)
        ax.text(4.75, 1.75, "Donation", ha="center", va="center", fontsize=9)

        # Arrows
        ax.annotate("", xy=(6, 6.25), xytext=(3.5, 6.25),
                     arrowprops=dict(arrowstyle="->", lw=2))
        ax.text(4.75, 6.7, "a = ?.??*", ha="center", fontsize=9)

        ax.annotate("", xy=(5.5, 2.5), xytext=(7, 5.5),
                     arrowprops=dict(arrowstyle="->", lw=2))
        ax.text(7, 4, "b = ?.??*", ha="center", fontsize=9)

        ax.annotate("", xy=(4, 2.5), xytext=(2.5, 5.5),
                     arrowprops=dict(arrowstyle="->", lw=2, linestyle="dashed"))
        ax.text(2, 4, "c' = ?.??\n(n.s.)", ha="center", fontsize=9,
                style="italic")

    plt.tight_layout()
    save_figure(fig, "fig_exp8_mediation_diagrams")


# ═══════════════════════════════════════════════════════════════════════════════
#  4. VICTIM INVARIANCE
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_victim_invariance(df):
    set_paper_style()
    single_full = df[
        (df["singularity"] == "single") & (df["identification_level"] == "full")
    ]
    if "victim_name" not in single_full.columns or single_full.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    summary = single_full.groupby("victim_name").agg(
        mean_donation=("donation_amount", "mean"),
        sem_donation=("donation_amount", "sem"),
    ).reset_index().sort_values("mean_donation", ascending=False)

    colors = sns.color_palette("Set2", len(summary))
    ax.bar(range(len(summary)), summary["mean_donation"],
           yerr=summary["sem_donation"], capsize=4, color=colors,
           edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(len(summary)))
    ax.set_xticklabels(summary["victim_name"], rotation=45, ha="right")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Donation by Individual Victim Profile\n(Testing Invariance)")
    ax.set_ylim(0, 5.5)

    grand_mean = single_full["donation_amount"].mean()
    ax.axhline(grand_mean, color="gray", linestyle="--", alpha=0.7,
               label=f"Grand mean: ${grand_mean:.2f}")
    ax.legend()
    plt.tight_layout()
    save_figure(fig, "fig_exp8_victim_invariance")


# ═══════════════════════════════════════════════════════════════════════════════
#  5. EMOTION HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_emotion_heatmap(df):
    set_paper_style()
    distress_cols = ["rating_worried", "rating_upset", "rating_sad",
                     "rating_disturbed", "rating_troubled"]
    empathy_cols = ["rating_sympathy_7", "rating_compassion", "rating_tender",
                    "rating_moved", "rating_softhearted"]
    all_cols = distress_cols + empathy_cols
    present = [c for c in all_cols if c in df.columns]
    if len(present) < 4:
        return

    df["condition_label"] = df["singularity"] + "_" + df["identification_level"]
    row_order = [
        "single_unidentified", "single_age", "single_age_name", "single_full",
        "group_unidentified", "group_age", "group_age_name", "group_full",
    ]
    pivot = df.groupby("condition_label")[present].mean()
    pivot = pivot.reindex([r for r in row_order if r in pivot.index])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.5, ax=ax, vmin=1, vmax=7)
    ax.set_title("Emotion Ratings by Condition")
    ax.set_xlabel("Rating Item")
    ax.set_ylabel("Condition")
    plt.tight_layout()
    save_figure(fig, "fig_exp8_emotion_heatmap")


# ═══════════════════════════════════════════════════════════════════════════════
#  6. QUANTITY NEGLECT
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_quantity_neglect(df):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(8, 5))

    summary = _summarize(df, "donation_amount", ["singularity", "identification_level"])
    summary["identification_level"] = pd.Categorical(
        summary["identification_level"], categories=LEVEL_ORDER, ordered=True,
    )
    summary = summary.sort_values("identification_level")

    x = np.arange(len(LEVEL_ORDER))
    width = 0.35
    single = summary[summary["singularity"] == "single"]
    group = summary[summary["singularity"] == "group"]

    ax.bar(x - width / 2, single["mean_val"], width, yerr=single["sem_val"],
           capsize=3, label="Single (1 child)", color=PALETTE["identifiable"],
           edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2, group["mean_val"], width, yerr=group["sem_val"],
           capsize=3, label="Group (8 children)", color=PALETTE["statistical"],
           edgecolor="white", linewidth=0.5)

    ax.axhline(2.5, color="gray", linestyle=":", alpha=0.5,
               label="Rational parity line")
    ax.set_xlabel("Identification Level")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Quantity Neglect: 1 Child vs 8 Children")
    ax.set_xticks(x)
    ax.set_xticklabels(LEVEL_LABELS)
    ax.legend(loc="upper left")
    ax.set_ylim(0, 5.5)
    plt.tight_layout()
    save_figure(fig, "fig_exp8_quantity_neglect")


# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp8_all(df, stats_results=None):
    plot_exp8_core_interaction(df, stats_results)
    plot_exp8_triple_panel(df, stats_results)
    plot_exp8_mediation_diagram(stats_results)
    plot_exp8_victim_invariance(df)
    plot_exp8_emotion_heatmap(df)
    plot_exp8_quantity_neglect(df)
