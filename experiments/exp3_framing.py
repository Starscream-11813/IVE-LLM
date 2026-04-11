"""
Experiment 3 — Framing the Intervention
========================================
Design: 2 (identifiability) × 3 (frame: more_identifiable, less_statistical, normative)
All conditions receive an intervention; we test whether the frame matters.
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import (
    STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS,
    FRAME_MORE_IDENTIFIABLE, FRAME_LESS_STATISTICAL, FRAME_NORMATIVE,
)
from prompts.templates import BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES

_FRAMES = {
    "frame_more": FRAME_MORE_IDENTIFIABLE,
    "frame_less": FRAME_LESS_STATISTICAL,
    "frame_normative": FRAME_NORMATIVE,
}


class Exp3Framing(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp3_framing"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical"]:
            for frame_key in ["frame_more", "frame_less", "frame_normative"]:
                conditions.append({
                    "identifiability": identifiability,
                    "intervention": frame_key,
                    "prime": "none",
                    "cot": "none",
                    "persona": "participant",
                    "prompt_frame": "first_person",
                })
        return conditions

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        if condition["identifiability"] == "identifiable":
            stimulus = IDENTIFIABLE_VARIANTS[variant_id]
        else:
            stimulus = STATISTICAL_VARIANTS[variant_id]

        intervention_text = _FRAMES[condition["intervention"]]

        prompt = BASE_DONATION_PROMPT.format(
            intervention_text=intervention_text,
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES["first_person"],
            cot_instruction="",
        )
        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
