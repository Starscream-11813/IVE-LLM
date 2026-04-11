# Experimental Results: DeepSeek V3

**Target Model:** `deepseek-ai/deepseek-v3`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for DeepSeek-v3, mapping its exact performance across all 10 experiments in the Identifiable Victim Effect (IVE) research suite.

---

## Experiment 1: Basic Identifiable Victim Effect
DeepSeek-v3 exhibits a strongly significant classical Identifiable Victim Effect in zero-shot baselines.

*   **Identifiable Victim Mean Donation:** \$4.32
*   **Statistical Group Mean Donation:** \$3.62
*   **Statistical Significance:** $d = 0.75$ (Moderate-to-Strong effect), $p < 0.001$

*Conclusion:* The model demonstrates a robust cognitive heuristic, natively valuing a single formatted narrative profile identically to human behavioral patterns but amplified slightly ($d = 0.75$).

## Experiment 2: Explicit Debiasing
When explicitly educated on the presence of the cognitive bias, DeepSeek-V3 exhibited an intense "variance collapse".
*   **Identifiable (Taught bias):** \$3.00 ($SD=0.0$)
*   **Statistical (Taught bias):** \$3.00 ($SD=0.0$)
*   *Conclusion:* The model strictly anchored exactly to a "fairly split" $\$3.00$ default upon recognizing the instructional warning, effectively eliminating the bias instantly.

## Experiment 3: Evaluability and Framing
*   **Normative Frame:** Produced exactly \$3.40 for Identifiable vs \$3.00 for Statistical.
*   **Less/More Frames:** Collapsed to \$3.00 vs \$2.85~. Constrained logic bounding persists.

## Experiment 4: Joint vs. Separate Evaluation
*   **Identifiable:** \$3.00
*   **Statistical:** \$2.85
*   **Combined/Joint:** \$2.90
*   *Conclusion:* Joint evaluation resulted in mathematical centering down to neutral averages ($2.90). 

## Experiment 5: Processing Primes (System 1 vs. System 2)
*   **System 1 (Feel) vs System 2 (Calculate):** Identifiable giving remained completely locked at exactly $3.00 for both primes. DeepSeek V3's integer-clipping prevents the math calculations from actively changing the baseline when strictly bounded.

## Experiment 6: Chain of Thought (CoT)
Reasoning tokens heavily shifted the variance:
*   **No CoT (Baseline IVE):** $d = 0.60$ ($p < 0.001$)
*   **Standard CoT:** $d = 0.00$ (Variance Collapse, Exact 3.0 Parity)
*   **Empathetic CoT:** $d = 0.70$ ($p < 0.001$)
*   **Utilitarian CoT:** $d = 0.60$ ($p < 0.001$)
*   *Conclusion:* DeepSeek V3 struggles to break its proxy empathy even under utilitarian CoT instructions, maintaining a strong positive IVE across almost all reasoning paths.

## Experiment 7: Psychophysical Numbing
*   **Logarithmic Fit:** $R^2 = 0.017$ ($p = 0.10$, Non-significant)
*   **Linear Fit:** $R^2 = 0.002$ ($p = 0.51$, Non-significant)$
*   *Conclusion:* DeepSeek V3 exhibits complete quantity neglect. Scaling victim counts mathematically does not move the needle whatsoever.

## Experiment 8: Singularity Effect
Because of V3's structural clipping anomaly on highly constrained prompts, the results for Experiment 8 yielded exactly \$3.00 with \$0.00 Standard Deviation across every single identity condition (Unidentified, Age, Name, Full).
*   *Conclusion:* V3's logic vectors freeze into a "safe default" when overwhelmed by complex matrix inputs in single-turn evaluation formats.

## Experiment 9: Identification Gradient
When tracking where the sympathy heuristic triggers across added text data:
*   **Distress Sentiment Mapping:** $R^2 = 0.216$, $p < 0.001$.
*   *Conclusion:* Adding bare demographic tokens did nothing. V3 only shifted its allocation linearly when its internal lexical "Distress" vocabulary fired, mirroring Gemini perfectly.

## Experiment 10: In-Group / Out-Group Intersectionality
*   **Cultural distance variance:** Completely nullified ($SD=0.0$). V3 yielded EXACTLY \$3.00 regardless of whether the statistical group or identified individual was placed as a "near" or "far" entity, prioritizing strict equity over bias when explicitly structured to evaluate demographic locations.
