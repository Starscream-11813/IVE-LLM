"""
Experiment 1 Plots — Basic IVE
================================
1. Main effect bar chart (mirroring Fig 1 in original paper)
2. Persona/framing effect facets
3. Violin + swarm plot of distributions
4. Feelings heatmap
5. Radar chart of affective profiles
6. Feelings-donation correlation scatter
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from visualization.style import (
    set_paper_style, save_figure, add_significance_bracket,
    PALETTE, MODEL_COLORS, IDENT_STAT_PALETTE, format_pvalue,
)


def plot_exp1_main_bars(df, stats_results):
    """Main effect bar chart: identifiable vs statistical per model."""
    set_paper_style()

    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()
    if core.empty:
        return

    models = sorted(core["model_key"].unique())
    n_models = len(models)

    fig, ax = plt.subplots(figsize=(max(6, n_models * 2.5), 5))

    x = np.arange(n_models)
    width = 0.35

    ident_means, stat_means = [], []
    ident_sems, stat_sems = [], []

    for model in models:
        mdf = core[core["model_key"] == model]
        ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
        stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
        ident_means.append(ident.mean() if len(ident) > 0 else 0)
        stat_means.append(stat.mean() if len(stat) > 0 else 0)
        ident_sems.append(ident.sem() if len(ident) > 1 else 0)
        stat_sems.append(stat.sem() if len(stat) > 1 else 0)

    bars1 = ax.bar(x - width / 2, stat_means, width, yerr=stat_sems,
                   color=PALETTE["statistical"], label="Statistical Victims",
                   edgecolor="white", linewidth=0.8, capsize=3)
    bars2 = ax.bar(x + width / 2, ident_means, width, yerr=ident_sems,
                   color=PALETTE["identifiable"], label="Identifiable Victim",
                   edgecolor="white", linewidth=0.8, capsize=3)

    # Significance brackets
    for i, model in enumerate(models):
        if model in stats_results.get("per_model", {}):
            p = stats_results["per_model"][model].get("t_p")
            if p is not None:
                y_max = max(ident_means[i] + ident_sems[i],
                            stat_means[i] + stat_sems[i])
                add_significance_bracket(ax, i - width / 2, i + width / 2,
                                         y_max + 0.15, p)

    ax.set_xlabel("Model")
    ax.set_ylabel("Mean Donation ($)")
    ax.set_title("Identifiable Victim Effect Across LLMs")
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("-", "\n") for m in models])
    ax.set_ylim(0, 5.5)
    ax.legend(loc="upper right")

    save_figure(fig, "exp1_main_bars")


def plot_exp1_violins(df):
    """Violin + swarm plot of donation distributions."""
    set_paper_style()

    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()
    if core.empty:
        return

    models = sorted(core["model_key"].unique())
    fig, axes = plt.subplots(1, len(models), figsize=(4 * len(models), 5),
                             sharey=True)
    if len(models) == 1:
        axes = [axes]

    for ax, model in zip(axes, models):
        mdf = core[core["model_key"] == model].dropna(subset=["donation_amount"])
        if mdf.empty:
            continue
        sns.violinplot(
            data=mdf, x="condition_identifiability", y="donation_amount",
            palette={"statistical": PALETTE["statistical"],
                     "identifiable": PALETTE["identifiable"]},
            order=["statistical", "identifiable"],
            inner=None, alpha=0.3, ax=ax,
        )
        sns.stripplot(
            data=mdf, x="condition_identifiability", y="donation_amount",
            palette={"statistical": PALETTE["statistical"],
                     "identifiable": PALETTE["identifiable"]},
            order=["statistical", "identifiable"],
            size=3, alpha=0.5, jitter=0.2, ax=ax,
        )
        ax.set_title(model)
        ax.set_xlabel("")
        ax.set_ylabel("Donation ($)" if ax == axes[0] else "")
        ax.set_ylim(-0.5, 5.5)

    fig.suptitle("Distribution of Donations by Condition", fontweight="bold", y=1.02)
    fig.tight_layout()
    save_figure(fig, "exp1_violins")


def plot_exp1_heatmap(df):
    """Heatmap: mean ratings by model × condition × rating item."""
    set_paper_style()

    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()
    if core.empty:
        return

    rating_cols = [
        "rating_upsetting", "rating_sympathetic",
        "rating_moral_responsibility", "rating_touched", "rating_appropriate",
    ]
    labels = ["Upsetting", "Sympathetic", "Moral Resp.", "Touched", "Appropriate"]

    models = sorted(core["model_key"].unique())
    conditions = ["statistical", "identifiable"]

    data = []
    row_labels = []
    for model in models:
        for cond in conditions:
            subset = core[
                (core["model_key"] == model) &
                (core["condition_identifiability"] == cond)
            ]
            means = [subset[c].mean() for c in rating_cols]
            data.append(means)
            row_labels.append(f"{model}\n({cond[:5]})")

    data_arr = np.array(data)
    fig, ax = plt.subplots(figsize=(8, max(4, len(row_labels) * 0.6)))
    im = ax.imshow(data_arr, cmap="YlOrRd", aspect="auto", vmin=1, vmax=5)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=9)

    # Annotate cells
    for i in range(len(row_labels)):
        for j in range(len(labels)):
            val = data_arr[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                        fontsize=9, color="white" if val > 3.5 else "black")

    fig.colorbar(im, ax=ax, shrink=0.7, label="Mean Rating (1-5)")
    ax.set_title("Affective Ratings by Model and Condition")
    fig.tight_layout()
    save_figure(fig, "exp1_heatmap")


def plot_exp1_radar(df):
    """Radar chart: affective profile per model."""
    set_paper_style()

    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()
    if core.empty:
        return

    rating_cols = [
        "rating_upsetting", "rating_sympathetic",
        "rating_moral_responsibility", "rating_touched", "rating_appropriate",
    ]
    labels = ["Upsetting", "Sympathetic", "Moral\nResp.", "Touched", "Appropriate"]

    models = sorted(core["model_key"].unique())
    n_cols = min(len(models), 4)
    n_rows = (len(models) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(4 * n_cols, 4 * n_rows),
                             subplot_kw=dict(polar=True))
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    flat_axes = axes.flatten()
    for idx, model in enumerate(models):
        ax = flat_axes[idx]
        for cond, color in [("statistical", PALETTE["statistical"]),
                             ("identifiable", PALETTE["identifiable"])]:
            subset = core[
                (core["model_key"] == model) &
                (core["condition_identifiability"] == cond)
            ]
            values = [subset[c].mean() for c in rating_cols]
            values += values[:1]
            ax.plot(angles, values, "o-", color=color, label=cond, linewidth=1.5)
            ax.fill(angles, values, color=color, alpha=0.15)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_ylim(0, 5)
        ax.set_title(model, pad=20, fontsize=11, fontweight="bold")
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8)

    # Hide unused axes
    for idx in range(len(models), len(flat_axes)):
        flat_axes[idx].set_visible(False)

    fig.suptitle("Affective Profile: Identifiable vs. Statistical", fontweight="bold", y=1.02)
    fig.tight_layout()
    save_figure(fig, "exp1_radar")


def plot_exp1_correlation(df):
    """Feelings-donation correlation scatter faceted by model."""
    set_paper_style()

    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].dropna(subset=["feelings_composite", "donation_amount"]).copy()
    if core.empty:
        return

    g = sns.FacetGrid(
        core, col="model_key", hue="condition_identifiability",
        palette={"identifiable": PALETTE["identifiable"],
                 "statistical": PALETTE["statistical"]},
        col_wrap=2, height=4, aspect=1.2,
    )
    g.map_dataframe(sns.regplot, x="feelings_composite", y="donation_amount",
                    scatter_kws={"alpha": 0.4, "s": 20}, ci=95)
    g.set_axis_labels("Feelings Composite (1–5)", "Donation ($)")
    g.set_titles("{col_name}")
    g.add_legend(title="Condition")
    g.fig.suptitle("Feelings–Donation Correlation", fontweight="bold", y=1.02)

    save_figure(g.fig, "exp1_correlation")


def plot_exp1_all(df, stats_results):
    """Generate all Exp1 plots."""
    plot_exp1_main_bars(df, stats_results)
    plot_exp1_violins(df)
    plot_exp1_heatmap(df)
    plot_exp1_radar(df)
    plot_exp1_correlation(df)
