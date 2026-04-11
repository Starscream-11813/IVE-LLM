"""
Experiment 4 — Joint vs. Separate Presentation
================================================
Conditions:
  1. identifiable  (standard donation prompt)
  2. statistical   (standard donation prompt)
  3. combined      (both stimuli, standard donation prompt)
  4. combined_allocation (allocation prompt: split $5 between Rokia & general fund)
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import (
    STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS, COMBINED_TEMPLATE,
)
from prompts.templates import (
    BASE_DONATION_PROMPT, ALLOCATION_PROMPT, PERSONA_MAP, DONATION_FRAMES,
)


class Exp4JointSeparate(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp4_joint_separate"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical", "combined"]:
            conditions.append({
                "identifiability": identifiability,
                "intervention": "none",
                "prime": "none",
                "cot": "none",
                "persona": "participant",
                "prompt_frame": "first_person",
                "task_type": "donation",
            })
        # Allocation sub-task for combined condition
        conditions.append({
            "identifiability": "combined",
            "intervention": "none",
            "prime": "none",
            "cot": "none",
            "persona": "participant",
            "prompt_frame": "first_person",
            "task_type": "allocation",
        })
        return conditions

    def get_experiment_type(self, condition: Dict) -> str:
        return "allocation" if condition.get("task_type") == "allocation" else "standard"

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        identifiability = condition["identifiability"]

        if identifiability == "identifiable":
            stimulus = IDENTIFIABLE_VARIANTS[variant_id]
        elif identifiability == "statistical":
            stimulus = STATISTICAL_VARIANTS[variant_id]
        else:  # combined
            stimulus = COMBINED_TEMPLATE.format(
                statistical_text=STATISTICAL_VARIANTS[variant_id],
                identifiable_text=IDENTIFIABLE_VARIANTS[variant_id],
            )

        if condition.get("task_type") == "allocation":
            # Use allocation prompt instead of standard donation prompt
            prompt = (
                "You have just earned $5.00 for completing a survey. "
                "You now have the opportunity to donate any portion of this money "
                "to the organization Save the Children.\n\n"
                f"{stimulus}\n\n"
                f"{ALLOCATION_PROMPT}"
            )
        else:
            prompt = BASE_DONATION_PROMPT.format(
                intervention_text="",
                stimulus_text=stimulus,
                donation_question=DONATION_FRAMES["first_person"],
                cot_instruction="",
            )

        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
