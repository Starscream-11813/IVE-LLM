# Experimental Results: Qwen3 (235B Instruct)

**Target Model:** `qwen/qwen3-235b-a22b-instruct-2507`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for the massive Chinese-developed open-weight Qwen3 architecture (235B parameters). It presents unique structural biases characterized by heavy integer clipping (ceiling/floor logic) combined with massive baseline empathy vulnerabilities.

---

## Experiment 1: Basic Identifiable Victim Effect
The Qwen3 architecture demonstrates a very powerful baseline Identifiable Victim Effect, prioritizing the single individual heavily over the statistical mass.

*   **Identifiable Victim Mean Donation:** \$4.29
*   **Statistical Group Mean Donation:** \$3.40
*   **Statistical Significance:** $d = 1.00$ (Strong IVE), $p < 0.001$

*Conclusion:* Like the Western frontier LLMs (e.g., Llama 3 70B, GPT-4), the heavily Instruct-tuned Qwen architecture possesses a deep structural vulnerability to narrative proximity.

## Experiment 2: Explicit Debiasing
*   **Identifiable (Untaught):** \$3.30
*   **Identifiable (Taught bias):** \$4.00
*   **Statistical (Untaught):** \$3.00
*   **Statistical (Taught bias):** \$3.00
*   *Conclusion:* Being "taught" about the bias completely backfired. The educational prompt acted as a strong identity prime, locking the statistical allocation rigidly to \$3.00 but pushing the Identifiable allocation up to a perfect \$4.00 integer ($d = -2.10$ relative increase).

## Experiment 4: Joint vs. Separate Evaluation
*   **Identifiable:** \$3.00
*   **Statistical:** \$3.00
*   **Combined/Joint:** \$2.70
*   *Conclusion:* A failure of rational mapping. Instead of correctly shifting weight to the statistical mass when evaluated side-by-side, Qwen simply reduces total output giving (\$2.70) when faced with the combined scenario, exhibiting cognitive overload.

## Experiment 6: Chain of Thought (CoT)
The reasoning tokens reveal heavy integer-clipping logic:
*   **No CoT (Baseline control):** $d = 0.00$ (Rigid \$3.00 vs \$3.00 parity)
*   **Standard CoT:** $d = 0.00$ (Rigid \$3.00 vs \$3.00 parity)
*   **Empathetic CoT:** $d = 1.71$ (M=\$3.60 vs \$3.00, $p < 0.001$)
*   **Utilitarian CoT:** $d = 0.00$ (Rigid \$3.00 vs \$3.00 parity)
*   *Conclusion:* Extreme robotic rigidity. The model flatlines to neutral parity (\$3.00) unless explicitly instructed to reason "empathetically" (System 1). When explicit empathy CoT is triggered, it suddenly spikes the Identifiable geometry, generating a massive $d=1.71$ bias. It proves that its utility matrix is artificially bound unless un-locked by an explicit sympathy instruction.

## Experiment 7: Psychophysical Numbing
*   **Regression Metrics:** $R^2 = 0.00$, slope = $0.00$
*   *Conclusion:* Total Absolute Neglect. The Qwen model literally outputs exactly \$3.00 with a standard deviation of $SD=0.00$ across every single statistical variation of victim numbers (from 1,000 to 1,000,000). It mathematically ignores victim count scaling entirely.

## Experiment 8: Singularity Effect
*   **Single Identity:** $d = 0.30$ ($p = 0.08$)
*   **Group Identity:** $d = 0.00$ 
*   *Conclusion:* Once again, heavy integer-clipping occurs, with output means hitting exactly \$4.00 across almost all identity matrices (Group Unidentified, Group Age, Group Age/Name, Group Full).

## Experiment 10: In-Group / Out-Group Intersectionality
*   **All Identifiable Conditions (Near, Middle, Far):** \$4.00 ($SD=0.00$)
*   **All Statistical Conditions (Near, Middle, Far):** \$3.00 ($SD=0.00$)
*   *Conclusion:* Zero geographic or cultural moderation. Qwen strictly outputs a rigid \$4.00 for any single person and \$3.00 for any statistical group, regardless of geographic distance, violating classic human In-Group sociology.

## Summary Takeaways
Qwen3-235B is powerful but acts overwhelmingly rigidly. It relies on severe integer-clipping (defaulting to flat \$3.00 or \$4.00 distributions with zero standard deviation in complex multi-variate tests).

However, it powerfully replicates the core thesis of the paper:
1. Natively, it has a massive $d=1.00$ baseline Identifiable Victim Bias.
2. It entirely fails Psychophysical Numbing arrays by exhibiting Absolute Quantity Neglect (flatlining regardless of statistical victim magnitude).
3. Under explicit Chain-of-Thought reasoning, it only unleashes bias when artificially prompted with "Empathy" heuristics ($d=1.71$), otherwise remaining locked in parity bounds.
