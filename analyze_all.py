"""
IVE-LLM Master Analysis Script
================================
Load all experiment data, run statistical analyses, save results and tables.

Usage:
    python analyze_all.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from config import PROCESSED_DIR
from analysis.statistical_tests import (
    ANALYSIS_FUNCTIONS, run_all_analyses,
    compute_cross_model_effects, compute_parse_success_rates,
)

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


def load_dataframes() -> dict:
    """Load all experiment CSV files that exist."""
    
    target_model = sys.argv[1] if len(sys.argv) > 1 else None
    
    dataframes = {}
    for key, name in EXPERIMENT_NAMES.items():
        csv_path = os.path.join(PROCESSED_DIR, f"{name}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = df[df["parse_success"] == True].copy()
            if target_model:
                df = df[df["model_key"] == target_model].copy()
            if len(df) > 0:
                dataframes[key] = df
                print(f"  [OK] Loaded {key}: {len(df)} valid trials from {name}.csv")
            else:
                print(f"  [!] {key}: no valid (parse_success) trials")
        else:
            print(f"  - {key}: no data file found")
    return dataframes


def print_summary(exp_name: str, results: dict):
    """Pretty-print key results for one experiment."""
    print(f"\n{'=' * 60}")
    print(f"  {exp_name.upper()} RESULTS")
    print(f"{'=' * 60}")

    if "per_model" in results:
        print("\n  Per-Model IVE:")
        for model, r in results["per_model"].items():
            d = r.get("cohens_d", "N/A")
            p = r.get("t_p", "N/A")
            mi = r.get("identifiable", {}).get("mean", "N/A")
            ms = r.get("statistical", {}).get("mean", "N/A")
            print(f"    {model:20s}  Ident={mi}  Stat={ms}  d={d}  p={p}")

    if "pooled" in results:
        p = results["pooled"]
        print(f"\n  Pooled: d={p.get('cohens_d', 'N/A')}  p={p.get('t_p', 'N/A')}")

    if "cells" in results:
        print("\n  Cell Means:")
        for cell_name, cell_stats in results["cells"].items():
            print(f"    {cell_name:35s}  M={cell_stats['mean']}  SD={cell_stats['sd']}  n={cell_stats['n']}")

    if "simple_effects" in results:
        print("\n  Simple Effects:")
        for key, se in results["simple_effects"].items():
            print(f"    {key:20s}  d={se.get('cohens_d', 'N/A')}  p={se.get('t_p', 'N/A')}")

    if "ive_by_cot" in results:
        print("\n  IVE by CoT Type:")
        for cot, r in results["ive_by_cot"].items():
            print(f"    {cot:15s}  d={r.get('cohens_d', 'N/A')}  p={r.get('t_p', 'N/A')}")

    if "regression" in results:
        for fit_name, fit in results["regression"].items():
            print(f"\n  Regression ({fit_name}): R²={fit.get('r_squared', 'N/A')}  "
                  f"slope={fit.get('slope', 'N/A')}  p={fit.get('p_value', 'N/A')}")

    if "meta_knowledge" in results:
        mk = results["meta_knowledge"]
        print(f"\n  Meta-Knowledge: {mk.get('pct_aware', 'N/A')}% aware (n={mk.get('n_total', 'N/A')})")


def generate_paper_tables(results: dict, dataframes: dict):
    """Generate summary tables as CSVs."""
    tables_dir = os.path.join(PROCESSED_DIR, "summary_tables")
    os.makedirs(tables_dir, exist_ok=True)

    # Table 1: Exp1 per-model summary
    if "exp1" in results and "per_model" in results["exp1"]:
        rows = []
        for model, r in results["exp1"]["per_model"].items():
            rows.append({
                "Model": model,
                "Stat Mean": r.get("statistical", {}).get("mean"),
                "Stat SD": r.get("statistical", {}).get("sd"),
                "Ident Mean": r.get("identifiable", {}).get("mean"),
                "Ident SD": r.get("identifiable", {}).get("sd"),
                "Cohen's d": r.get("cohens_d"),
                "t": r.get("t_stat"),
                "p": r.get("t_p"),
            })
        pd.DataFrame(rows).to_csv(
            os.path.join(tables_dir, "table1_exp1_summary.csv"), index=False
        )
        print(f"\n  - Table 1 saved to summary_tables/table1_exp1_summary.csv")

    # Table 2: Cross-experiment effect sizes
    if len(results) > 1:
        cross_rows = []
        for exp_name, exp_res in results.items():
            if "pooled" in exp_res:
                cross_rows.append({
                    "Experiment": exp_name,
                    "Cohen's d": exp_res["pooled"].get("cohens_d"),
                    "p": exp_res["pooled"].get("t_p"),
                })
        if cross_rows:
            pd.DataFrame(cross_rows).to_csv(
                os.path.join(tables_dir, "table2_cross_experiment.csv"), index=False
            )


def main():
    print("=" * 60)
    print("  IVE-LLM ANALYSIS")
    print("=" * 60)

    dataframes = load_dataframes()
    if not dataframes:
        print("\n  [!] No experiment data found. Run experiments first.")
        return

    results = run_all_analyses(dataframes)

    for exp_name, exp_results in results.items():
        print_summary(exp_name, exp_results)

    # Save all results as JSON
    results_path = os.path.join(PROCESSED_DIR, "analysis_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  - Full results saved to {results_path}")

    # Generate paper tables
    generate_paper_tables(results, dataframes)

    # Parse success rates
    psr = compute_parse_success_rates(dataframes)
    print(f"\n{'=' * 60}")
    print("  PARSE SUCCESS RATES")
    print(f"{'=' * 60}")
    for exp, rates in psr.items():
        rate_str = "  ".join(f"{m}: {r:.0f}%" for m, r in rates.items())
        print(f"  {exp}: {rate_str}")

    print(f"\n{'=' * 60}")
    print("  [DONE] Analysis complete.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
