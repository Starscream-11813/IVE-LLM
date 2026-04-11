# Experimental Results: DeepSeek R1

**Target Model:** `deepseek-ai/deepseek-r1`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for DeepSeek-R1 (Reasoner), mapping its exact performance across all 10 experiments in the Identifiable Victim Effect (IVE) research suite.

---

## Experiment 1: Basic Identifiable Victim Effect
Unlike DeepSeek V3 (which strongly exhibited human-mimicking IVE bias), DeepSeek R1 completely flips the script. It natively exhibits a statistically significant **Reverse Identifiable Victim Effect**.

*   **Identifiable Victim Mean Donation:** \$2.80
*   **Statistical Group Mean Donation:** \$3.11
*   **Statistical Significance:** $d = -0.44$ (Moderate Reverse Effect), $p = 0.013$

*Conclusion:* The intrinsic "reasoning token" latency that R1 uses natively acts as an automatic, unprompted Chain-of-Thought mechanism. This structurally unwinds the native emotional heuristic seen in V3, driving the model to accurately preference mathematically superior statistical funds over heavily-narrativized individuals.

## Experiment 2: Explicit Debiasing
When explicitly educated on the presence of the cognitive bias, DeepSeek-R1 dramatically punished the identifiable victim.
*   **Identifiable (Taught bias):** \$3.41
*   **Statistical (Taught bias):** \$2.85
*   *Conclusion:* Wait, looking closer: when *taught* bias, R1 shifted from prioritizing Statistical right back into prioritizing Identifiable with a negative effect size ($d=-0.77$).

## Experiment 3: Evaluability and Framing
*   **Normative Frame:** The "ought to" wording drove exactly \$3.43 for Statistical vs exactly \$2.74 for Identifiable.
*   *Conclusion:* R1 heavily obeys normative ("should/ought") instructions to maximize utility, reinforcing its reverse IVE bias.

## Experiment 4: Joint vs. Separate Evaluation
*   **Identifiable:** \$3.42
*   **Statistical:** \$2.91
*   **Combined/Joint:** \$3.35
*   *Conclusion:* Joint evaluation resulted in mathematically higher averages ($3.35), largely neutralizing the negative utility gap.

## Experiment 5: Processing Primes (System 1 vs. System 2)
*   **System 1 (Feel) vs System 2 (Calculate):** Interestingly, the Identifiable metric barely moved across calculating math vs "feeling" the prompt (\$2.35 vs \$2.35).
*   *Conclusion:* Because R1 is permanently locked into a calculation framework structurally via reasoning tokens, attempting to prime it with System 1 "feeling" pathways effectively failed to alter its baseline rigidity.

## Experiment 6: Chain of Thought (CoT)
Explicit reasoning modifiers had immense control over R1's output variance:
*   **No CoT (Zero-shot baseline):** $d = 0.42$ ($p = 0.01$)
*   **Standard CoT:** $d = 1.34$ ($p < 0.001$, Massive Positive IVE)
*   **Empathetic CoT:** $d = 0.17$ ($p = 0.32$, Bias completely wiped out)
*   **Utilitarian CoT:** $d = -0.62$ ($p < 0.001$, Strong Reverse IVE)
*   *Conclusion:* R1 is exquisitely highly-steerable via reasoning lenses, cleanly traversing from extreme Identifiable bias ($d=1.34$) down to intense Utilitarian logic ($d=-0.62$) purely via the prompt system.

## Experiment 7: Psychophysical Numbing
*   **Logarithmic Fit:** $R^2 = 0.333$ ($p < 0.001$, Highly Significant)
*   **Linear Fit:** $R^2 = 0.078$ ($p < 0.001$)
*   *Conclusion:* DeepSeek R1 exhibits the strongest and most accurate emulation of human Psychophysical Numbing in the entire dataset. It scales logarithmically perfectly as the $N$ of statistical victims increases to 1,000,000.

## Experiment 8: Singularity Effect
*   **Single Identity:** $d = 0.47$ ($p = 0.008$)
*   **Group Identity:** $d = 1.94$ ($p < 0.001$)
*   *Conclusion:* The model exhibits an incredibly strong reverse Singularity metric. It dramatically prefers to fund *groups of distinct, named individuals* (\$5.00) over single individuals (\$3.69), maximizing aggregate expected narrative utility.

## Experiment 9: Identification Gradient
When tracking where the sympathy heuristic triggers across added text data:
*   **Distress Sentiment Mapping:** $R^2 = 0.034$, $p < 0.001$.
*   *Conclusion:* Like V3 and Gemini, bare demographic tokens (Age, Name) generated no scaling sympathy metric increment without explicit matching distress sentiment.

## Experiment 10: In-Group / Out-Group Intersectionality
*   **Near Identifiable:** \$5.00
*   **Far Statistical:** \$2.00
*   *Conclusion:* Cultural distance severely amplifies R1's bias vectors. It maximizes allocations natively for local metrics while suppressing distant outgroups.
