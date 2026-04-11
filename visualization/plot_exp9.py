"""
Experiment 9 Visualizations — Identification Gradient (Dose-Response)
=====================================================================
  1. Dose-response curve (one line per model)
  2. Dual dose-response (donation + distress)
  3. Step-size bar chart (pairwise increments)
  4. Model threshold scatter
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats as sp_stats
from visualization.style import (
    set_paper_style, save_figure, MODEL_COLORS, format_pvalue_text,
)

LEVEL_ORDER = [
    "bare", "age", "age_gender", "age_gender_name",
    "age_gender_name_location", "full_narrative",
]
LEVEL_LABELS = [
    "Bare\n(a child)", "Age\n(7 yr old)", "Age+\nGender",
    "Age+Gender\n+Name", "+Name\n+Location", "Full\nNarrative",
]
LEVEL_NUMERIC = list(range(1, 7))


# ═══════════════════════════════════════════════════════════════════════════════
#  1. DOSE-RESPONSE CURVE
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp9_dose_response(df, stats_results=None):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(9, 5))

    for model in sorted(df["model_key"].unique()):
        mdf = df[df["model_key"] == model]
        summary = mdf.groupby("identification_level").agg(
            mean=("donation_amount", "mean"),
            sem=("donation_amount", "sem"),
        )
        summary = summary.reindex(LEVEL_ORDER)
        color = MODEL_COLORS.get(model, "gray")
        ax.errorbar(LEVEL_NUMERIC, summary["mean"], yerr=summary["sem"],
                     marker="o", capsize=3, label=model, color=color,
                     linewidth=2, markersize=6)

    ax.set_xticks(LEVEL_NUMERIC)
    ax.set_xticklabels(LEVEL_LABELS, fontsize=8)
    ax.set_xlabel("Level of Identification")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Dose-Response: Identification Level and Generosity")
    ax.legend(loc="upper left", fontsize=7, ncol=2)
    ax.set_ylim(0, 5.5)
    plt.tight_layout()
    save_figure(fig, "fig_exp9_dose_response")


# ═══════════════════════════════════════════════════════════════════════════════
#  2. DUAL DOSE-RESPONSE (Donation + Distress)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp9_dual_dose_response(df, stats_results=None):
    set_paper_style()
    fig, ax1 = plt.subplots(figsize=(9, 5))

    summary_don = df.groupby("identification_level")["donation_amount"].agg(
        ["mean", "sem"]
    ).reindex(LEVEL_ORDER)

    ax1.errorbar(LEVEL_NUMERIC, summary_don["mean"], yerr=summary_don["sem"],
                  marker="s", capsize=3, color="#E63946", linewidth=2,
                  label="Donation ($)")
    ax1.set_ylabel("Mean Donation ($)", color="#E63946")
    ax1.set_ylim(0, 5.5)
    ax1.tick_params(axis="y", labelcolor="#E63946")

    if "distress_composite" in df.columns:
        ax2 = ax1.twinx()
        summary_dis = df.groupby("identification_level")["distress_composite"].agg(
            ["mean", "sem"]
        ).reindex(LEVEL_ORDER)
        ax2.errorbar(LEVEL_NUMERIC, summary_dis["mean"], yerr=summary_dis["sem"],
                      marker="^", capsize=3, color="#457B9D", linewidth=2,
                      linestyle="--", label="Distress (1-7)")
        ax2.set_ylabel("Mean Distress Composite (1-7)", color="#457B9D")
        ax2.set_ylim(1, 7.5)
        ax2.tick_params(axis="y", labelcolor="#457B9D")

    ax1.set_xticks(LEVEL_NUMERIC)
    ax1.set_xticklabels(LEVEL_LABELS, fontsize=8)
    ax1.set_xlabel("Level of Identification")
    ax1.set_title("Identification Gradient: Donation and Distress")

    lines1, labels1 = ax1.get_legend_handles_labels()
    if "distress_composite" in df.columns:
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    else:
        ax1.legend(loc="upper left")

    plt.tight_layout()
    save_figure(fig, "fig_exp9_dual_dose_response")


# ═══════════════════════════════════════════════════════════════════════════════
#  3. STEP-SIZE BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp9_step_sizes(df, stats_results=None):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(8, 5))

    summary = df.groupby("identification_level")["donation_amount"].mean()
    summary = summary.reindex(LEVEL_ORDER)

    pairs = list(zip(LEVEL_ORDER[:-1], LEVEL_ORDER[1:]))
    deltas = [summary[b] - summary[a] for a, b in pairs]
    pair_labels = [f"{a[:4]}→\n{b[:4]}" for a, b in pairs]
    x = np.arange(len(pairs))

    colors = ["#2A9D8F" if d > 0 else "#E76F51" for d in deltas]
    ax.bar(x, deltas, color=colors, edgecolor="white", linewidth=0.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(pair_labels, fontsize=8)
    ax.set_ylabel("Δ Mean Donation ($)")
    ax.set_title("Marginal Increase at Each Identification Step")
    plt.tight_layout()
    save_figure(fig, "fig_exp9_step_sizes")


# ═══════════════════════════════════════════════════════════════════════════════
#  4. MODEL THRESHOLD SCATTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp9_threshold_comparison(df, stats_results=None):
    set_paper_style()
    fig, ax = plt.subplots(figsize=(8, 5))

    models = sorted(df["model_key"].unique())
    thresholds = []
    for model in models:
        mdf = df[df["model_key"] == model]
        summary = mdf.groupby("identification_level")["donation_amount"].mean()
        summary = summary.reindex(LEVEL_ORDER)
        # Find steepest step
        vals = summary.values
        best_step_idx = 0
        best_delta = 0
        for i in range(len(vals) - 1):
            d = vals[i + 1] - vals[i]
            if d > best_delta:
                best_delta = d
                best_step_idx = i + 1
        thresholds.append(best_step_idx + 1)  # 1-indexed

    colors = [MODEL_COLORS.get(m, "gray") for m in models]
    ax.barh(range(len(models)), thresholds, color=colors,
            edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=8)
    ax.set_xlabel("Identification Threshold Level")
    ax.set_xticks(LEVEL_NUMERIC)
    ax.set_xticklabels(["Bare", "Age", "+Gen", "+Name", "+Loc", "Full"],
                       fontsize=8)
    ax.set_title("Where Does Each Model 'See' a Person?")
    plt.tight_layout()
    save_figure(fig, "fig_exp9_threshold_comparison")


# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER
# ═══════════════════════════════════════════════════════════════════════════════

def plot_exp9_all(df, stats_results=None):
    plot_exp9_dose_response(df, stats_results)
    plot_exp9_dual_dose_response(df, stats_results)
    plot_exp9_step_sizes(df, stats_results)
    plot_exp9_threshold_comparison(df, stats_results)
