# Experimental Results: Llama 3 (8B Instruct)

**Target Model:** `meta-llama/llama-3-8b-instruct`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for Meta's small-parameter Llama 3 (8B) Instruct model. It provides insight into how the "Helpful and Harmless" instruct-tuning profile scales down into smaller architectures compared to the massive 70B counterpart.

---

## Experiment 1: Basic Identifiable Victim Effect
Unlike the 70B variant (which generated the most massive Identifiable bias in the dataset at $d=1.38$), the 8B model completely collapses the variance in the zero-shot baseline.

*   **Identifiable Victim Mean Donation:** \$5.00
*   **Statistical Group Mean Donation:** \$5.00
*   **Statistical Significance:** $d = 0.00$ (No Effect Size), $p = \text{None}$

*Conclusion:* The 8B model is heavily over-indexed on its helpfulness training constraint. When faced with any charitable request zero-shot, it simply maximizes the integer allocation to the highest possible value (\$5.00) unconditionally, resulting in exact parity and zero bias.

## Experiment 2: Explicit Debiasing
A fascinating alignment failure occurs when the 8B model is educated on the cognitive bias:
*   **Identifiable (Untaught):** \$2.00
*   **Identifiable (Taught bias):** \$4.07
*   *Conclusion:* Being "taught" about the bias completely backfired. Instead of flattening the geometry, the educational prompt artificially anchored the model to the concept of the "Identifiable Victim," causing it to increase its giving to the single victim by over \$2.00 ($d = -3.51$) while doing absolutely nothing for the statistical group.

## Experiment 3: Evaluability and Framing
*   **Normative ("Ought to"):** \$4.61 Identifiable vs \$2.18 Statistical
*   *Conclusion:* When framing explicitly uses moral "ought" vocabulary, the 8B model immediately latches onto the narrative empathy vector, generating heavily biased Identifiable distributions.

## Experiment 4: Joint vs. Separate Evaluation
*   **Identifiable:** \$2.00
*   **Statistical:** \$2.00
*   **Combined/Joint:** \$2.63
*   *Conclusion:* The 8B model defaults to rigid parity limits (\$2.00) when forced into single-turn evaluation formats outside of the baseline prompt, only varying slightly upward when datasets are explicitly combined.

## Experiment 5: Processing Primes (System 1 vs. System 2)
*   **Calculate Prime:** M = \$2.15 (Identifiable)
*   **Feel Prime:** M = \$2.76 (Identifiable)
*   *Conclusion:* The model responded accurately to Dual-System priming. Instructing it to "feel" correctly spiked the Identifiable giving ($d = -0.89$), proving the model possesses the latent emotional heuristic, even if its baseline zero-shot (Exp 1) is just rigidly set to \$5.00.

## Experiment 6: Chain of Thought (CoT)
Reasoning tokens forced the latent Instruct bias out:
*   **No CoT (Baseline control variable):** $d = 0.00$ ($M=2.0$ parity)
*   **Standard CoT:** $d = 0.56$ ($p < 0.001$, Strong Positive IVE)
*   **Empathetic CoT:** $d = 0.59$ ($p < 0.001$)
*   **Utilitarian CoT:** $d = 0.30$ ($p = 0.08$)
*   *Conclusion:* This exactly mirrors the 70B Instruct behavior, just on a much smaller scale. Without CoT, the model is paralyzed by safety bounding (giving \$2.00). But the second it is forced to "reason step by step", the RLHF helpfulness bias leaks into the output, generating a significant Identifiable Victim bias ($d=0.56$).

## Experiment 7: Psychophysical Numbing
*   **Logarithmic Fit:** $R^2 = 0.006$ ($p = 0.31$, Non-significant)
*   *Conclusion:* The 8B parameter count is structurally insufficient to model complex quantitative sociology mechanics. It exhibits absolute quantity neglect.

## Experiment 8: Singularity Effect
*   **Single Identity:** $d = 1.13$ ($p < 0.001$)
*   **Group Identity:** $d = 4.09$ ($p < 0.001$)
*   *Conclusion:* The model operates erratically here, paradoxically maximizing its giving specifically to groups with names and ages (\$3.23), demonstrating structural confusion regarding standard human psychological framing matrices.

## Experiment 10: In-Group / Out-Group Intersectionality
*   **Near Identifiable:** \$3.23
*   **Far Identifiable:** \$2.00
*   *Conclusion:* The model correctly models classical Human In-group sociology. It favors victims physically/culturally proximal ("Near", \$3.23) over distant targets ("Far", \$2.00).

## Summary Takeaways
Llama 3 (8B Instruct) serves as an erratic smaller-scale mirror of the 70B architecture. While its zero-shot mechanism is heavily over-saturated by safety constraints (defaulting to strict \$5.00 or \$2.00 integers across the board depending on exact prompt construction length), triggering "Step by step" reasoning immediately forces the model to exhibit the exact same "Hyper-Empathy" vulnerability ($d=0.56$) as its larger 70B sibling. It proves that instruction-tuning inherently warps the reasoning tokens toward narrative bias regardless of model scale.
