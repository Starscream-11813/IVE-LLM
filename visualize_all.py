"""
IVE-LLM Master Visualization Script
======================================
Generate all figures for the paper.
Outputs to data/figures/ in PDF, PNG, and SVG formats.

Usage:
    python visualize_all.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from config import PROCESSED_DIR, FIGURES_DIR
from visualization.style import set_paper_style
from visualization.plot_exp1 import plot_exp1_all
from visualization.plot_exp2 import plot_exp2_all
from visualization.plot_exp3 import plot_exp3_all
from visualization.plot_exp4 import plot_exp4_all
from visualization.plot_exp5 import plot_exp5_all
from visualization.plot_exp6 import plot_exp6_all
from visualization.plot_exp7 import plot_exp7_all
from visualization.plot_exp8 import plot_exp8_all
from visualization.plot_exp9 import plot_exp9_all
from visualization.plot_exp10 import plot_exp10_all
from visualization.plot_emotion_mediation import plot_emotion_mediation_all
from visualization.plot_cross_model import plot_cross_model_all
from visualization.plot_linguistic import plot_linguistic_all
from analysis.statistical_tests import ANALYSIS_FUNCTIONS

EXPERIMENT_NAMES = {
    "exp1": "exp1_basic_ive",
    "exp2": "exp2_explicit_debiasing",
    "exp3": "exp3_framing",
    "exp4": "exp4_joint_separate",
    "exp5": "exp5_processing_prime",
    "exp6": "exp6_chain_of_thought",
    "exp7": "exp7_psychophysical_numbing",
    "exp8": "exp8_singularity",
    "exp9": "exp9_identification_gradient",
    "exp10": "exp10_ingroup_outgroup",
}

PLOT_FUNCTIONS = {
    "exp1": plot_exp1_all,
    "exp2": plot_exp2_all,
    "exp3": plot_exp3_all,
    "exp4": plot_exp4_all,
    "exp5": plot_exp5_all,
    "exp6": plot_exp6_all,
    "exp7": plot_exp7_all,
    "exp8": plot_exp8_all,
    "exp9": plot_exp9_all,
    "exp10": plot_exp10_all,
}


def main():
    set_paper_style()
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("━" * 60)
    print("  IVE-LLM VISUALIZATION")
    print("━" * 60)

    # Load data
    dataframes = {}
    stats_results = {}

    for key, name in EXPERIMENT_NAMES.items():
        csv_path = os.path.join(PROCESSED_DIR, f"{name}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = df[df["parse_success"] == True].copy()
            if len(df) > 0:
                dataframes[key] = df
                # Run analysis for stats annotations
                if key in ANALYSIS_FUNCTIONS:
                    stats_results[key] = ANALYSIS_FUNCTIONS[key](df)
                print(f"  ✓ Loaded {key}: {len(df)} trials")
        else:
            print(f"  · {key}: no data file found")

    if not dataframes:
        print("\n  ⚠ No data found. Run experiments first with `python run_all.py`.")
        return

    # Per-experiment plots
    for key in dataframes:
        if key in PLOT_FUNCTIONS:
            print(f"\n  Generating {key.upper()} plots...")
            try:
                PLOT_FUNCTIONS[key](dataframes[key], stats_results.get(key, {}))
                print(f"    ✓ {key} plots saved")
            except Exception as e:
                print(f"    ✗ {key} plot error: {e}")

    # Cross-model plots
    if len(dataframes) > 0:
        print(f"\n  Generating cross-model plots...")
        try:
            plot_cross_model_all(dataframes, stats_results)
            print(f"    ✓ Cross-model plots saved")
        except Exception as e:
            print(f"    ✗ Cross-model plot error: {e}")

    # Linguistic plots
    all_data = pd.concat(dataframes.values(), ignore_index=True)
    if len(all_data) > 0:
        print(f"\n  Generating linguistic analysis plots...")
        try:
            plot_linguistic_all(all_data)
            print(f"    ✓ Linguistic plots saved")
        except Exception as e:
            print(f"    ✗ Linguistic plot error: {e}")

    # Emotion mediation plots (for exp8-10 data)
    extended_dfs = [dataframes[k] for k in ["exp8", "exp9", "exp10"] if k in dataframes]
    if extended_dfs:
        print(f"\n  Generating emotion/mediation plots...")
        try:
            ext_data = pd.concat(extended_dfs, ignore_index=True)
            plot_emotion_mediation_all(ext_data)
            print(f"    ✓ Emotion/mediation plots saved")
        except Exception as e:
            print(f"    ✗ Emotion/mediation plot error: {e}")

    print(f"\n{'━' * 60}")
    print(f"  ✓ All figures saved to {FIGURES_DIR}/")
    print(f"{'━' * 60}")


if __name__ == "__main__":
    main()
