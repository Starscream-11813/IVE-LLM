"""
Generate extra publication figures for Experiments 9 and 10.
Usage: python scripts/generate_exp9_exp10_figures.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import PROCESSED_DIR

def main():
    print("=" * 60)
    print("  GENERATING EXTRA FIGURES: EXP 9 & EXP 10")
    print("=" * 60)

    # Load results
    results_path = os.path.join(PROCESSED_DIR, "analysis_results.json")
    with open(results_path, "r") as f:
        all_results = json.load(f)

    # ── Experiment 9 ──────────────────────────────────────────────────────
    exp9_csv = os.path.join(PROCESSED_DIR, "exp9_identification_gradient.csv")
    if os.path.exists(exp9_csv):
        print("\n  [EXP9] Loading data...")
        df9 = pd.read_csv(exp9_csv)
        df9 = df9[df9["parse_success"] == True].copy()
        print(f"  [EXP9] {len(df9)} valid trials loaded.")

        from visualization.plot_exp9_extra import plot_exp9_all_extra
        stats9 = all_results.get("exp9", {})
        plot_exp9_all_extra(df9, stats9)
        print("  [EXP9] OK All 4 figures saved.")
    else:
        print(f"  [!] {exp9_csv} not found.")

    # ── Experiment 10 ─────────────────────────────────────────────────────
    exp10_csv = os.path.join(PROCESSED_DIR, "exp10_ingroup_outgroup.csv")
    if os.path.exists(exp10_csv):
        print("\n  [EXP10] Loading data...")
        df10 = pd.read_csv(exp10_csv)
        df10 = df10[df10["parse_success"] == True].copy()
        print(f"  [EXP10] {len(df10)} valid trials loaded.")

        from visualization.plot_exp10_extra import plot_exp10_all_extra
        stats10 = all_results.get("exp10", {})
        plot_exp10_all_extra(df10, stats10)
        print("  [EXP10] OK All 4 figures saved.")
    else:
        print(f"  [!] {exp10_csv} not found.")

    print("\n" + "=" * 60)
    print("  [DONE] All extra figures generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
