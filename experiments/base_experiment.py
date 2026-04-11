"""
Base Experiment Class
=====================
Handles the common experiment loop: iterate over models × temperatures ×
conditions × prompt variants × runs.  Writes JSONL for resumability,
runs linguistic analysis, and exports CSV / Parquet.
"""

import os
import json
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Tuple, Optional

import pandas as pd
from tqdm import tqdm

from models import ReplicateModel
from parsing.response_parser import parse_response, parse_response_extended
from parsing.linguistic_analysis import analyze_text
from config import (
    MODELS, TEMPERATURES, RUNS_PER_CONDITION, RUNS_PER_CONDITION_TEMP0,
    NUM_PROMPT_VARIANTS, RAW_DIR, PROCESSED_DIR,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  TRIAL RESULT DATACLASS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TrialResult:
    # Experiment metadata
    experiment_id: str = ""
    experiment_name: str = ""
    trial_id: str = ""
    timestamp: str = ""
    # Model
    model_key: str = ""
    model_id: str = ""
    temperature: float = 0.7
    # Conditions
    condition_identifiability: str = ""      # identifiable | statistical | combined
    condition_intervention: str = "none"     # none | teaching | frame_more | frame_less | frame_normative
    condition_prime: str = "none"            # none | calculate | feel
    condition_cot: str = "none"             # none | standard | empathetic | utilitarian
    condition_persona: str = "none"         # none | participant | advisor
    condition_prompt_frame: str = "first_person"
    # Stimulus
    prompt_variant_id: int = 0
    stimulus_text: str = ""
    full_prompt: str = ""
    system_prompt: str = ""
    # Run
    run_number: int = 0
    # Parsed response
    donation_amount: Optional[int] = None
    rating_upsetting: Optional[int] = None
    rating_sympathetic: Optional[int] = None
    rating_moral_responsibility: Optional[int] = None
    rating_touched: Optional[int] = None
    rating_appropriate: Optional[int] = None
    feelings_composite: Optional[float] = None
    reasoning_text: str = ""
    # Allocation (Exp4)
    rokia_donation: Optional[float] = None
    general_fund: Optional[float] = None
    amount_kept: Optional[float] = None
    # Meta-knowledge (Exp2)
    meta_awareness: Optional[bool] = None
    meta_influence_text: str = ""
    # Parsing
    parse_success: bool = False
    parse_method: str = ""
    raw_response: str = ""
    # Linguistic features
    word_count: Optional[int] = None
    sympathy_density: Optional[float] = None
    utilitarian_density: Optional[float] = None
    hedging_density: Optional[float] = None
    sentiment_polarity: Optional[float] = None
    sentiment_subjectivity: Optional[float] = None
    emotion_vs_logic_ratio: Optional[float] = None
    reasoning_type: Optional[str] = None
    # API
    latency_seconds: Optional[float] = None
    cached: bool = False
    # Numbing (Exp7)
    n_victims: Optional[int] = None
    contextualized: Optional[bool] = None
    # ── Singularity experiment fields (Exp8-9) ────────────────────────────
    singularity: str = ""              # "single", "group", ""
    identification_level: str = ""     # "unidentified", "age", "age_name", "full", etc.
    victim_name: str = ""              # name of specific victim shown
    victim_index: int = -1             # index in CANONICAL_VICTIMS
    # Cultural distance (Exp10)
    cultural_distance: str = ""        # "near", "middle", "far", ""
    # ── Extended emotion ratings (1-7, Exp8-10) ──────────────────────────
    rating_worried: Optional[int] = None
    rating_upset: Optional[int] = None
    rating_sad: Optional[int] = None
    rating_disturbed: Optional[int] = None
    rating_troubled: Optional[int] = None
    distress_composite: Optional[float] = None
    rating_sympathy_7: Optional[int] = None
    rating_compassion: Optional[int] = None
    rating_tender: Optional[int] = None
    rating_moved: Optional[int] = None
    rating_softhearted: Optional[int] = None
    empathy_composite: Optional[float] = None
    rating_moral_responsibility_7: Optional[int] = None
    rating_appropriate_7: Optional[int] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  BASE EXPERIMENT
# ═══════════════════════════════════════════════════════════════════════════════

class BaseExperiment:
    """
    Subclasses implement:
        get_experiment_name() -> str
        get_conditions()      -> List[Dict]
        build_prompt(condition, variant_id) -> Tuple[str, str]  (prompt, system_prompt)

    Optional overrides:
        get_experiment_type(condition) -> str   (for parser: "standard" | "meta" | "allocation")
        use_all_variants(condition)    -> bool  (False → use only variant 0)
    """

    def __init__(
        self,
        models: List[str] | None = None,
        temperatures: List[float] | None = None,
        runs_per_condition: int | None = None,
        prompt_variants: int = NUM_PROMPT_VARIANTS,
    ):
        self.model_client = ReplicateModel()
        self.models = models or list(MODELS.keys())
        self.temperatures = temperatures or TEMPERATURES
        self.runs = runs_per_condition or RUNS_PER_CONDITION
        self.prompt_variants = prompt_variants
        self.results: List[TrialResult] = []
        self.experiment_name = self.get_experiment_name()
        self.experiment_id = f"{self.experiment_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self.output_path = os.path.join(RAW_DIR, f"{self.experiment_name}.jsonl")

    # ── Abstract methods ─────────────────────────────────────────────────

    def get_experiment_name(self) -> str:
        raise NotImplementedError

    def get_conditions(self) -> List[Dict]:
        raise NotImplementedError

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        raise NotImplementedError

    def get_experiment_type(self, condition: Dict) -> str:
        return "standard"

    def use_all_variants(self, condition: Dict) -> bool:
        return True

    # ── Main run loop ────────────────────────────────────────────────────

    def run(self):
        existing_ids = self._check_resumability()
        conditions = self.get_conditions()

        total_trials = self._estimate_total(conditions)
        pbar = tqdm(total=total_trials, desc=self.experiment_name, unit="trial")

        for model_key in self.models:
            for temperature in self.temperatures:
                n_runs = RUNS_PER_CONDITION_TEMP0 if temperature == 0.0 else self.runs
                for condition in conditions:
                    n_variants = self.prompt_variants if self.use_all_variants(condition) else 1
                    for variant_id in range(n_variants):
                        for run_number in range(n_runs):
                            trial_id = self._make_trial_id(
                                model_key, temperature, condition, variant_id, run_number
                            )
                            if trial_id in existing_ids:
                                pbar.update(1)
                                continue

                            result = self._run_single_trial(
                                model_key, temperature, condition,
                                variant_id, run_number, trial_id,
                            )
                            self.results.append(result)
                            self._append_jsonl(result)
                            pbar.update(1)

        pbar.close()
        print(f"\n[DONE] {self.experiment_name} complete - "
              f"{len(self.results)} new trials | "
              f"API stats: {self.model_client.stats()}")

    # ── Single trial ─────────────────────────────────────────────────────

    def _run_single_trial(
        self, model_key: str, temperature: float, condition: Dict,
        variant_id: int, run_number: int, trial_id: str,
    ) -> TrialResult:
        prompt, system_prompt = self.build_prompt(condition, variant_id)
        exp_type = self.get_experiment_type(condition)

        # API call
        api_result = self.model_client.generate(
            model_key=model_key,
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )

        raw_text = api_result["response_text"]

        # Parse — use extended parser for experiments 8-10
        if exp_type == "extended":
            parsed = parse_response_extended(raw_text)
        else:
            parsed = parse_response(raw_text, experiment_type=exp_type)

        # Linguistic analysis
        ling = analyze_text(parsed.reasoning_text) if parsed.reasoning_text else None

        # Trial metadata from experiment subclass
        extra = {}
        if hasattr(self, "get_trial_metadata"):
            extra = self.get_trial_metadata(condition, variant_id)

        # Build trial result
        tr = TrialResult(
            experiment_id=self.experiment_id,
            experiment_name=self.experiment_name,
            trial_id=trial_id,
            timestamp=api_result["timestamp"],
            model_key=model_key,
            model_id=api_result["model_id"],
            temperature=temperature,
            condition_identifiability=condition.get("identifiability", ""),
            condition_intervention=condition.get("intervention", "none"),
            condition_prime=condition.get("prime", "none"),
            condition_cot=condition.get("cot", "none"),
            condition_persona=condition.get("persona", "none"),
            condition_prompt_frame=condition.get("prompt_frame", "first_person"),
            prompt_variant_id=variant_id,
            stimulus_text=condition.get("_stimulus_text", ""),
            full_prompt=prompt,
            system_prompt=system_prompt,
            run_number=run_number,
            # Core parsed fields
            donation_amount=parsed.donation_amount,
            rating_upsetting=parsed.rating_upsetting,
            rating_sympathetic=parsed.rating_sympathetic,
            rating_moral_responsibility=parsed.rating_moral_responsibility,
            rating_touched=parsed.rating_touched,
            rating_appropriate=parsed.rating_appropriate,
            feelings_composite=parsed.feelings_composite,
            reasoning_text=parsed.reasoning_text,
            # Allocation
            rokia_donation=parsed.rokia_donation,
            general_fund=parsed.general_fund,
            amount_kept=parsed.kept,
            # Meta-knowledge
            meta_awareness=parsed.meta_awareness,
            meta_influence_text=parsed.meta_influence_text,
            # Parsing
            parse_success=parsed.parse_success,
            parse_method=parsed.parse_method,
            raw_response=raw_text,
            # Linguistic
            word_count=ling.word_count if ling else None,
            sympathy_density=ling.sympathy_density if ling else None,
            utilitarian_density=ling.utilitarian_density if ling else None,
            hedging_density=ling.hedging_density if ling else None,
            sentiment_polarity=ling.sentiment_polarity if ling else None,
            sentiment_subjectivity=ling.sentiment_subjectivity if ling else None,
            emotion_vs_logic_ratio=ling.emotion_vs_logic_ratio if ling else None,
            reasoning_type=ling.reasoning_type if ling else None,
            # API
            latency_seconds=api_result["latency_seconds"],
            cached=api_result["cached"],
            # Numbing
            n_victims=condition.get("n_victims"),
            contextualized=condition.get("contextualized"),
            # Singularity
            singularity=condition.get("singularity", ""),
            identification_level=condition.get("identification_level", ""),
            victim_name=extra.get("victim_name", ""),
            victim_index=extra.get("victim_index", -1),
            # Cultural distance
            cultural_distance=condition.get("cultural_distance", ""),
            # Extended emotion ratings
            rating_worried=parsed.rating_worried,
            rating_upset=parsed.rating_upset,
            rating_sad=parsed.rating_sad,
            rating_disturbed=parsed.rating_disturbed,
            rating_troubled=parsed.rating_troubled,
            distress_composite=parsed.distress_composite,
            rating_sympathy_7=parsed.rating_sympathy,
            rating_compassion=parsed.rating_compassion,
            rating_tender=parsed.rating_tender,
            rating_moved=parsed.rating_moved,
            rating_softhearted=parsed.rating_softhearted,
            empathy_composite=parsed.empathy_composite,
            rating_moral_responsibility_7=parsed.rating_moral_responsibility_7,
            rating_appropriate_7=parsed.rating_appropriate_7,
        )
        return tr

    # ── Trial ID ─────────────────────────────────────────────────────────

    def _make_trial_id(self, model_key, temperature, condition, variant_id, run_number):
        parts = [
            self.experiment_name,
            model_key,
            f"t{temperature}",
            condition.get("identifiability", "x"),
            condition.get("intervention", "x"),
            condition.get("prime", "x"),
            condition.get("cot", "x"),
            condition.get("persona", "x"),
            condition.get("prompt_frame", "x"),
            f"v{variant_id}",
            f"r{run_number}",
        ]
        # Add experiment-specific keys
        if "n_victims" in condition:
            parts.append(f"n{condition['n_victims']}")
        if "contextualized" in condition:
            parts.append(f"ctx{condition['contextualized']}")
        if "singularity" in condition:
            parts.append(f"sg{condition['singularity']}")
        if "identification_level" in condition:
            parts.append(f"id{condition['identification_level']}")
        if "cultural_distance" in condition:
            parts.append(f"cd{condition['cultural_distance']}")
        return "__".join(str(p) for p in parts)

    # ── Resumability ─────────────────────────────────────────────────────

    def _check_resumability(self) -> set:
        existing = set()
        if os.path.exists(self.output_path):
            with open(self.output_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        raw = str(obj.get("raw_response", ""))
                        if raw.startswith("API_ERROR"):
                            continue
                        if obj.get("parse_success") is False and not raw.strip():
                            # API failed silently resulting in an empty string
                            continue
                        if obj.get("trial_id"):
                            existing.add(obj.get("trial_id"))
                    except json.JSONDecodeError:
                        continue
            print(f"  - Resuming {self.experiment_name}: {len(existing)} existing valid trials found")
        return existing

    def _append_jsonl(self, result: TrialResult):
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(result), default=str) + "\n")

    # ── Estimate total ───────────────────────────────────────────────────

    def _estimate_total(self, conditions):
        total = 0
        for model_key in self.models:
            for temperature in self.temperatures:
                n_runs = RUNS_PER_CONDITION_TEMP0 if temperature == 0.0 else self.runs
                for condition in conditions:
                    n_variants = self.prompt_variants if self.use_all_variants(condition) else 1
                    total += n_variants * n_runs
        return total

    # ── Save ─────────────────────────────────────────────────────────────

    def save_results(self):
        df = self.get_dataframe()
        if df.empty:
            return
        csv_path = os.path.join(PROCESSED_DIR, f"{self.experiment_name}.csv")
        parquet_path = os.path.join(PROCESSED_DIR, f"{self.experiment_name}.parquet")
        df.to_csv(csv_path, index=False)
        df.to_parquet(parquet_path, index=False)
        print(f"  - Saved {len(df)} rows to {csv_path}")

    def get_dataframe(self) -> pd.DataFrame:
        if os.path.exists(self.output_path):
            rows = []
            with open(self.output_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return pd.DataFrame(rows)
        return pd.DataFrame([asdict(r) for r in self.results])
