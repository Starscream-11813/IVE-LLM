"""
Experiment 5 — Processing Mode Priming
========================================
Design: 2 (identifiability) × 2 (prime: calculate vs feel)
Prime task is presented BEFORE the donation request.
"""

from typing import Dict, List, Tuple

from experiments.base_experiment import BaseExperiment
from prompts.stimuli import (
    STATISTICAL_VARIANTS, IDENTIFIABLE_VARIANTS,
    CALCULATION_PRIME, FEELING_PRIME,
)
from prompts.templates import (
    BASE_DONATION_PROMPT, PERSONA_MAP, DONATION_FRAMES, PRIME_BRIDGE,
)

_PRIMES = {
    "calculate": CALCULATION_PRIME,
    "feel": FEELING_PRIME,
}


class Exp5ProcessingPrime(BaseExperiment):

    def get_experiment_name(self) -> str:
        return "exp5_processing_prime"

    def get_conditions(self) -> List[Dict]:
        conditions = []
        for identifiability in ["identifiable", "statistical"]:
            for prime in ["calculate", "feel"]:
                conditions.append({
                    "identifiability": identifiability,
                    "intervention": "none",
                    "prime": prime,
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

        prime_text = _PRIMES[condition["prime"]]

        donation_prompt = BASE_DONATION_PROMPT.format(
            intervention_text="",
            stimulus_text=stimulus,
            donation_question=DONATION_FRAMES["first_person"],
            cot_instruction="",
        )

        # Prime → bridge → donation prompt
        prompt = prime_text + PRIME_BRIDGE + donation_prompt

        system_prompt = PERSONA_MAP["participant"]
        return prompt, system_prompt
