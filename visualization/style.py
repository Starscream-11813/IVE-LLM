"""
Publication-Quality Plot Style
===============================
Consistent styling for all IVE-LLM figures.
Colorblind-friendly palette, significance brackets, multi-format save.
Auto-generates colors for any number of models via a perceptually-uniform colormap.
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from config import FIGURES_DIR, MODELS

# ═══════════════════════════════════════════════════════════════════════════════
#  COLOR PALETTES
# ═══════════════════════════════════════════════════════════════════════════════

PALETTE = {
    "identifiable": "#E63946",
    "statistical": "#457B9D",
    "combined": "#2A9D8F",
    "no_intervention": "#264653",
    "intervention": "#E9C46A",
    "teaching": "#E9C46A",
    "none": "#264653",
    "calculate": "#457B9D",
    "feel": "#E63946",
    "cot_none": "#264653",
    "cot_standard": "#2A9D8F",
    "cot_empathetic": "#E63946",
    "cot_utilitarian": "#457B9D",
    "frame_more": "#E9C46A",
    "frame_less": "#F4A261",
    "frame_normative": "#E76F51",
}

HATCHES = {
    "identifiable": "",
    "statistical": "///",
    "combined": "xxx",
}

IDENT_STAT_PALETTE = [PALETTE["identifiable"], PALETTE["statistical"]]

# ── Auto-generate MODEL_COLORS for all registered models ─────────────────────
def _generate_model_colors(model_keys):
    """Generate visually distinct colors for an arbitrary number of models."""
    cmap = plt.cm.get_cmap("tab20", max(len(model_keys), 20))
    colors = {}
    for i, key in enumerate(sorted(model_keys)):
        colors[key] = mpl.colors.rgb2hex(cmap(i % 20))
    return colors

MODEL_COLORS = _generate_model_colors(MODELS.keys())

# ═══════════════════════════════════════════════════════════════════════════════
#  STYLE SETUP
# ═══════════════════════════════════════════════════════════════════════════════

def set_paper_style():
    """Call before creating any plot."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
        "legend.framealpha": 0.9,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "figure.figsize": (6, 4),
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
    })
    sns.set_context("paper")


# ═══════════════════════════════════════════════════════════════════════════════
#  SIGNIFICANCE BRACKETS
# ═══════════════════════════════════════════════════════════════════════════════

def add_significance_bracket(ax, x1, x2, y, p_value, height=0.05):
    """Draw a bracket between two x positions at height y with significance stars."""
    label = format_pvalue(p_value)
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y], lw=1.2, c="black")
    ax.text(
        (x1 + x2) / 2, y + height + 0.02,
        label, ha="center", va="bottom", fontsize=10, fontweight="bold",
    )


def format_pvalue(p):
    if p is None:
        return "n/a"
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "n.s."


def format_pvalue_text(p):
    if p is None:
        return "n/a"
    if p < 0.001:
        return "p < .001"
    elif p < 0.01:
        return f"p = {p:.3f}"
    elif p < 0.05:
        return f"p = {p:.3f}"
    else:
        return f"p = {p:.2f}"


# ═══════════════════════════════════════════════════════════════════════════════
#  SAVE
# ═══════════════════════════════════════════════════════════════════════════════

def save_figure(fig, name, formats=None):
    """Save figure in multiple formats."""
    if formats is None:
        formats = ["pdf", "png", "svg"]
    os.makedirs(FIGURES_DIR, exist_ok=True)
    for fmt in formats:
        path = os.path.join(FIGURES_DIR, f"{name}.{fmt}")
        fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
