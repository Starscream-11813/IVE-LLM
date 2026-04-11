"""
Experiment 10: In-group / Out-group Moderation of IVE in LLMs

Tests whether LLMs show differential sympathy based on victim cultural proximity
to the dominant training data (English-language, Western-centric).

Design: 3 (cultural distance: near/US, middle/Eastern Europe, far/Sub-Saharan Africa)
        × 2 (identifiability: identifiable single vs statistical)

Implications for AI fairness:
  - Do LLMs show more sympathy for Western victims?
  - Does the IVE magnitude vary by victim cultural background?
  - Relevant for LLM deployment in humanitarian contexts.

Uses extended rating items.
"""

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import INGROUP_OUTGROUP_STIMULI
from prompts.templates import RATING_ITEMS_EXTENDED, BASE_DONATION_PROMPT_EXTENDED, PERSONA_PARTICIPANT


class Exp10IngroupOutgroup(BaseExperiment):
    """In-group / out-group moderation of the identifiable victim effect."""

    def get_experiment_name(self):
        return "exp10_ingroup_outgroup"

    def get_experiment_type(self, condition):
        return "extended"

    def get_conditions(self):
        conditions = []
        for distance in ["near", "middle", "far"]:
            for identifiability in ["identifiable", "statistical"]:
                conditions.append({
                    "identifiability": identifiability,
                    "cultural_distance": distance,
                    "singularity": "single" if identifiability == "identifiable" else "statistical",
                    "identification_level": "full" if identifiability == "identifiable" else "statistical",
                    "intervention": "none",
                    "prime": "none",
                    "cot": "none",
                    "persona": "participant",
                    "prompt_frame": "first_person",
                    "n_victims": 1,
                })
        return conditions  # 6 conditions

    def build_prompt(self, condition, variant_id):
        distance = condition["cultural_distance"]
        identifiability = condition["identifiability"]
        stimulus_text = INGROUP_OUTGROUP_STIMULI[distance][identifiability]

        prompt = BASE_DONATION_PROMPT_EXTENDED.format(
            stimulus_text=stimulus_text,
            rating_section=RATING_ITEMS_EXTENDED,
        )
        system_prompt = PERSONA_PARTICIPANT
        return prompt, system_prompt

    def get_trial_metadata(self, condition, variant_id):
        return {
            "cultural_distance": condition["cultural_distance"],
        }
