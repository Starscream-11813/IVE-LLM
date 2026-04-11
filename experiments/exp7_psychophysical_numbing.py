"""
Experiment 7 — Psychophysical Numbing (NOVEL)
==============================================
Design: 6 (victim_count: 1, 10, 100, 1000, 100000, 3000000)
      × 2 (contextualized: yes / no)
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import NUMBING_SCALES, NUMBING_CONTEXTUALIZED
from prompts.templates import BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES


class Exp7PsychophysicalNumbing(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp7_psychophysical_numbing"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for n_victims in sorted(NUMBING_SCALES.keys()):
            for contextualized in [False, True]:
                scale = NUMBING_CONTEXTUALIZED if contextualized else NUMBING_SCALES
                entry = scale[n_victims]
                conditions.append({
                    "identifiability": entry["type"],
                    "intervention": "none",
                    "prime": "none",
                    "cot": "none",
                    "persona": "participant",
                    "prompt_frame": "first_person",
                    "n_victims": n_victims,
                    "contextualized": contextualized,
                    "_stimulus_text": entry["text"],
                })
        return conditions

    def use_all_variants(self, condition: Dict) -> bool:
        # No paraphrase variants for numbing; stimuli are predefined per scale
        return False

    def build_prompt(self, condition: Dict, variant_id: int) -> Tuple[str, str]:
        stimulus = condition["_stimulus_text"]

        prompt = BASE_DONATION_PROMPT.format(
            intervention_text="",
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES["first_person"],
            cot_instruction="",
        )

        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
