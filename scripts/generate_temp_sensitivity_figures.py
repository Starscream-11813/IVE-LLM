"""
Temperature & Sensitivity Analysis — Publication Figures
=========================================================
1. Paired dot plot: d at T=0.0 vs T=0.7 per model (Exp 1)
2. Grouped bar chart: pooled d at each temperature across experiments
3. Heatmap: Model x Temperature x Cohen's d
4. Forest plot comparison: Full vs Excluded pool
5. Before/After paired bar chart for sensitivity
"""

import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy import stats
from visualization.style import set_paper_style, save_figure, MODEL_COLORS

EXCLUDE = ['gemini-2.5-flash', 'llama3-8b-instruct']

EXPERIMENTS = {
    'exp1': 'exp1_basic_ive',
    'exp2': 'exp2_explicit_debiasing',
    'exp3': 'exp3_framing',
    'exp4': 'exp4_joint_separate',
    'exp5': 'exp5_processing_prime',
    'exp6': 'exp6_chain_of_thought',
    'exp10': 'exp10_ingroup_outgroup',
}
EXP_LABELS = {
    'exp1': 'Exp 1\nBasic IVE',
    'exp2': 'Exp 2\nDebiasing',
    'exp3': 'Exp 3\nFraming',
    'exp4': 'Exp 4\nJoint/Sep',
    'exp5': 'Exp 5\nPriming',
    'exp6': 'Exp 6\nCoT',
    'exp10': 'Exp 10\nIn-Group',
}


def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return float('nan')
    v1, v2 = g1.var(ddof=1), g2.var(ddof=1)
    sp = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    return (g1.mean() - g2.mean()) / sp if sp > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1: Paired Dot Plot — d at T=0.0 vs T=0.7 per model
# ═══════════════════════════════════════════════════════════════════════════════

def plot_temp_paired_dots():
    set_paper_style()
    df = pd.read_csv('data/processed/exp1_basic_ive.csv')
    df = df[(df['parse_success'] == True) &
            (df['condition_persona'] == 'none') &
            (df['condition_prompt_frame'] == 'first_person')].copy()

    models = sorted(df['model_key'].unique())
    data = {}
    for t in [0.0, 0.7]:
        tdf = df[df['temperature'] == t]
        for m in models:
            mdf = tdf[tdf['model_key'] == m]
            ig = mdf[mdf['condition_identifiability'] == 'identifiable']['donation_amount'].dropna()
            sg = mdf[mdf['condition_identifiability'] == 'statistical']['donation_amount'].dropna()
            if len(ig) >= 2 and len(sg) >= 2:
                d = cohens_d(ig, sg)
                data.setdefault(m, {})[t] = float(d)

    # Filter to models present at both temperatures
    both = [m for m in models if 0.0 in data.get(m, {}) and 0.7 in data.get(m, {})]
    # Sort by average d
    both.sort(key=lambda m: (data[m][0.0] + data[m][0.7]) / 2)

    fig, ax = plt.subplots(figsize=(8, max(5, len(both) * 0.42)))
    y_pos = np.arange(len(both))

    for i, m in enumerate(both):
        d0 = data[m][0.0]
        d7 = data[m][0.7]
        # Connecting line
        color = '#E63946' if abs(d7 - d0) > 0.5 else '#aaa'
        lw = 2.0 if abs(d7 - d0) > 0.5 else 1.0
        ax.plot([d0, d7], [i, i], color=color, linewidth=lw, alpha=0.6, zorder=1)
        # Dots
        ax.scatter(d0, i, color='#457B9D', s=70, zorder=5, edgecolor='white', linewidth=1.2)
        ax.scatter(d7, i, color='#E63946', s=70, zorder=5, edgecolor='white', linewidth=1.2)

    # Zero line
    ax.axvline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)
    # Human benchmark
    ax.axvline(0.23, color='#2A9D8F', linewidth=1.5, linestyle='--', alpha=0.7)
    ax.text(0.23, len(both) - 0.3, 'Human\n$d = 0.23$', fontsize=8,
            color='#2A9D8F', ha='center', fontstyle='italic')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([m.replace('-', '\n') for m in both], fontsize=8)
    ax.set_xlabel("Cohen's $d$ (IVE Effect Size)")
    ax.set_title("Temperature Effect on IVE: $T=0.0$ vs $T=0.7$ (Exp 1)")

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#457B9D',
                    markersize=9, label='$T = 0.0$ (Deterministic)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E63946',
                    markersize=9, label='$T = 0.7$ (Stochastic)'),
        plt.Line2D([0], [0], color='#E63946', linewidth=2, alpha=0.6,
                    label='Large shift ($|\\Delta d| > 0.5$)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8)

    fig.tight_layout()
    save_figure(fig, 'temp_paired_dots')
    print("  [OK] temp_paired_dots saved.")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2: Grouped Bars — pooled d at each temperature across experiments
# ═══════════════════════════════════════════════════════════════════════════════

def plot_temp_experiment_bars():
    set_paper_style()

    exp_keys = list(EXPERIMENTS.keys())
    d_t0, d_t7 = [], []

    for key in exp_keys:
        csv = f'data/processed/{EXPERIMENTS[key]}.csv'
        df = pd.read_csv(csv)
        df = df[df['parse_success'] == True].copy()
        if 'condition_identifiability' not in df.columns:
            continue
        for t, store in [(0.0, d_t0), (0.7, d_t7)]:
            tdf = df[df['temperature'] == t]
            ig = tdf[tdf['condition_identifiability'] == 'identifiable']['donation_amount'].dropna()
            sg = tdf[tdf['condition_identifiability'] == 'statistical']['donation_amount'].dropna()
            if len(ig) >= 2 and len(sg) >= 2:
                store.append(cohens_d(ig, sg))
            else:
                store.append(0)

    x = np.arange(len(exp_keys))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))

    bars1 = ax.bar(x - width / 2, d_t0, width, color='#457B9D',
                   edgecolor='white', linewidth=1.2, label='$T = 0.0$')
    bars2 = ax.bar(x + width / 2, d_t7, width, color='#E63946',
                   edgecolor='white', linewidth=1.2, label='$T = 0.7$')

    # Value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.02,
                    f'{h:.2f}', ha='center', fontsize=8, fontweight='bold')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axhline(0.23, color='#2A9D8F', linewidth=1.2, linestyle='--', alpha=0.6)
    ax.text(len(exp_keys) - 0.5, 0.25, 'Human $d$', fontsize=8,
            color='#2A9D8F', fontstyle='italic')

    ax.set_xticks(x)
    ax.set_xticklabels([EXP_LABELS[k] for k in exp_keys], fontsize=9)
    ax.set_ylabel("Cohen's $d$ (IVE)")
    ax.set_title("IVE Effect Size by Temperature Across Experiments")
    ax.legend(loc='upper right', fontsize=10)

    fig.tight_layout()
    save_figure(fig, 'temp_experiment_bars')
    print("  [OK] temp_experiment_bars saved.")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 3: Heatmap — Model x Temperature x Cohen's d
# ═══════════════════════════════════════════════════════════════════════════════

def plot_temp_heatmap():
    set_paper_style()
    df = pd.read_csv('data/processed/exp1_basic_ive.csv')
    df = df[(df['parse_success'] == True) &
            (df['condition_persona'] == 'none') &
            (df['condition_prompt_frame'] == 'first_person')].copy()

    models = sorted(df['model_key'].unique())
    temps = [0.0, 0.7]
    data = []
    valid_models = []

    for m in models:
        row = []
        has_data = True
        for t in temps:
            tdf = df[(df['model_key'] == m) & (df['temperature'] == t)]
            ig = tdf[tdf['condition_identifiability'] == 'identifiable']['donation_amount'].dropna()
            sg = tdf[tdf['condition_identifiability'] == 'statistical']['donation_amount'].dropna()
            if len(ig) >= 2 and len(sg) >= 2:
                row.append(cohens_d(ig, sg))
            else:
                row.append(np.nan)
                has_data = False
        if has_data:
            data.append(row)
            valid_models.append(m)

    data_arr = np.array(data)
    # Sort by average d
    avg_d = np.nanmean(data_arr, axis=1)
    sort_idx = np.argsort(avg_d)
    data_arr = data_arr[sort_idx]
    valid_models = [valid_models[i] for i in sort_idx]

    fig, ax = plt.subplots(figsize=(5, max(5, len(valid_models) * 0.45)))
    im = ax.imshow(data_arr, cmap='RdBu_r', aspect='auto', vmin=-2.0, vmax=2.0)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(['$T = 0.0$', '$T = 0.7$'], fontsize=11, fontweight='bold')
    ax.set_yticks(range(len(valid_models)))
    ax.set_yticklabels([m.replace('-', '\n') for m in valid_models], fontsize=8)

    for i in range(len(valid_models)):
        for j in range(2):
            val = data_arr[i, j]
            if not np.isnan(val):
                text_color = 'white' if abs(val) > 1.2 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=9, color=text_color, fontweight='bold')

    fig.colorbar(im, ax=ax, shrink=0.7, label="Cohen's $d$")
    ax.set_title("IVE by Model and Temperature (Exp 1)")

    fig.tight_layout()
    save_figure(fig, 'temp_model_heatmap')
    print("  [OK] temp_model_heatmap saved.")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 4: Forest Plot Comparison — Full vs Excluded Pool
# ═══════════════════════════════════════════════════════════════════════════════

def plot_sensitivity_forest():
    set_paper_style()

    exp_keys = list(EXPERIMENTS.keys())
    full_d, excl_d = [], []
    full_ci, excl_ci = [], []

    for key in exp_keys:
        csv = f'data/processed/{EXPERIMENTS[key]}.csv'
        df = pd.read_csv(csv)
        df = df[df['parse_success'] == True].copy()
        if 'condition_identifiability' not in df.columns:
            continue

        for exclude, d_store, ci_store in [
            (False, full_d, full_ci), (True, excl_d, excl_ci)
        ]:
            subset = df[~df['model_key'].isin(EXCLUDE)] if exclude else df
            ig = subset[subset['condition_identifiability'] == 'identifiable']['donation_amount'].dropna()
            sg = subset[subset['condition_identifiability'] == 'statistical']['donation_amount'].dropna()
            if len(ig) >= 2 and len(sg) >= 2:
                d = cohens_d(ig, sg)
                n = len(ig) + len(sg)
                se = np.sqrt(1/len(ig) + 1/len(sg) + d**2 / (2*n))
                d_store.append(d)
                ci_store.append(1.96 * se)
            else:
                d_store.append(0)
                ci_store.append(0)

    y = np.arange(len(exp_keys))
    offset = 0.15
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Full pool
    ax.errorbar(full_d, y + offset, xerr=full_ci, fmt='s', color='#999',
                markersize=8, capsize=4, capthick=1.5, linewidth=1.5,
                markeredgecolor='white', markeredgewidth=1, label='Full Pool (16 models)',
                zorder=4)

    # Excluded pool
    ax.errorbar(excl_d, y - offset, xerr=excl_ci, fmt='D', color='#E63946',
                markersize=8, capsize=4, capthick=1.5, linewidth=1.5,
                markeredgecolor='white', markeredgewidth=1, label='Excluded Pool (14 models)',
                zorder=5)

    # Zero line
    ax.axvline(0, color='black', linewidth=0.8, alpha=0.5)
    # Human benchmark
    ax.axvline(0.23, color='#2A9D8F', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.text(0.23, len(exp_keys) - 0.3, 'Human\n$d = 0.23$', fontsize=8,
            color='#2A9D8F', ha='center', fontstyle='italic')

    ax.set_yticks(y)
    ax.set_yticklabels([EXP_LABELS[k] for k in exp_keys], fontsize=10)
    ax.set_xlabel("Cohen's $d$ (IVE Effect Size)")
    ax.set_title("Sensitivity Analysis: Full vs. Ceiling-Excluded Pool")
    ax.legend(loc='lower right', fontsize=10)
    ax.invert_yaxis()

    fig.tight_layout()
    save_figure(fig, 'sensitivity_forest')
    print("  [OK] sensitivity_forest saved.")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 5: Before/After Paired Bar Chart
# ═══════════════════════════════════════════════════════════════════════════════

def plot_sensitivity_bars():
    set_paper_style()

    exp_keys = list(EXPERIMENTS.keys())
    full_d, excl_d = [], []

    for key in exp_keys:
        csv = f'data/processed/{EXPERIMENTS[key]}.csv'
        df = pd.read_csv(csv)
        df = df[df['parse_success'] == True].copy()
        if 'condition_identifiability' not in df.columns:
            continue

        for exclude, d_store in [(False, full_d), (True, excl_d)]:
            subset = df[~df['model_key'].isin(EXCLUDE)] if exclude else df
            ig = subset[subset['condition_identifiability'] == 'identifiable']['donation_amount'].dropna()
            sg = subset[subset['condition_identifiability'] == 'statistical']['donation_amount'].dropna()
            if len(ig) >= 2 and len(sg) >= 2:
                d_store.append(cohens_d(ig, sg))
            else:
                d_store.append(0)

    x = np.arange(len(exp_keys))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))

    bars1 = ax.bar(x - width / 2, full_d, width, color='#bbb',
                   edgecolor='white', linewidth=1.2, label='Full Pool (16)')
    bars2 = ax.bar(x + width / 2, excl_d, width, color='#E63946',
                   edgecolor='white', linewidth=1.2, label='Excluded Pool (14)')

    # Value labels
    for bars, vals in [(bars1, full_d), (bars2, excl_d)]:
        for bar, v in zip(bars, vals):
            y_pos = v + 0.02 if v >= 0 else v - 0.06
            ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                    f'{v:.2f}', ha='center', fontsize=8, fontweight='bold')

    # Delta arrows between pairs
    for i in range(len(exp_keys)):
        delta = excl_d[i] - full_d[i]
        sign = '+' if delta > 0 else ''
        color = '#2A9D8F' if delta > 0 else '#E76F51'
        y_top = max(full_d[i], excl_d[i]) + 0.08
        ax.text(x[i], y_top, f'{sign}{delta:.3f}', ha='center', fontsize=7,
                color=color, fontweight='bold', fontstyle='italic')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axhline(0.23, color='#2A9D8F', linewidth=1.2, linestyle='--', alpha=0.6)
    ax.text(len(exp_keys) - 0.5, 0.25, 'Human $d = 0.23$', fontsize=8,
            color='#2A9D8F', fontstyle='italic')

    ax.set_xticks(x)
    ax.set_xticklabels([EXP_LABELS[k] for k in exp_keys], fontsize=9)
    ax.set_ylabel("Cohen's $d$ (IVE)")
    ax.set_title("Sensitivity: Effect Size Before/After Ceiling Exclusion")
    ax.legend(loc='upper right', fontsize=10)

    fig.tight_layout()
    save_figure(fig, 'sensitivity_bars')
    print("  [OK] sensitivity_bars saved.")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  GENERATING TEMPERATURE & SENSITIVITY FIGURES")
    print("=" * 60)
    plot_temp_paired_dots()
    plot_temp_experiment_bars()
    plot_temp_heatmap()
    plot_sensitivity_forest()
    plot_sensitivity_bars()
    print("\n" + "=" * 60)
    print("  [DONE] All 5 figures generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
