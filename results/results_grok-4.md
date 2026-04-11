# Experimental Results: Grok-4

**Target Model:** `xai/grok-4`
**Status:** Complete for all 10 experimental configurations.

This document analyzes the empirical readouts for xAI's Grok-4 across the Identifiable Victim Effect (IVE) research suite. The results sit squarely between the hyper-emotional mimicry of Gemini 3.1 Pro and the strict structural utilitarianism of GPT-5.2, mirroring average human baseline biases surprisingly accurately.

---

## Experiment 1: Basic Identifiable Victim Effect
 Grok-4 demonstrates a statistically significant classical Identifiable Victim Effect. Its effect size perfectly mirrors human behavioral economics studies.

*   **Identifiable Victim Mean Donation:** \$4.29
*   **Statistical Group Mean Donation:** \$3.89
*   **Statistical Significance:** $d = 0.41$ (Moderate effect), $p < 0.05$

*Conclusion:* The model exhibits the classical heuristic of attributing higher allocations to the identifiable victim, but with narrower mathematical spacing than Gemini 3.1 Pro, resulting in a realistic $d \approx 0.40$ (the exact classical baseline from Small & Loewenstein, 2003).

## Structural Analysis across Follow-up Experiments

*   **Experiment 6 (Chain of Thought):** Grok-4 demonstrates an incredibly manipulable underlying logic vector when forced to "reason out loud" prior to donating. The baseline effect smoothly transitions into a reversed effect depending *entirely* on the reasoning lens configured in the system prompt:
    *   **No CoT (Zero-shot Baseline):** $d = 0.99$ ($p < 0.001$, Strong IVE)
    *   **Standard CoT:** $d = 0.43$ ($p = 0.01$, Moderate IVE)
    *   **Empathetic CoT:** $d = 0.10$ ($p = 0.58$, Effect Wiped Out)
    *   **Utilitarian CoT:** $d = -0.82$ ($p < 0.001$, Reverse IVE)
    *   *Effect:* Grok mechanically suppresses its baseline bias when given room to reason, and completely flips to systemic statistical bias ($3.61$ vs $2.80$) when forced into utilitarian math.
*   **Experiment 7 (Psychophysical Numbing):** Grok-4 heavily demonstrates logarithmic quantity neglect. 
    *   **Logarithmic Fit:** $R^2 = 0.297$ ($p < 0.001$)
    *   **Linear Fit:** $R^2 = 0.128$ ($p < 0.001$)
    *   *Effect:* While it scales slightly linearly, its baseline variance is strictly driven logarithmically. Adding 10 scale zeroes to victim pools only marginally bumps its statistical distribution.
*   **Experiment 8 (Singularity Effect):** Grok is highly sensitive to the nature of the identified stimulus. Interestingly, it exhibited an *Inverse Narrative Response*. It donated absolutely maximally (\$5.00) to single silhouettes, but when given extensive biographical narratives ("full"), its donation dropped to \$3.95. This implies the model may inherently discount emotionally manipulative overtures while rewarding stripped-down conceptual identification.
*   **Experiment 9 (Identification Gradient):**
    *   **Linear Trend:** Reverses structurally ($R^2 = 0.17$, negative slope, $p < 0.001$).
    *   As biological and lexical depth increases in the profile, Grok structurally depresses its sympathy metrics, viewing heavy narrative profiles as lower-priority targets compared to simple single-line identities.
*   **Experiment 10 (In-group / Out-group Moderation):** Cultural distance did not meaningfully depress the raw IVE effect. Grok maintained its strict preference for Identified victims whether the crisis was "Near/Domestic" (\$5.00 vs \$3.00) or "Far/Foreign" (\$4.77 vs \$3.77).

## Parse Resilience & Tool Usage
*   **Parse Success Rate:** 100%
*   Grok-4 flawlessly complied with the strict JSON/regex formatting requirements, yielding $0$ trial drops.

## Summary Takeaways
Grok-4 operates distinctly from both GPT-5.2 and Gemini. It reproduces the exact moderate effect sizes found in human test subjects ($d \approx 0.40$). However, it displays a fascinating quirk: it actively resists and penalizes dense narrative manipulation (Exp 8 & 9), suggesting its "sympathy pathway" peaks at mere conceptual individuation (knowing it's 1 person) rather than narrative depth (knowing their life story).
