"""
Experiment 9: Fine-grained Identification Gradient

Extends Kogut & Ritov's 4-level identification to 6 levels, testing the
dose-response curve of identification on LLM sympathy.

Levels (single victim only):
  1. bare           – "a child in need"
  2. age            – "a 7-year-old child"
  3. age_gender     – "a 7-year-old girl"
  4. age_gender_name         – "Rokia, a 7-year-old girl"
  5. age_gender_name_location – "Rokia, a 7-year-old girl from Mali"
  6. full_narrative           – full backstory, physical desc, weight

Design: 6 (identification levels) × N models.  Uses extended rating items.
"""

from experiments.base_experiment import BaseExperiment
from prompts.victims import CANONICAL_VICTIMS, generate_single_stimulus
from prompts.templates import RATING_ITEMS_EXTENDED, BASE_DONATION_PROMPT_EXTENDED, PERSONA_PARTICIPANT


class Exp9IdentificationGradient(BaseExperiment):
    """Fine-grained identification gradient (6-level dose-response)."""

    LEVELS = [
        "bare", "age", "age_gender", "age_gender_name",
        "age_gender_name_location", "full_narrative",
    ]

    def get_experiment_name(self):
        return "exp9_identification_gradient"

    def get_experiment_type(self, condition):
        return "extended"

    def get_conditions(self):
        conditions = []
        for level in self.LEVELS:
            conditions.append({
                "identifiability": f"single_{level}",
                "singularity": "single",
                "identification_level": level,
                "intervention": "none",
                "prime": "none",
                "cot": "none",
                "persona": "participant",
                "prompt_frame": "first_person",
                "n_victims": 1,
            })
        return conditions  # 6 conditions

    def build_prompt(self, condition, variant_id):
        level = condition["identification_level"]
        victim_index = variant_id % len(CANONICAL_VICTIMS)
        victim = CANONICAL_VICTIMS[victim_index]
        stimulus_text = generate_single_stimulus(victim, level)

        prompt = BASE_DONATION_PROMPT_EXTENDED.format(
            stimulus_text=stimulus_text,
            rating_section=RATING_ITEMS_EXTENDED,
        )
        system_prompt = PERSONA_PARTICIPANT
        return prompt, system_prompt

    def get_trial_metadata(self, condition, variant_id):
        victim_index = variant_id % len(CANONICAL_VICTIMS)
        victim = CANONICAL_VICTIMS[victim_index]
        return {
            "victim_name": victim.name,
            "victim_age": victim.age,
            "victim_gender": victim.gender,
            "victim_index": victim_index,
        }
