# Narrative over Numbers: The Identifiable Victim Effect and its Amplification Under Alignment and Reasoning in Large Language Models

This repository contains the code and data of the paper titled "Narrative over Numbers: The Identifiable Victim Effect and its Amplification Under Alignment and Reasoning in Large Language Models."

This codebase runs behavioral experiments on LLMs via the Replicate API to test whether language models replicate the findings from Small, Loewenstein, & Slovic (2007).

## Research Questions

| # | Question |
|---|----------|
| RQ1 | Do LLMs recommend greater generosity toward identifiable victims than statistical victims? |
| RQ2 | Does deliberative processing (CoT, priming, debiasing) asymmetrically reduce sympathy toward identifiable victims? |
| RQ3 | Do LLMs exhibit the "sympathy-callousness" paradox? |
| RQ4 | How do model architecture, alignment training, and scale modulate these effects? |

## Experiments

| Exp | Name | Design |
|-----|------|--------|
| 1 | Basic IVE | 2 (identifiability) × 2 (persona) × 3 (frame) |
| 2 | Explicit Debiasing | 2 (identifiability) × 2 (intervention) + meta-knowledge probe |
| 3 | Framing | 2 (identifiability) × 3 (frame type) |
| 4 | Joint vs. Separate | 3 conditions + allocation sub-task |
| 5 | Processing Prime | 2 (identifiability) × 2 (prime: calculate/feel) |
| 6 | Chain-of-Thought | 2 (identifiability) × 4 (CoT type) — **NOVEL** |
| 7 | Psychophysical Numbing | 6 victim scales × 2 (contextualized) — **NOVEL** |
| 8 | Singularity × Identification | 2 (single vs. group) × 4 (identification levels) — **NOVEL** |
| 9 | Identification Gradient | 6-level dose-response mapping — **NOVEL** |
| 10 | Cultural Distance (Fairness) | 3 (cultural distance) × 2 (identifiability) — **NOVEL** |

## Models (16 active models)

The codebase supports an active budget-constrained set of 16 modern language models accessed via Replicate and OpenRouter across major AI labs:

- **Google**: Gemini 3.1 Pro (flagship), Gemini 2.5 Flash (efficiency)
- **Anthropic**: Claude Opus 4.6
- **OpenAI**: GPT-5.2 (flagship), GPT-OSS-20B (open-weight)
- **DeepSeek**: V3 (non-reasoning), R1 (reasoning)
- **xAI**: Grok 4
- **Qwen**: Qwen3-235B
- **Moonshot**: Kimi K2.5 *(via OpenRouter)*
- **IBM**: Granite 3.3 8B
- **Meta**: LLaMA 3 70B & 8B (both instruct and base versions for RLHF comparisons)

*(Note: The registry in `config.py` supports 40+ models, but defaults to this subset for budget optimization.)*

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key (already in api/config.json)
# Ensure api/config.json contains your REPLICATE_API_TOKEN

# 3. Quick test (2 runs, 1 model, single temperature)
python run_all.py --quick-test --experiments exp1

# 4. Run specific experiments
python run_all.py --experiments exp1 exp6 --models gpt-4o claude-4.5-sonnet

# 5. Full run (all experiments, all models)
python run_all.py

# 6. Analyze results
python analyze_all.py

# 7. Generate figures
python visualize_all.py
```

## Project Structure

```
IVE-LLM/
│
├── config.py                  # Model registry, API routing, temperature config
├── models.py                  # Replicate/OpenRouter API wrapper (cache, retry, rate-limit)
├── run_all.py                 # Master experiment runner
├── analyze_all.py             # Master analysis pipeline
├── visualize_all.py           # Master figure generator
├── test_all_models.py         # Quick connectivity test for all 16 models
├── requirements.txt           # Python dependencies
│
├── prompts/                   # ── Stimulus & Template Library ──
│   ├── stimuli.py             # All experimental stimuli, paraphrases, numbing scales
│   ├── templates.py           # Prompt templates, personas, CoT variants, rating scales
│   └── victims.py             # Canonical victim profiles & stimulus generators
│
├── experiments/               # ── Experiment Implementations ──
│   ├── base_experiment.py     # Base class with resumability & progress tracking
│   ├── exp1_basic_ive.py      # Experiment 1: Basic IVE replication
│   ├── exp2_explicit_debiasing.py
│   ├── exp3_framing.py
│   ├── exp4_joint_separate.py
│   ├── exp5_processing_prime.py
│   ├── exp6_chain_of_thought.py   # NOVEL: CoT as deliberation
│   ├── exp7_psychophysical_numbing.py  # NOVEL
│   ├── exp8_singularity.py        # NOVEL: Kogut & Ritov interaction
│   ├── exp9_identification_gradient.py  # NOVEL: 6-level dose-response
│   ├── exp10_ingroup_outgroup.py  # NOVEL: Cultural distance fairness
│   └── runner.py              # CLI experiment dispatcher
│
├── analysis/                  # ── Statistical Analysis ──
│   └── statistical_tests.py   # t-tests, ANOVA, Cohen's d, bootstrap CI, mediation
│
├── parsing/                   # ── Response Processing ──
│   ├── response_parser.py     # Multi-stage LLM response parser (exact → regex → fuzzy)
│   └── linguistic_analysis.py # Linguistic feature extraction
│
├── visualization/             # ── Figure Generation ──
│   ├── style.py               # Publication-quality plot styling & save_figure()
│   ├── plot_exp1.py – plot_exp7.py  # Per-experiment visualizations
│   ├── plot_emotion_mediation.py    # Distress vs. empathy mediation plots
│   ├── plot_cross_model.py    # Forest plot, effect heatmap, scale analysis
│   └── plot_linguistic.py     # Linguistic feature visualizations
│
├── scripts/                   # ── Utility & One-Off Scripts ──
│   ├── generate_temp_sensitivity_figures.py  # Temperature & sensitivity figures
│   ├── regenerate_distress_empathy.py       # Mediation scatter plot
│   └── extract_distress_empathy_data.py     # Data extraction utility
│
├── api/                       # ── API Configuration ──
│   └── config.json            # API keys (gitignored)
│
├── results/                   # ── Results & Analysis Reports ──
│   ├── results_global_synthesis.md          # Cross-model pooled analysis
│   ├── results_sensitivity_analysis.md      # Ceiling-exclusion sensitivity
│   ├── results_temperature_stratified.md    # Temperature stratification
│   ├── results_<model-name>.md              # Per-model result summaries (×16)
│   ├── expected_results.md                  # Pre-registration predictions
│   └── tentative_results.md                 # Early/interim findings
│
├── docs/                      # ── Paper & Documentation ──
│   ├── appendix_prompts.tex   # LaTeX appendix: full prompt catalog
│   ├── appendix_prompts.md    # Markdown version of prompt catalog
│   ├── prompts_appendix.tex   # Earlier appendix draft
│   ├── ive_figures.tex        # LaTeX figure includes for manuscript
│   ├── mathematical_formulations.md  # Statistical model specifications
│   └── research_summary.md   # Literature review & design rationale
│
├── logs/                      # ── Raw Run Logs ──
│   └── <model>_results.txt    # Raw stdout/analysis output per model (×16)
│
└── data/                      # ── Generated Data (gitignored) ──
    ├── raw/                   # JSONL trial logs
    ├── processed/             # CSV/Parquet datasets, analysis_results.json
    └── figures/               # PDF/PNG/SVG publication figures
```

## Key Design Decisions

- **Disk caching**: Every API call is cached by `SHA256(model + prompt + temperature)` — re-runs cost nothing
- **Resumability**: JSONL append mode; crashed experiments resume from where they stopped
- **Multi-stage parser**: exact → regex → fuzzy fallback handles messy LLM outputs
- **Temperatures**: Evaluated at τ=0.0 (deterministic, 3 runs) and τ=0.7 (stochastic, 10 runs)
- **Prompt variants**: 5 paraphrased versions of each stimulus for robustness analysis
- **Extended affect scales**: Experiments 8–10 use Batson's distress/empathic concern subscales (1–7)

## License

MIT — see [LICENSE](LICENSE) for details.