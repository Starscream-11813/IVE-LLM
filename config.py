"""
IVE-LLM Configuration
=====================
Central configuration for the Identifiable Victim Effect research codebase.
Loads API keys from api/config.json, defines model registry, paths, and constants.
"""

import os
import json

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
API_CONFIG_PATH = os.path.join(PROJECT_ROOT, "api", "config.json")

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FIGURES_DIR = os.path.join(DATA_DIR, "figures")
CACHE_DIR = os.path.join(PROJECT_ROOT, ".cache")

for _d in [RAW_DIR, PROCESSED_DIR, FIGURES_DIR, CACHE_DIR]:
    os.makedirs(_d, exist_ok=True)

# ── API keys ─────────────────────────────────────────────────────────────────
def _load_api_keys():
    if not os.path.exists(API_CONFIG_PATH):
        raise FileNotFoundError(
            f"API config not found at {API_CONFIG_PATH}. "
            "Create api/config.json with REPLICATE_API_TOKEN."
        )
    with open(API_CONFIG_PATH, "r") as f:
        return json.load(f)

_API_KEYS = _load_api_keys()
REPLICATE_API_TOKEN = _API_KEYS.get("REPLICATE_API_TOKEN", "")
OPENROUTER_API_KEY = _API_KEYS.get("OPENROUTER_API_KEY", "")

# ── Model registry ───────────────────────────────────────────────────────────
# Full catalog of all text-capable LLMs available on Replicate.
# Use ALL_MODELS for reference; MODELS (below) is the active budget subset.
ALL_MODELS = {
    # ── Google ────────────────────────────────────────────────────────────
    "gemini-3.1-pro":       "google/gemini-3.1-pro",
    "gemini-3-pro":         "google/gemini-3-pro",
    "gemini-2.5-flash":     "google/gemini-2.5-flash",
    # ── Anthropic ─────────────────────────────────────────────────────────
    "claude-opus-4.6":      "anthropic/claude-opus-4.6",
    "claude-4.5-sonnet":    "anthropic/claude-4.5-sonnet",
    "claude-4.5-haiku":     "anthropic/claude-4.5-haiku",
    "claude-4-sonnet":      "anthropic/claude-4-sonnet",
    "claude-3.7-sonnet":    "anthropic/claude-3.7-sonnet",
    "claude-3.5-haiku":     "anthropic/claude-3.5-haiku",
    # ── OpenAI ────────────────────────────────────────────────────────────
    "gpt-5.2":              "openai/gpt-5.2",
    "gpt-5":                "openai/gpt-5",
    "gpt-5-mini":           "openai/gpt-5-mini",
    "gpt-5-nano":           "openai/gpt-5-nano",
    "gpt-4.1":              "openai/gpt-4.1",
    "gpt-4.1-mini":         "openai/gpt-4.1-mini",
    "gpt-4.1-nano":         "openai/gpt-4.1-nano",
    "gpt-4o":               "openai/gpt-4o",
    "gpt-4o-mini":          "openai/gpt-4o-mini",
    "o4-mini":              "openai/o4-mini",
    "o1":                   "openai/o1",
    "o1-mini":              "openai/o1-mini",
    "gpt-oss-120b":         "openai/gpt-oss-120b",
    "gpt-oss-20b":          "openai/gpt-oss-20b",
    # ── DeepSeek ──────────────────────────────────────────────────────────
    "deepseek-v3":          "deepseek-ai/deepseek-v3",
    "deepseek-v3.1":        "deepseek-ai/deepseek-v3.1",
    "deepseek-r1":          "deepseek-ai/deepseek-r1",
    # ── xAI ───────────────────────────────────────────────────────────────
    "grok-4":               "xai/grok-4",
    # ── Qwen ──────────────────────────────────────────────────────────────
    "qwen3-235b":           "qwen/qwen3-235b-a22b-instruct-2507",
    # ── Moonshot ──────────────────────────────────────────────────────────
    "kimi-k2.5":            "moonshotai/kimi-k2.5",
    # ── IBM ───────────────────────────────────────────────────────────────
    "granite-3.3-8b":       "ibm-granite/granite-3.3-8b-instruct",
    # ── Meta LLaMA ────────────────────────────────────────────────────────
    "llama3-70b-instruct":  "meta/meta-llama-3-70b-instruct",
    "llama3-70b-base":      "meta/meta-llama-3-70b",
    "llama3-8b-instruct":   "meta/meta-llama-3-8b-instruct",
    "llama3-8b-base":       "meta/meta-llama-3-8b",
    # ── Google DeepMind ───────────────────────────────────────────────────
    "gemma-2b-it":          "google-deepmind/gemma-2b-it",
    # ── Stability AI ─────────────────────────────────────────────────────
    "stablelm-7b":          "stability-ai/stablelm-tuned-alpha-7b",
    # ── Replicate hosted ─────────────────────────────────────────────────
    "flan-t5-xl":           "replicate/flan-t5-xl",
    "llama-7b":             "replicate/llama-7b",
}

# ── Active model set (budget-constrained) ────────────────────────────────────
# 1 model per company + LLaMA instruct/base pairs for RLHF comparison.
# Switch to ALL_MODELS for a full-scale run.
_ACTIVE_KEYS = [
    "gemini-3.1-pro",
    "gemini-2.5-flash",
    "claude-opus-4.6",
    "gpt-5.2",
    "gpt-oss-20b",
    "gpt-oss-120b",
    "deepseek-v3",
    "deepseek-r1",
    "grok-4",
    "qwen3-235b",
    "granite-3.3-8b",
    "llama3-70b-instruct",
    "llama3-70b-base",
    "llama3-8b-instruct",
    "llama3-8b-base",
]
MODELS = {k: ALL_MODELS[k] for k in _ACTIVE_KEYS}

# Approximate parameter counts (billions) for cross-model analysis
MODEL_PARAMS = {
    # Google
    "gemini-3.1-pro": 600,    # estimated
    "gemini-3-pro": 500,      # estimated
    "gemini-2.5-flash": 200,  # estimated
    # Anthropic
    "claude-opus-4.6": 500,   # estimated
    "claude-4.5-sonnet": 300, # estimated
    "claude-4.5-haiku": 70,   # estimated
    "claude-4-sonnet": 250,   # estimated
    "claude-3.7-sonnet": 200, # estimated
    "claude-3.5-haiku": 50,   # estimated
    # OpenAI
    "gpt-5.2": 800,           # estimated
    "gpt-5": 700,             # estimated
    "gpt-5-mini": 200,        # estimated
    "gpt-5-nano": 50,         # estimated
    "gpt-4.1": 500,           # estimated
    "gpt-4.1-mini": 150,      # estimated
    "gpt-4.1-nano": 30,       # estimated
    "gpt-4o": 200,            # estimated
    "gpt-4o-mini": 70,        # estimated
    "o4-mini": 100,           # estimated
    "o1": 300,                # estimated
    "o1-mini": 100,           # estimated
    "gpt-oss-120b": 120,
    "gpt-oss-20b": 20,
    # DeepSeek
    "deepseek-v3": 671,
    "deepseek-v3.1": 671,
    "deepseek-r1": 671,
    # xAI
    "grok-4": 600,            # estimated
    # Qwen
    "qwen3-235b": 235,
    # Moonshot
    "kimi-k2.5": 300,         # estimated
    # IBM
    "granite-3.3-8b": 8,
    # Meta
    "llama3-70b-instruct": 70,
    "llama3-70b-base": 70,
    "llama3-8b-instruct": 8,
    "llama3-8b-base": 8,
    # Google DeepMind
    "gemma-2b-it": 2,
    # Stability AI
    "stablelm-7b": 7,
    # Replicate
    "flan-t5-xl": 3,
    "llama-7b": 7,
}

# ── Generation parameters ────────────────────────────────────────────────────
TEMPERATURES = [0.0, 0.7]
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 1024
TOP_P = 0.95

# ── Experiment parameters ────────────────────────────────────────────────────
RUNS_PER_CONDITION = 10          # per temperature; temp=0 uses only 3
RUNS_PER_CONDITION_TEMP0 = 3     # deterministic check
NUM_PROMPT_VARIANTS = 3          # variants 0-2
RANDOM_SEED = 42

# ── Rate limiting ────────────────────────────────────────────────────────────
MAX_REQUESTS_PER_MINUTE = 10
