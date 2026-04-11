"""
Experiment 8: Singularity × Identification Interaction (Kogut & Ritov 2005)

Tests whether LLMs show the human pattern where the identified victim effect
is restricted to single victims — groups of identified victims do NOT receive
more than groups of unidentified ones.

Design: 2 (singularity: single vs group of 8) × 4 (identification:
        unidentified, age, age+name, full_description)

Uses the EXTENDED rating items (distress + empathic concern subscales).
"""

from experiments.base_experiment import BaseExperiment
from prompts.victims import CANONICAL_VICTIMS, generate_single_stimulus, generate_group_stimulus
from prompts.templates import RATING_ITEMS_EXTENDED, BASE_DONATION_PROMPT_EXTENDED, PERSONA_PARTICIPANT


class Exp8Singularity(BaseExperiment):
    """Singularity × Identification interaction (Kogut & Ritov 2005 replication)."""

    def get_experiment_name(self):
        return "exp8_singularity"

    def get_experiment_type(self, condition):
        return "extended"

    def get_conditions(self):
        conditions = []
        identification_levels = ["unidentified", "age", "age_name", "full"]
        for singularity in ["single", "group"]:
            for identification in identification_levels:
                conditions.append({
                    "identifiability": f"{singularity}_{identification}",
                    "singularity": singularity,
                    "identification_level": identification,
                    "intervention": "none",
                    "prime": "none",
                    "cot": "none",
                    "persona": "participant",
                    "prompt_frame": "first_person",
                    "n_victims": 1 if singularity == "single" else 8,
                })
        return conditions  # 8 conditions

    def build_prompt(self, condition, variant_id):
        singularity = condition["singularity"]
        identification = condition["identification_level"]

        if singularity == "single":
            victim_index = variant_id % len(CANONICAL_VICTIMS)
            victim = CANONICAL_VICTIMS[victim_index]
            stimulus_text = generate_single_stimulus(victim, identification)
        else:
            stimulus_text = generate_group_stimulus(CANONICAL_VICTIMS, identification)

        prompt = BASE_DONATION_PROMPT_EXTENDED.format(
            stimulus_text=stimulus_text,
            rating_section=RATING_ITEMS_EXTENDED,
        )
        system_prompt = PERSONA_PARTICIPANT
        return prompt, system_prompt

    def get_trial_metadata(self, condition, variant_id):
        metadata = {}
        if condition["singularity"] == "single":
            victim_index = variant_id % len(CANONICAL_VICTIMS)
            victim = CANONICAL_VICTIMS[victim_index]
            metadata["victim_name"] = victim.name
            metadata["victim_age"] = victim.age
            metadata["victim_gender"] = victim.gender
            metadata["victim_index"] = victim_index
        else:
            metadata["victim_name"] = "group_of_8"
            metadata["victim_index"] = -1
        return metadata
