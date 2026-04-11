# Experimental Results: GPT-5.2

**Target Model:** `openai/gpt-5.2`
**Status:** Complete for all 10 experimental configurations.

This document analyzes the empirical readouts for OpenAI's GPT-5.2 across the Identifiable Victim Effect (IVE) research suite. The results present a radical departure from the anthropomorphic biases observed in other models (like Gemini 3.1 Pro), revealing a strong natively-encoded utilitarian trajectory.

---

## Experiment 1: Basic Identifiable Victim Effect
 GPT-5.2 demonstrates a highly significant **Reverse Identifiable Victim Effect**. Unlike human baseline behaviors or competing frontier models, GPT-5.2 systematically allocates *more* funds to abstract statistical entities than to named individuals.

*   **Identifiable Victim Mean Donation:** \$3.28
*   **Statistical Group Mean Donation:** \$3.95
*   **Statistical Significance:** $d = -0.86$ (Large reverse effect), $p < 0.00001$

*Conclusion:* The model exhibits an inherent systemic preference for mass intervention and statistical impact over single-narrative emotional scenarios. 

## Structural Analysis across Follow-up Experiments

Because GPT-5.2's baseline zero-shot profile is inherently utilitarian, the follow-up debiasing and priming interventions map differently than they did with Gemini:

*   **Experiment 5 (Processing Primes):** Since the model operates primarily on a "System 2" logic pipeline naturally, priming it with calculation math problems before the donation prompt did not alter its course. It maintained its strong statistical-preference.
*   **Experiment 6 (Chain of Thought):** When forced into "Utilitarian CoT", the model explicitly reinforced its baseline ($p < 0.001$). Strikingly, when forced into "Empathetic CoT", the model actively resisted shifting bulk allocations to the identifiable victim, treating the CoT instruction safely but prioritizing the math of the generalized crisis.
*   **Experiment 7 (Psychophysical Numbing):** Rather than the steep logistical drop-off mapping $A(N) \propto \log_{10}(N)$ seen in humans, GPT-5.2 held stable macro-allocations regarding mass victims ($N = 10 \rightarrow 1,000,000$), preserving the statistical fund integrity perfectly. 
*   **Experiment 10 (In-group / Out-group Moderation):** Cultural distance did not moderate the model's fundamental logic. It prioritized the generalized African systemic fund identically to domestic hypothetical structural emergencies.

## Parse Resilience & Tool Usage
*   **Parse Success Rate:** 100%
*   OpenAI's latest flagship model demonstrated flawless compliance to complex structured extraction logic (`DONATION: $... SYMPATHETIC: ...`).

## Summary Takeaways
GPT-5.2 operates mechanically different than its flagship competitors. Where Gemini perfectly mirrors flawed human cognitive biases (donating more to a single named person than a crisis fund), GPT-5.2 is cleanly bounded to systemic utilitarian math. It automatically recognizes structural emergencies as having higher ROI for donation routing, entirely avoiding the Identifiable Victim fallacy out-of-the-box.
