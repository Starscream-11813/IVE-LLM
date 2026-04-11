"""
Regenerate fig_distress_vs_empathy with:
  - Color palette inspired by the blob/transport diagram (purples, blues, magentas)
  - LaTeX Computer Modern fonts
"""

import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy import stats
from visualization.style import save_figure

# ── LaTeX / Computer Modern font setup ────────────────────────────────────────
mpl.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage{amssymb}',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'legend.framealpha': 0.92,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
})

# ── Blob-diagram inspired palette ────────────────────────────────────────────
# Deep indigo, sky blue, lavender-purple, orchid-magenta
BLOB_PALETTE = {
    'single_full':         '#FF6EB4',   # hot pink
    'single_unidentified': '#4DB8FF',   # sky blue
    'group_full':          '#9B59B6',   # medium purple
    'group_unidentified':  '#CC99FF',   # light lavender
}
BLOB_LABELS = {
    'single_full':         r'Single $+$ Full ID',
    'single_unidentified': r'Single $+$ Unidentified',
    'group_full':          r'Group $+$ Full ID',
    'group_unidentified':  r'Group $+$ Unidentified',
}


def main():
    # Load data
    df = pd.read_csv('data/processed/exp8_singularity.csv')
    df = df[df['parse_success'] == True].copy()
    clean = df.dropna(subset=['distress_composite', 'empathy_composite', 'donation_amount']).copy()
    clean['cond_label'] = clean['singularity'] + '_' + clean['identification_level']

    # Load parallel mediation
    with open('data/processed/analysis_results.json', 'r') as f:
        results = json.load(f)
    pm = results.get('exp8', {}).get('dual_mediation', {}).get('parallel_model', {})

    # Correlations
    r_dd, _ = stats.pearsonr(clean['distress_composite'], clean['donation_amount'])
    r_ed, _ = stats.pearsonr(clean['empathy_composite'], clean['donation_amount'])

    fig, ax = plt.subplots(figsize=(9, 7))

    # ── Scatter ───────────────────────────────────────────────────────────
    for label in ['group_unidentified', 'single_unidentified', 'group_full', 'single_full']:
        color = BLOB_PALETTE[label]
        display = BLOB_LABELS[label]
        sub = clean[clean['cond_label'] == label]
        if sub.empty:
            continue
        sizes = sub['donation_amount'].fillna(2.5) * 12 + 8
        ax.scatter(sub['distress_composite'], sub['empathy_composite'],
                   c=color, s=sizes, alpha=0.50, label=display,
                   edgecolors='white', linewidth=0.4, zorder=3)

    # ── Equality line ─────────────────────────────────────────────────────
    lims = [0.5, 7.5]
    ax.plot(lims, lims, color='#aaa', linestyle='--', linewidth=0.9,
            alpha=0.5, label=r'Equality line', zorder=1)
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    # ── Grand Mean marker ─────────────────────────────────────────────────
    mean_dist = clean['distress_composite'].mean()
    mean_emp = clean['empathy_composite'].mean()
    ax.axvline(mean_dist, color='#9B59B6', linewidth=0.8, linestyle=':', alpha=0.4)
    ax.axhline(mean_emp, color='#4DB8FF', linewidth=0.8, linestyle=':', alpha=0.4)
    ax.plot(mean_dist, mean_emp, '*', color='white', markersize=16, zorder=11,
            markeredgecolor='#6B3FA0', markeredgewidth=1.8)
    ax.annotate(rf'Grand Mean ({mean_dist:.2f}, {mean_emp:.2f})',
                xy=(mean_dist, mean_emp),
                xytext=(mean_dist + 0.7, mean_emp - 0.9),
                fontsize=9, ha='left', color='#6B3FA0',
                arrowprops=dict(arrowstyle='->', color='#6B3FA0', lw=1.2))

    # ── Parallel mediation annotation box ─────────────────────────────────
    if pm:
        c_total = pm.get('path_c_coeff', 0)
        c_prime = pm.get('path_c_prime_coeff', 0)
        a1 = pm.get('path_a1_coeff', 0)
        b1 = pm.get('path_b1_coeff', 0)
        a2 = pm.get('path_a2_coeff', 0)
        b2 = pm.get('path_b2_coeff', 0)
        ind1 = pm.get('indirect1', 0)
        ind2 = pm.get('indirect2', 0)
        n = pm.get('n', 0)

        textbox = (
            rf"\textbf{{Parallel Mediation}} ($N = {n}$)" "\n"
            r"\rule{5.2cm}{0.4pt}" "\n"
            rf"Total effect ($c$): $\beta = {c_total:.2f}^{{***}}$" "\n"
            rf"Direct effect ($c'$): $\beta = {c_prime:.2f}^{{***}}$" "\n"
            r"\rule{5.2cm}{0.4pt}" "\n"
            rf"Distress: $a_1 = {a1:.2f}^{{***}},\ b_1 = {b1:.2f}^{{***}}$" "\n"
            rf"\quad Indirect $a_1 b_1 = {ind1:.3f}$" "\n"
            rf"Empathy: $a_2 = {a2:.2f}^{{***}},\ b_2 = {b2:.2f}^{{***}}$" "\n"
            rf"\quad Indirect $a_2 b_2 = {ind2:.3f}$" "\n"
            r"\rule{5.2cm}{0.4pt}" "\n"
            rf"Distress dominance: ${ind1/ind2:.1f}\times$"
        )

        props = dict(boxstyle='round,pad=0.6', facecolor='#F3EAFF',
                     edgecolor='#6B3FA0', alpha=0.92, linewidth=1.2)
        ax.text(0.02, 0.98, textbox, transform=ax.transAxes, fontsize=8.5,
                verticalalignment='top', bbox=props)

    # ── Correlation annotations ───────────────────────────────────────────
    ax.text(0.98, 0.02,
            rf'$r_{{\mathrm{{dist,don}}}} = {r_dd:.3f}$' '\n'
            rf'$r_{{\mathrm{{emp,don}}}} = {r_ed:.3f}$',
            transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
            color='#6B3FA0', fontstyle='italic')

    # ── Labels ────────────────────────────────────────────────────────────
    ax.set_xlabel(r'Distress Composite (1--7)')
    ax.set_ylabel(r'Empathic Concern Composite (1--7)')
    ax.set_title(r'Distress vs.\ Empathic Concern: Parallel Mediation Context')
    ax.legend(fontsize=9, loc='center right', framealpha=0.92,
              edgecolor='#6B3FA0', fancybox=True)

    fig.tight_layout()
    save_figure(fig, 'fig_distress_vs_empathy')
    print("[OK] fig_distress_vs_empathy regenerated (blob palette + CM font).")


if __name__ == '__main__':
    main()
