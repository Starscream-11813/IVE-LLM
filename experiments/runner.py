"""
Experiment Runner (CLI)
========================
Master runner that dispatches individual experiments or all experiments.
Supports --quick-test mode for pipeline validation.
"""

import argparse
import sys

from experiments.exp1_basic_ive import Exp1BasicIVE
from experiments.exp2_explicit_debiasing import Exp2ExplicitDebiasing
from experiments.exp3_framing import Exp3Framing
from experiments.exp4_joint_separate import Exp4JointSeparate
from experiments.exp5_processing_prime import Exp5ProcessingPrime
from experiments.exp6_chain_of_thought import Exp6ChainOfThought
from experiments.exp7_psychophysical_numbing import Exp7PsychophysicalNumbing
from experiments.exp8_singularity import Exp8Singularity
from experiments.exp9_identification_gradient import Exp9IdentificationGradient
from experiments.exp10_ingroup_outgroup import Exp10IngroupOutgroup

EXPERIMENTS = {
    "exp1": Exp1BasicIVE,
    "exp2": Exp2ExplicitDebiasing,
    "exp3": Exp3Framing,
    "exp4": Exp4JointSeparate,
    "exp5": Exp5ProcessingPrime,
    "exp6": Exp6ChainOfThought,
    "exp7": Exp7PsychophysicalNumbing,
    "exp8": Exp8Singularity,
    "exp9": Exp9IdentificationGradient,
    "exp10": Exp10IngroupOutgroup,
}


def main():
    parser = argparse.ArgumentParser(
        description="IVE-LLM Experiment Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m experiments.runner --experiments exp1 exp2
  python -m experiments.runner --experiments exp8 exp9 exp10
  python -m experiments.runner --quick-test
  python -m experiments.runner --models gpt-4o claude-4.5-sonnet --runs 10
        """,
    )
    parser.add_argument(
        "--experiments", nargs="+", default=["all"],
        choices=list(EXPERIMENTS.keys()) + ["all"],
        help="Which experiments to run (default: all)",
    )
    parser.add_argument(
        "--models", nargs="+", default=["all"],
        help="Model keys to use (default: all)",
    )
    parser.add_argument(
        "--temperatures", nargs="+", type=float, default=None,
        help="Temperatures to test (default: config.TEMPERATURES)",
    )
    parser.add_argument(
        "--runs", type=int, default=None,
        help="Runs per condition per temperature (default: config.RUNS_PER_CONDITION)",
    )
    parser.add_argument(
        "--variants", type=int, default=5,
        help="Number of prompt variants (default: 5)",
    )
    parser.add_argument(
        "--quick-test", action="store_true",
        help="Quick-test mode: 1 model, 2 runs, temp=0.7 only",
    )
    args = parser.parse_args()

    # Resolve experiments
    if "all" in args.experiments:
        exp_keys = list(EXPERIMENTS.keys())
    else:
        exp_keys = args.experiments

    # Resolve models
    from config import MODELS as MODEL_REGISTRY
    if "all" in args.models:
        models = list(MODEL_REGISTRY.keys())
    else:
        models = args.models

    # Quick-test overrides
    if args.quick_test:
        models = [models[0]]  # first model only
        temperatures = [0.7]
        runs = 2
        variants = 1
        print("-" * 60)
        print("  [QUICK-TEST MODE]")
        print(f"  Model: {models[0]} | Runs: 2 | Temp: 0.7 | Variants: 1")
        print("-" * 60)
    else:
        temperatures = args.temperatures
        runs = args.runs
        variants = args.variants

    # Run experiments
    for exp_key in exp_keys:
        print(f"\n{'=' * 60}")
        doc = EXPERIMENTS[exp_key].__doc__ or exp_key
        print(f"  Running {exp_key.upper()}: {doc.strip().split(chr(10))[0]}")
        print(f"{'=' * 60}")

        kwargs = {"models": models, "prompt_variants": variants}
        if temperatures is not None:
            kwargs["temperatures"] = temperatures
        if runs is not None:
            kwargs["runs_per_condition"] = runs

        experiment = EXPERIMENTS[exp_key](**kwargs)
        experiment.run()
        experiment.save_results()

    print(f"\n{'-' * 60}")
    print("  [OK] All requested experiments complete.")
    print(f"{'-' * 60}")


if __name__ == "__main__":
    main()
