"""
Experiment 6 — Chain-of-Thought as Deliberation (NOVEL)
========================================================
Design: 2 (identifiability) × 4 (CoT: none, standard, empathetic, utilitarian)
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS
from prompts.templates import (
    BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES, COT_VARIANTS,
)


class Exp6ChainOfThought(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp6_chain_of_thought"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical"]:
            for cot in ["none", "standard", "empathetic", "utilitarian"]:
                conditions.append({
                    "identifiability": identifiability,
                    "intervention": "none",
                    "prime": "none",
                    "cot": cot,
                    "persona": "participant",
                    "prompt_frame": "first_person",
                })
        return conditions

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        if condition["identifiability"] == "identifiable":
            stimulus = IDENTIFIABLE_VARIANTS[variant_id]
        else:
            stimulus = STATISTICAL_VARIANTS[variant_id]

        cot_text = COT_VARIANTS[condition["cot"]]

        prompt = BASE_DONATION_PROMPT.format(
            intervention_text="",
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES["first_person"],
            cot_instruction=cot_text,
        )

        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
