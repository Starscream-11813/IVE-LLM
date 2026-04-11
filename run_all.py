"""
IVE-LLM Master Experiment Runner
==================================
Usage:
    python run_all.py                          # Run all experiments
    python run_all.py --experiments exp1 exp6   # Run specific experiments
    python run_all.py --quick-test              # Quick test mode (2 runs, 1 model)
    python run_all.py --models llama3-70b       # Specific models
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.runner import main

if __name__ == "__main__":
    main()
