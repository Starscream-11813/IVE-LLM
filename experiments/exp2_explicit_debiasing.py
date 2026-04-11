"""
Experiment 2 — Explicit Debiasing (Teaching Intervention)
==========================================================
Design: 2 (identifiability) × 2 (intervention: teaching vs none)
Includes meta-knowledge probe appended after main response.
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import (
    STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS, TEACHING_INTERVENTION,
)
from prompts.templates import (
    BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES, META_KNOWLEDGE_PROBE,
)


class Exp2ExplicitDebiasing(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp2_explicit_debiasing"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical"]:
            for intervention in ["none", "teaching"]:
                conditions.append({
                    "identifiability": identifiability,
                    "intervention": intervention,
                    "prime": "none",
                    "cot": "none",
                    "persona": "participant",
                    "prompt_frame": "first_person",
                })
        return conditions

    def get_experiment_type(self, condition: Dict) -> str:
        return "meta"

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        if condition["identifiability"] == "identifiable":
            stimulus = IDENTIFIABLE_VARIANTS[variant_id]
        else:
            stimulus = STATISTICAL_VARIANTS[variant_id]

        intervention_text = (
            TEACHING_INTERVENTION if condition["intervention"] == "teaching" else ""
        )

        prompt = BASE_DONATION_PROMPT.format(
            intervention_text=intervention_text,
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES["first_person"],
            cot_instruction="",
        )
        # Append meta-knowledge probe
        prompt += META_KNOWLEDGE_PROBE

        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
