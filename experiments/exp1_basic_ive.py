"""
Experiment 1 — Basic Identifiable Victim Effect
=================================================
Design: 2 (identifiability: identifiable vs statistical)
      × 2 (persona: none, participant)
      × 3 (frame: first_person, third_person, advisory)
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS
from prompts.templates import (
    BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES,
)


class Exp1BasicIVE(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp1_basic_ive"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical"]:
            for persona in ["none", "participant"]:
                for frame in ["first_person", "third_person", "advisory"]:
                    conditions.append({
                        "identifiability": identifiability,
                        "intervention": "none",
                        "prime": "none",
                        "cot": "none",
                        "persona": persona,
                        "prompt_frame": frame,
                    })
        return conditions

    def use_all_variants(self, condition: Dict) -> bool:
        # Full 5 variants only for core condition (no_persona + first_person)
        return (
            condition["persona"] == "none"
            and condition["prompt_frame"] == "first_person"
        )

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        # Select stimulus
        if condition["identifiability"] == "identifiable":
            stimulus = IDENTIFIABLE_VARIANTS[variant_id]
        else:
            stimulus = STATISTICAL_VARIANTS[variant_id]

        # Build prompt
        prompt = BASE_DONATION_PROMPT.format(
            intervention_text="",
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES[condition["prompt_frame"]],
            cot_instruction="",
        )

        system_prompt = PERSONA_MAP.get(condition["persona"], "")
        return prompt, system_prompt
