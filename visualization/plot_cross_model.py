"""
Cross-Model Comparison Plots
==============================
1. Forest plot: IVE effect size by model
2. Heatmap: effect across experiments × models
3. Model size vs IVE effect
4. Temperature effects
5. Parse success rates
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from visualization.style import set_paper_style, save_figure, MODEL_COLORS, PALETTE
from analysis.statistical_tests import (
    compute_cohens_d, bootstrap_ci, compute_cross_model_effects,
    compute_parse_success_rates,
)
from config import MODEL_PARAMS


def plot_forest(dataframes, stats_results):
    """Forest plot: IVE Cohen's d per model (Exp1 core condition)."""
    set_paper_style()

    if "exp1" not in dataframes:
        return

    df = dataframes["exp1"]
    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()
    if core.empty:
        return

    models = sorted(core["model_key"].unique())
    effect_data = []

    for model in models:
        mdf = core[core["model_key"] == model]
        ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
        stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
        if len(ident) >= 2 and len(stat) >= 2:
            d = compute_cohens_d(ident, stat)
            # Bootstrap CI for Cohen's d
            combined = np.concatenate([ident.values, stat.values])
            n_i = len(ident)
            boot_ds = []
            rng = np.random.RandomState(42)
            for _ in range(2000):
                sample = rng.choice(combined, size=len(combined), replace=True)
                bd = compute_cohens_d(pd.Series(sample[:n_i]), pd.Series(sample[n_i:]))
                if not np.isnan(bd):
                    boot_ds.append(bd)
            ci_l = np.percentile(boot_ds, 2.5) if boot_ds else d
            ci_u = np.percentile(boot_ds, 97.5) if boot_ds else d
            effect_data.append((model, d, ci_l, ci_u))

    if not effect_data:
        return

    # Sort by effect size
    effect_data.sort(key=lambda x: x[1])

    fig, ax = plt.subplots(figsize=(7, max(3, len(effect_data) * 0.7)))

    for i, (model, d, ci_l, ci_u) in enumerate(effect_data):
        color = MODEL_COLORS.get(model, "#333")
        ax.plot(d, i, "D", color=color, markersize=10, zorder=5)
        ax.hlines(i, ci_l, ci_u, color=color, linewidth=2, zorder=4)
        ax.text(ci_u + 0.05, i, f"d = {d:.2f}", va="center", fontsize=9)

    ax.axvline(0, color="black", linewidth=0.8, linestyle="--", zorder=1)
    ax.set_yticks(range(len(effect_data)))
    ax.set_yticklabels([e[0] for e in effect_data])
    ax.set_xlabel("Cohen's d (Identifiable – Statistical)")
    ax.set_title("Forest Plot: IVE Effect Size by Model")
    fig.tight_layout()
    save_figure(fig, "cross_forest_plot")


def plot_effect_heatmap(dataframes, stats_results):
    """Heatmap: effect sizes across experiments × models."""
    set_paper_style()

    cross = compute_cross_model_effects(dataframes)
    if not cross:
        return

    exps = sorted(cross.keys())
    all_models = set()
    for exp_res in cross.values():
        all_models.update(exp_res.keys())
    models = sorted(all_models)

    data = np.full((len(exps), len(models)), np.nan)
    for i, exp in enumerate(exps):
        for j, model in enumerate(models):
            if model in cross[exp]:
                data[i, j] = cross[exp][model]["cohens_d"]

    fig, ax = plt.subplots(figsize=(max(6, len(models) * 1.5), max(4, len(exps) * 0.8)))
    im = ax.imshow(data, cmap="RdBu_r", aspect="auto", vmin=-1, vmax=1)

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=30, ha="right")
    ax.set_yticks(range(len(exps)))
    ax.set_yticklabels([e.upper() for e in exps])

    for i in range(len(exps)):
        for j in range(len(models)):
            if not np.isnan(data[i, j]):
                ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center",
                        fontsize=9, color="white" if abs(data[i, j]) > 0.5 else "black")

    fig.colorbar(im, ax=ax, shrink=0.7, label="Cohen's d")
    ax.set_title("IVE Effect Size Across Experiments and Models")
    fig.tight_layout()
    save_figure(fig, "cross_effect_heatmap")


def plot_model_size_vs_effect(dataframes, stats_results):
    """Scatter: model parameter count vs IVE effect."""
    set_paper_style()

    if "exp1" not in dataframes:
        return

    df = dataframes["exp1"]
    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()

    models = sorted(core["model_key"].unique())

    fig, ax = plt.subplots(figsize=(7, 5))
    for model in models:
        if model not in MODEL_PARAMS:
            continue
        mdf = core[core["model_key"] == model]
        ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
        stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
        if len(ident) >= 2 and len(stat) >= 2:
            d = compute_cohens_d(ident, stat)
            params = MODEL_PARAMS[model]
            color = MODEL_COLORS.get(model, "#333")
            ax.scatter(params, d, s=120, c=color, zorder=5, edgecolors="white")
            ax.annotate(model, (params, d), textcoords="offset points",
                        xytext=(8, 5), fontsize=9)

    ax.set_xscale("log")
    ax.set_xlabel("Parameters (Billions, log scale)")
    ax.set_ylabel("IVE Effect Size (Cohen's d)")
    ax.set_title("Model Scale vs. IVE Effect")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    fig.tight_layout()
    save_figure(fig, "cross_size_vs_effect")


def plot_temperature_effects(dataframes, stats_results):
    """Grouped bars: temperature × model for IVE effect."""
    set_paper_style()

    if "exp1" not in dataframes:
        return

    df = dataframes["exp1"]
    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()

    models = sorted(core["model_key"].unique())
    temps = sorted(core["temperature"].unique())

    if len(temps) < 2:
        return

    fig, ax = plt.subplots(figsize=(max(6, len(models) * 2), 5))
    x = np.arange(len(models))
    width = 0.8 / len(temps)

    for i, temp in enumerate(temps):
        effects = []
        for model in models:
            mdf = core[(core["model_key"] == model) & (core["temperature"] == temp)]
            ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
            stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
            d = compute_cohens_d(ident, stat) if len(ident) >= 2 and len(stat) >= 2 else 0
            effects.append(d if not np.isnan(d) else 0)
        offset = (i - (len(temps) - 1) / 2) * width
        ax.bar(x + offset, effects, width, label=f"T={temp}",
               edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=30, ha="right")
    ax.set_ylabel("IVE Effect Size (Cohen's d)")
    ax.set_title("Temperature Effects on IVE")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "cross_temperature_effects")


def plot_parse_success(dataframes, stats_results):
    """Bar chart: parse success rate by model × experiment."""
    set_paper_style()

    rates = compute_parse_success_rates(dataframes)
    if not rates:
        return

    exps = sorted(rates.keys())
    all_models = set()
    for exp_res in rates.values():
        all_models.update(exp_res.keys())
    models = sorted(all_models)

    data = np.zeros((len(exps), len(models)))
    for i, exp in enumerate(exps):
        for j, model in enumerate(models):
            data[i, j] = rates[exp].get(model, 0)

    fig, ax = plt.subplots(figsize=(max(6, len(models) * 1.5), max(4, len(exps) * 0.6)))
    im = ax.imshow(data, cmap="Greens", aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=30, ha="right")
    ax.set_yticks(range(len(exps)))
    ax.set_yticklabels([e.upper() for e in exps])

    for i in range(len(exps)):
        for j in range(len(models)):
            ax.text(j, i, f"{data[i, j]:.0f}%", ha="center", va="center",
                    fontsize=9, color="white" if data[i, j] > 70 else "black")

    fig.colorbar(im, ax=ax, shrink=0.7, label="Parse Success %")
    ax.set_title("Response Parse Success Rate")
    fig.tight_layout()
    save_figure(fig, "cross_parse_success")


def plot_cross_model_all(dataframes, stats_results):
    plot_forest(dataframes, stats_results)
    plot_effect_heatmap(dataframes, stats_results)
    plot_model_size_vs_effect(dataframes, stats_results)
    plot_temperature_effects(dataframes, stats_results)
    plot_parse_success(dataframes, stats_results)
